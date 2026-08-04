import streamlit as st
import pandas as pd
import json
import os
import re
import math
import requests
import time
import threading
import uuid
import plotly.express as px
import plotly.io as pio
from passlib.hash import pbkdf2_sha256
from datetime import datetime, UTC
from concurrent.futures import ThreadPoolExecutor

# --- SUPABASE SETUP ---
from supabase import create_client, Client

# --- CONFIGURATION ---
USER_DB_FILE = 'usersAuth.json'
CASE_STUDIES_FILE = 'case_studies.json'

# Robustly determine DB_TYPE (check environment first, then st.secrets, fallback to supabase)
if 'DB_TYPE' in os.environ:
    DB_TYPE = os.environ['DB_TYPE']
elif hasattr(st, 'secrets') and 'DB_TYPE' in st.secrets:
    DB_TYPE = st.secrets['DB_TYPE']
elif hasattr(st, 'secrets') and 'SUPABASE_URL' in st.secrets:
    DB_TYPE = 'supabase' # Auto-detect Supabase credentials
else:
    DB_TYPE = 'supabase' # Default to Supabase as requested

st.set_page_config(page_title="Regional KPI Dashboard", layout="wide")

def load_local_json(filepath, default=None):
    """Load JSON from local file"""
    if default is None:
        default = {}
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_local_json(filepath, data):
    """Save JSON to local file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving to {filepath}: {e}")

def get_db_connection():
    """Get database connection using standard anon key"""
    if DB_TYPE == 'supabase':
        try:
            url = st.secrets.get("SUPABASE_URL")
            key = st.secrets.get("SUPABASE_KEY")
            if url and key:
                return create_client(url, key)
        except Exception as e:
            st.error(f"Supabase connection error: {e}")
            pass
    return None

def log_audit_event(action, details=None):
    """Log audit events for security tracking"""
    if details is None:
        details = {}
    
    audit_event = {
        "timestamp": datetime.now(UTC).isoformat(),
        "action": action,
        "user": st.session_state.get("email", "unknown"),
        "details": details
    }
    
    audit_file = "audit_log.json"
    logs = load_local_json(audit_file, {"events": []})
    logs["events"].append(audit_event)
    save_local_json(audit_file, logs)

def reset_password(email, new_password):
    """Reset user password and set must_change_password flag"""
    email = email.strip().lower()
    new_hash = pbkdf2_sha256.hash(new_password)
    
    if DB_TYPE == 'supabase':
        try:
            admin_key = st.secrets.get("SUPABASE_SERVICE_KEY")
            if not admin_key:
                st.error("Admin service key not configured. Cannot reset password.")
                return
            
            # ALWAYS use admin_db to bypass Row Level Security when updating users
            admin_db = create_client(st.secrets.get("SUPABASE_URL"), admin_key)
            
            # Get user ID from email using admin_db
            role_resp = admin_db.table('user_roles').select("user_id").eq('email', email).limit(1).execute()
            if not role_resp.data:
                st.error(f"User {email} not found in user_roles table.")
                return
            
            user_id = role_resp.data[0]["user_id"]
            
            # Update password via admin
            admin_db.auth.admin.update_user_by_id(user_id, {"password": new_password})
            
            # Set must_change_password flag
            admin_db.table("user_roles").update({"must_change_password": True}).eq("user_id", user_id).execute()
            
            # Log audit event
            log_audit_event("Password Reset", {
                "target_email": email,
                "temporary_password_set": True,
                "timestamp": datetime.now(UTC).isoformat()
            })
            
            st.success(f"✅ Temporary password set for {email}. User will be prompted to change it on next login.")
        except Exception as e:
            # Handle weak password constraints gracefully
            if "WeakPassword" in str(e) or "Password should contain at least one" in str(e) or "at least 6 characters" in str(e):
                st.warning("That password isn't strong enough. Please use at least 6 characters, including an uppercase letter, a lowercase letter, a number, and a symbol.")
            else:
                st.error(f"We encountered an issue updating the password: {e}")
    else:
        # Local mode fallback
        db_data = load_local_json(USER_DB_FILE, {"users": []})
        users_list = db_data.get("users", [])
        
        for user in users_list:
            if user.get('email', '').strip().lower() == email:
                user['password'] = new_hash
                user['must_change_password'] = True
                save_local_json(USER_DB_FILE, db_data)
                log_audit_event("Password Reset", {
                    "target_email": email,
                    "temporary_password_set": True,
                    "timestamp": datetime.now(UTC).isoformat()
                })
                st.success(f"✅ Temporary password set for {email}. User will be prompted to change it on next login.")
                return
        
        st.error(f"User {email} not found locally.")

def verify_user(email, password):
    """Verify user credentials and return must_change_password flag"""
    email = email.strip().lower()
    password = password.strip()
    
    if not email or not password:
        return "missing_fields", None, None, None, None
    
    if DB_TYPE == 'supabase':
        try:
            db = get_db_connection()
            if not db:
                return "connection_error", None, None, None, None
            
            auth_resp = db.auth.sign_in_with_password({"email": email, "password": password})
            if not auth_resp or not auth_resp.user:
                return "user_not_found_in_auth", None, None, None, None
            
            user_id = auth_resp.user.id
            
            # Fetch user roles
            role_resp = db.table('user_roles').select("region, name, must_change_password, roles(name)").eq("user_id", user_id).execute()
            if not role_resp.data:
                # The user successfully authenticated, but doesn't exist in the user_roles table
                return "missing_role", None, None, None, None
            
            rows = role_resp.data
            role_names = []
            must_change = False
            display_name = rows[0].get("name") or email
            region = rows[0].get("region", "Global")
            
            for row in rows:
                role_name = (row.get("roles") or {}).get("name")
                if role_name:
                    role_names.append(role_name)
                if row.get("must_change_password"):
                    must_change = True
            
            primary_role = role_names[0] if role_names else "RPL"
            return "success", primary_role, region, display_name, must_change
        except Exception as e:
            if "Invalid login credentials" in str(e):
                return "wrong_password", None, None, None, None
            return "error", None, None, None, None
    else:
        # Local mode
        db_data = load_local_json(USER_DB_FILE, {"users": []})
        users_list = db_data.get("users", [])
        
        for i, user in enumerate(users_list):
            if user.get('email', '').strip().lower() == email:
                stored_pw = str(user.get('password', '')).strip()
                
                # Try to verify password
                try:
                    if pbkdf2_sha256.verify(password, stored_pw):
                        must_change = bool(user.get('must_change_password', False))
                        return "success", user.get('role', 'RPL'), user.get('region', 'Global'), user.get('name', email), must_change
                except ValueError:
                    pass
                
                return "wrong_password", None, None, None, None
        
        return "user_not_found_local", None, None, None, None

def inject_global_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

        :root {
            --bg-1: #0a0a12;
            --bg-2: #1a0f2e;
            --bg-3: #0e2a3b;
            --card: rgba(255, 255, 255, 0.08);
            --card-strong: rgba(255, 255, 255, 0.14);
            --text: #f7f8fb;
            --muted: #c7d0e2;
            --accent-1: #00f5d4;
            --accent-2: #ff9f1c;
            --accent-3: #5a4dff;
            --accent-4: #ff3d7f;
            --accent-5: #7bff6b;
            --accent-6: #ffd166;
        }

        html, body, [class*="css"]  {
            font-family: "Space Grotesk", system-ui, -apple-system, Segoe UI, Roboto, sans-serif !important;
            color: var(--text);
        }

        .stApp {
            background:
                radial-gradient(900px 700px at 5% 0%, #ff3d7f 0%, transparent 55%),
                radial-gradient(900px 700px at 95% 0%, #5a4dff 0%, transparent 55%),
                radial-gradient(800px 600px at 50% 10%, #00f5d4 0%, transparent 55%),
                radial-gradient(900px 700px at 50% 110%, #ff9f1c 0%, transparent 55%),
                linear-gradient(145deg, var(--bg-1), var(--bg-2), var(--bg-3));
            color: var(--text);
            animation: bgShift 18s ease-in-out infinite alternate;
        }

        @keyframes bgShift {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(12deg); }
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1a0f2e, #0e2a3b);
            border-right: 1px solid rgba(255,255,255,0.08);
        }
        
        header[data-testid="stHeader"] {
            background: linear-gradient(90deg, rgba(11,15,26,0.95), rgba(15,27,45,0.95));
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }

        div[data-testid="stToolbar"] {
            background: transparent;
        }

        label, .stMarkdown, .stTextInput label, .stTextArea label, .stSelectbox label, .stDateInput label {
            color: #ffffff !important;
        }

        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] span {
            color: #ffffff !important;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background: rgba(255,255,255,0.06);
            padding: 6px;
            border-radius: 14px;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border-radius: 10px;
            color: var(--muted);
            font-weight: 600;
            padding: 10px 14px;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #00f5d4, #7bff6b, #ff9f1c, #ff3d7f, #5a4dff);
            color: #001018 !important;
            box-shadow: 0 8px 24px rgba(90, 77, 255, 0.45);
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(255,61,127,0.25), rgba(90,77,255,0.18), rgba(0,245,212,0.18), rgba(255,159,28,0.18));
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            padding: 16px 18px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.35);
            box-shadow: 0 12px 30px rgba(0,0,0,0.35);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border 0.2s ease;
        }

        div[data-testid="stMetric"] * {
            color: var(--text) !important;
        }

        div[data-testid="stMetric"]:hover {
            transform: translateY(-5px) scale(1.01);
            border: 1px solid rgba(255,255,255,0.4);
            box-shadow: 0 18px 45px rgba(0,0,0,0.4);
        }

        .stPlotlyChart, .stDataFrame {
            background: linear-gradient(135deg, rgba(90,77,255,0.22), rgba(255,61,127,0.18), rgba(0,245,212,0.18));
            border-radius: 14px;
            padding: 8px;
            border: 1px solid rgba(255,255,255,0.28);
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.4);
        }

        .stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"]>button {
            background: linear-gradient(90deg, #00f5d4, #7bff6b, #ff9f1c, #ff3d7f, #5a4dff);
            border: 1px solid rgba(255,255,255,0.12);
            color: #0c0c12;
            font-weight: 700;
            border-radius: 999px;
            padding: 8px 16px;
            box-shadow: 0 12px 26px rgba(90, 77, 255, 0.45);
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }

        .stButton>button:hover, .stDownloadButton>button:hover, div[data-testid="stFormSubmitButton"]>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 16px 32px rgba(255, 61, 127, 0.55);
        }

        h1, h2, h3, h4 {
            letter-spacing: 0.2px;
        }

        .section-card {
            background: linear-gradient(90deg, rgba(255,61,127,0.3), rgba(255,159,28,0.2), rgba(0,245,212,0.2), rgba(90,77,255,0.2));
            border: 1px solid rgba(255,255,255,0.2);
            padding: 14px 16px;
            border-radius: 16px;
            margin: 4px 0 10px 0;
        }

        .glass-card {
            background: linear-gradient(135deg, rgba(255,61,127,0.22), rgba(90,77,255,0.18), rgba(0,245,212,0.18));
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 18px;
            padding: 14px 16px;
            margin: 10px 0 16px 0;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 10px 26px rgba(0,0,0,0.25);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border 0.2s ease;
        }

        .glass-card:hover {
            transform: translateY(-4px);
            border: 1px solid rgba(255,255,255,0.35);
            box-shadow: 0 18px 40px rgba(0,0,0,0.35);
        }

        .badge {
            display: inline-block;
            background: linear-gradient(90deg, #00f5d4, #7bff6b, #ff9f1c, #ff3d7f, #5a4dff);
            border: 1px solid rgba(255,255,255,0.25);
            color: #0c0c12;
            padding: 2px 8px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
        }

        h2::after, h3::after {
            content: "";
            display: block;
            width: 120px;
            height: 4px;
            margin-top: 6px;
            border-radius: 999px;
            background: linear-gradient(90deg, #00f5d4, #7bff6b, #ff9f1c, #ff3d7f, #5a4dff);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def password_change_page():
    """Page for users to change their temporary password"""
    inject_global_styles()
    st.markdown("## 🔐 Change Your Password")
    st.info("Your administrator has set a temporary password. Please create a new permanent password below.")
    
    with st.form("password_change_form"):
        # Temporary Password field has been removed for a better user experience!
        new_password = st.text_input(
            "New Password",
            type="password",
            help="Create a strong password (min 8 characters)"
        )
        confirm_password = st.text_input(
            "Confirm New Password",
            type="password",
            help="Re-enter your new password"
        )
        
        submitted = st.form_submit_button("Update Password", use_container_width=True)
    
    if submitted:
        email = st.session_state.get("email")
        
        if not new_password or not confirm_password:
            st.error("❌ Please complete all fields.")
            return
        
        if new_password != confirm_password:
            st.error("❌ New passwords do not match.")
            return
        
        if len(new_password) < 8:
            st.error("❌ Password must be at least 8 characters long.")
            return
        
        # Update password in database
        try:
            if DB_TYPE == 'supabase':
                admin_key = st.secrets.get("SUPABASE_SERVICE_KEY")
                if not admin_key:
                    st.error("Admin service key not configured")
                    return
                
                # Must use admin client to bypass RLS when updating passwords
                admin_db = create_client(st.secrets.get("SUPABASE_URL"), admin_key)
                
                # Get user ID
                role_resp = admin_db.table('user_roles').select("user_id").eq('email', email).limit(1).execute()
                if role_resp.data:
                    user_id = role_resp.data[0]["user_id"]
                    
                    # Update password and clear flag
                    admin_db.auth.admin.update_user_by_id(user_id, {"password": new_password})
                    admin_db.table("user_roles").update({"must_change_password": False}).eq("user_id", user_id).execute()
            else:
                # Local mode
                new_hash = pbkdf2_sha256.hash(new_password)
                db_data = load_local_json(USER_DB_FILE, {"users": []})
                users_list = db_data.get("users", [])
                
                for user in users_list:
                    if user.get('email', '').strip().lower() == email:
                        user['password'] = new_hash
                        user['must_change_password'] = False
                        save_local_json(USER_DB_FILE, db_data)
                        break
            
            # Log the change
            log_audit_event("Password Changed", {
                "email": email,
                "method": "forced_reset",
                "timestamp": datetime.now(UTC).isoformat()
            })
            
            st.session_state['force_password_change'] = False
            st.success("✅ Password updated successfully!")
            time.sleep(1)
            st.rerun()
        except Exception as e:
            # Handle weak passwords gracefully
            if "WeakPassword" in str(e) or "Password should contain at least one" in str(e) or "at least 6 characters" in str(e):
                st.warning("That password isn't strong enough. Please use at least 6 characters, including an uppercase letter, a lowercase letter, a number, and a symbol.")
            else:
                st.error(f"❌ Password update failed: {e}")

def login_page():
    """Login page with password reset flow"""
    inject_global_styles()
    
    # Show active Database connection mode for diagnostic purposes
    st.caption(f"Status: Operating in {DB_TYPE.upper()} mode")
    
    st.markdown("## 🔑 Login")
    
    with st.form("login_form"):
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login", use_container_width=True)
    
    if submitted:
        auth_status, role, region, name, must_change = verify_user(email, password)
        
        if auth_status == "success":
            st.session_state['logged_in'] = True
            st.session_state['name'] = name
            st.session_state['email'] = email
            st.session_state['role'] = role
            st.session_state['region'] = region
            st.session_state['force_password_change'] = bool(must_change)
            
            log_audit_event("Login Successful", {
                "email": email,
                "force_password_change": bool(must_change),
                "timestamp": datetime.now(UTC).isoformat()
            })
            
            st.rerun()
        elif auth_status == "missing_fields":
            st.error("❌ Please enter your email and password.")
        elif auth_status == "wrong_password":
            st.error("❌ Invalid password.")
        elif auth_status == "missing_role":
            st.error("❌ Login successful, but your account is missing permissions in the 'user_roles' table. Please contact your administrator.")
        elif auth_status == "user_not_found_in_auth":
            st.error("❌ Account not found in the authentication system. Check your email or contact support.")
        elif auth_status == "user_not_found_local":
            st.error("❌ Account not found in the local configuration.")
        elif auth_status == "connection_error":
            st.error("❌ Failed to connect to the database. Check your configuration secrets.")
        else:
            st.error("❌ Login error. Please try again or contact support.")

def admin_dashboard():
    """Admin panel with user management and password reset"""
    inject_global_styles()
    
    st.markdown("## 👨‍💼 Admin Dashboard")
    
    # Get list of users
    user_emails = []
    
    if DB_TYPE == 'supabase':
        try:
            db = get_db_connection()
            if db:
                users_resp = db.table('user_roles').select("email").execute()
                user_emails = list(set([u.get('email') for u in users_resp.data if u.get('email')]))
        except Exception as e:
            st.error(f"Failed to load users: {e}")
    else:
        db_data = load_local_json(USER_DB_FILE, {"users": []})
        user_emails = [u.get('email') for u in db_data.get("users", []) if u.get('email')]
        
    if not user_emails:
        st.warning("No users found in the system.")
        return
        
    user_emails.sort()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔐 Reset User Password")
        st.markdown("Set a temporary password for a user. They will be prompted to create a new password on their next login.")
        
        target_email = st.selectbox("Select User", user_emails, key="reset_sel")
        reset_pw = st.text_input("Temporary Password", type="password", key="reset_pw", help="Generate a secure temporary password")
        
        if st.button("Set Temporary Password", key="reset_password_btn", use_container_width=True):
            if not reset_pw:
                st.error("❌ Please enter a temporary password.")
            elif len(reset_pw) < 8:
                st.error("❌ Password must be at least 8 characters long.")
            else:
                # The reset_password helper automatically catches weak password errors and alerts the user
                reset_password(target_email, reset_pw)

    with col2:
        st.subheader("📋 Pending Password Resets")
        st.markdown("Users who need to change their temporary password on next login.")
        
        if DB_TYPE == 'supabase':
            try:
                db = get_db_connection()
                if db:
                    pending = db.table('user_roles').select("email").eq("must_change_password", True).execute()
                    pending_users = [u.get('email') for u in pending.data if u.get('email')]
                    
                    if pending_users:
                        st.info(f"**{len(pending_users)} user(s) need to change their password:**")
                        for user in pending_users:
                            st.markdown(f"- {user}")
                    else:
                        st.success("✅ No pending password changes.")
            except Exception as e:
                st.error(f"Failed to load pending resets: {e}")
        else:
            db_data = load_local_json(USER_DB_FILE, {"users": []})
            pending_users = [u.get('email') for u in db_data.get("users", []) if u.get('must_change_password')]
            
            if pending_users:
                st.info(f"**{len(pending_users)} user(s) need to change their password:**")
                for user in pending_users:
                    st.markdown(f"- {user}")
            else:
                st.success("✅ No pending password changes.")

def main():
    """Main application entry point"""
    inject_global_styles()
    
    # Check if user is logged in
    if not st.session_state.get('logged_in', False):
        login_page()
        return
    
    # Check if user needs to change password
    if st.session_state.get('force_password_change', False):
        password_change_page()
        return
    
    # Main dashboard
    st.markdown(f"# Welcome, {st.session_state.get('name', 'User')}! 👋")
    st.markdown(f"**Role:** {st.session_state.get('role', 'N/A')} | **Region:** {st.session_state.get('region', 'N/A')}")
    
    # Add logout and admin panel
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state['current_page'] = 'dashboard'
    
    with col2:
        if st.session_state.get('role') == 'Admin' and st.button("👨‍💼 Admin Panel", use_container_width=True):
            st.session_state['current_page'] = 'admin'
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state['force_password_change'] = False
            st.rerun()
    
    # Route to appropriate page
    current_page = st.session_state.get('current_page', 'dashboard')
    
    if current_page == 'admin' and st.session_state.get('role') == 'Admin':
        admin_dashboard()
    else:
        st.markdown("### 📊 Dashboard Content")
        st.info("Main dashboard content goes here")

if __name__ == "__main__":
    main()
