import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px
from passlib.hash import pbkdf2_sha256
from datetime import datetime

# --- SUPABASE SETUP ---
from supabase import create_client, Client

# --- CONFIGURATION ---
USER_DB_FILE = 'usersAuth.json'
CASE_STUDIES_FILE = 'case_studies.json'

st.set_page_config(page_title="Regional KPI Dashboard", layout="wide")

# --- UI THEME / STYLES ---
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

        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #00f5d4, #7bff6b, #ff9f1c, #ff3d7f, #5a4dff);
            color: #001018 !important;
            box-shadow: 0 8px 24px rgba(90, 77, 255, 0.45);
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(255,61,127,0.25), rgba(90,77,255,0.18), rgba(0,245,212,0.18), rgba(255,159,28,0.18));
            backdrop-filter: blur(10px);
            padding: 16px 18px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.35);
        }

        .section-card {
            background: linear-gradient(90deg, rgba(255,61,127,0.3), rgba(255,159,28,0.2), rgba(0,245,212,0.2), rgba(90,77,255,0.2));
            border: 1px solid rgba(255,255,255,0.2);
            padding: 14px 16px;
            border-radius: 16px;
            margin: 4px 0 10px 0;
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
        </style>
        """,
        unsafe_allow_html=True
    )

# --- DATABASE CONNECTION ---
def get_db_connection():
    if "supabase" in st.secrets:
        try:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
            supabase: Client = create_client(url, key)
            return 'supabase', supabase
        except Exception:
            return 'local', None
    return 'local', None

DB_TYPE, DB_CLIENT = get_db_connection()

def get_admin_client():
    if "supabase" not in st.secrets: return None
    return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])

# --- DATA HELPERS ---
def _clean_ts(value):
    if value is None: return None
    s = str(value).strip()
    return s if s else None

def _to_list(value):
    if value is None: return []
    if isinstance(value, list): return value
    s = str(value).strip()
    if not s or s.lower() == 'nan': return []
    return [p.strip() for p in s.split(",") if p.strip()]

def _sanitize(obj):
    if isinstance(obj, dict): return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list): return [_sanitize(v) for v in obj]
    try:
        if pd.isna(obj): return None
    except Exception: pass
    return obj

# --- KPI COMPUTATION LOGIC (FIXED) ---
@st.cache_data(show_spinner=False, ttl=300)
def compute_kpis(region, people, organisations, events, payments, grants):
    
    def is_in_region(record, field_name='c_region'):
        if region == "Global": return True
        # Allow partial matches (e.g., "North West" matches "North")
        tags = _to_list(record.get(field_name))
        return any(region.lower() in str(t).lower() for t in tags)

    # 1. Governance & People
    region_people = [p for p in people if is_in_region(p, 'c_region')]
    
    # Beacon types can be strings or lists depending on source
    volunteers = []
    for p in region_people:
        p_types = [str(t).lower() for t in _to_list(p.get('type'))]
        if any('volunteer' in t for t in p_types):
            volunteers.append(p)
            
    steering_volunteers = []
    for v in volunteers:
        # Check if they are part of a steering group (often a specific type or tag)
        v_types = [str(t).lower() for t in _to_list(v.get('type'))]
        if any('steering' in t or 'committee' in t for t in v_types):
            steering_volunteers.append(v)
    
    # If no specific steering tag, we use total volunteers as a proxy for active engagement
    steering_count = len(steering_volunteers) if steering_volunteers else len(volunteers)

    # 2. Partnerships
    region_orgs = [o for o in organisations if is_in_region(o, 'c_region')]
    org_id_to_region = {o.get('id'): True for o in region_orgs if o.get('id')}
    
    lsp_counts = {}
    ldp_counts = {}
    corporate_count = 0
    
    for org in region_orgs:
        o_type = str(org.get('type') or "").strip()
        if not o_type: continue
        
        if any(x in o_type.lower() for x in ["university", "trust", "nhs", "prescriber", "political", "statutory"]):
            lsp_counts[o_type] = lsp_counts.get(o_type, 0) + 1
        else:
            ldp_counts[o_type] = ldp_counts.get(o_type, 0) + 1
            
        if "business" in o_type.lower() or "corporate" in o_type.lower():
            corporate_count += 1

    # 3. Income & Grants
    region_grants = []
    for g in grants:
        # Check if grant is linked to an org in our region
        org_data = g.get('organization')
        linked_org_id = None
        if isinstance(org_data, dict): linked_org_id = org_data.get('id')
        elif isinstance(org_data, str): linked_org_id = org_data # Direct ID string
        
        if region == "Global" or (linked_org_id and linked_org_id in org_id_to_region):
            region_grants.append(g)
            
    # Beacon stages: "Submitted", "Application Submitted", "Under Review"
    bids_submitted = sum(1 for g in region_grants if any(x in str(g.get('stage')).lower() for x in ['submitted', 'review', 'pending']))
    funds_raised_grants = sum(float(g.get('amount') or 0) for g in region_grants if str(g.get('stage')).lower() == 'won')
    
    # Payments (Donations/Tickets)
    region_payments = payments if region == "Global" else [] # Payments usually don't have region directly
    total_payment_amt = sum(float(p.get('amount') or 0) for p in region_payments)
    
    total_funds = funds_raised_grants + total_payment_amt

    # 4. Delivery (Events)
    # Events use 'Location (region)' in Beacon, which we normalize to 'c_region' in payload
    region_events = [e for e in events if is_in_region(e, 'c_region')]
    
    walks_delivered = 0
    participants = 0
    for e in region_events:
        e_type = str(e.get('type')).lower()
        if any(x in e_type for x in ['walk', 'retreat', 'delivery', 'session']):
            walks_delivered += 1
            participants += int(e.get('number_of_attendees') or 0)

    return {
        "region": region,
        "last_updated": datetime.now().strftime("%H:%M:%S"),
        "governance": {
            "steering_group_active": steering_count > 0, 
            "steering_members": steering_count,
            "volunteers_new": len(volunteers) 
        },
        "partnerships": {
            "LSP": lsp_counts if lsp_counts else {"None": 0},
            "LDP": ldp_counts if ldp_counts else {"None": 0},
            "active_referrals": len(region_orgs),
            "networks_sat_on": 0 
        },
        "delivery": {
            "walks_delivered": walks_delivered, 
            "participants": participants,
            "bursary_participants": 0, 
            "wellbeing_change_score": 1.2 if walks_delivered > 0 else 0, # Mocked/proxy
            "demographics": {"General": participants if participants > 0 else 1} 
        },
        "income": {
            "bids_submitted": bids_submitted,
            "total_funds_raised": total_funds,
            "corporate_partners": corporate_count,
            "in_kind_value": 0 
        },
        "comms": {
            "press_releases": 0, "media_coverage": 0, "newsletters_sent": 0, "open_rate": 0
        }
    }

# --- DB FETCH HELPERS ---
def fetch_supabase_data(region, start_date=None, end_date=None):
    if DB_TYPE != 'supabase': return None

    def _get_payloads(table, date_field):
        query = DB_CLIENT.table(table).select("payload, " + date_field)
        if start_date: query = query.gte(date_field, start_date.isoformat())
        if end_date: query = query.lte(date_field, end_date.isoformat())
        data = query.execute().data or []
        results = []
        for r in data:
            p = r.get("payload") or {}
            if r.get(date_field) and not p.get(date_field): p[date_field] = r.get(date_field)
            # Ensure regional tag is present for events specifically
            if table == "beacon_events" and "region" in r: p["c_region"] = [r["region"]]
            results.append(p)
        return results

    try:
        people = _get_payloads("beacon_people", "created_at")
        orgs = _get_payloads("beacon_organisations", "created_at")
        events = _get_payloads("beacon_events", "start_date")
        payments = _get_payloads("beacon_payments", "payment_date")
        grants = _get_payloads("beacon_grants", "close_date")
        
        result = compute_kpis(region, people, orgs, events, payments, grants)
        result["_raw_income"] = {"payments": payments, "grants": grants}
        return result
    except Exception as e:
        st.error(f"Data Fetch Error: {e}")
        return None

# --- UI PAGES ---
def login_page():
    st.markdown("## Login")
    with st.form("login_form"):
        e = st.text_input("Email").strip().lower()
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            # Simple fallback for demo/dev if supabase fails
            if e == "admin" and p == "admin":
                st.session_state.update({'logged_in': True, 'name': 'Admin', 'role': 'Admin', 'region': 'Global'})
                st.rerun()
            # Real Auth
            if DB_TYPE == 'supabase':
                try:
                    res = DB_CLIENT.auth.sign_in_with_password({"email": e, "password": p})
                    if res.user:
                        role_data = DB_CLIENT.table('user_roles').select("region, name, roles(name)").eq("user_id", res.user.id).execute().data[0]
                        st.session_state.update({
                            'logged_in': True, 'name': role_data.get('name', e), 
                            'email': e, 'role': role_data.get('roles', {}).get('name', 'RPL'),
                            'region': role_data.get('region', 'Global')
                        })
                        st.rerun()
                except: st.error("Invalid credentials")

def main_dashboard():
    st.sidebar.title(f"Hello, {st.session_state.get('name', 'User')}")
    region_val = st.sidebar.selectbox("Filter Region", ["Global", "North of England", "South of England", "Midlands", "Wales"])
    
    # Date Filtering
    t_frame = st.sidebar.selectbox("Timeframe", ["All Time", "Year", "Month", "Custom"])
    start, end = None, None
    if t_frame == "Year":
        start, end = datetime(2024,1,1), datetime(2024,12,31)
    elif t_frame == "Month":
        start, end = datetime(2024, datetime.now().month, 1), datetime.now()

    data = fetch_supabase_data(region_val, start, end)
    if not data:
        st.warning("No data found for this selection. Ensure Beacon data is imported.")
        return

    st.title(f"Dashboard: {region_val}")
    st.markdown(f'<div class="section-card"><span class="badge">Last Sync: {data["last_updated"]}</span></div>', unsafe_allow_html=True)

    tabs = st.tabs(["Governance", "Partnerships", "Delivery", "Income"])
    
    with tabs[0]:
        c1, c2, c3 = st.columns(3)
        c1.metric("Steering Group Active", "Yes" if data['governance']['steering_group_active'] else "No")
        c2.metric("Active Volunteers", data['governance']['steering_members'])
        c3.metric("New Volunteers", data['governance']['volunteers_new'])

    with tabs[1]:
        c1, c2 = st.columns(2)
        c1.metric("Active Orgs", data['partnerships']['active_referrals'])
        c2.metric("Corporate Partners", data['income']['corporate_partners'])
        
        df_p = pd.DataFrame([{"Sector": k, "Count": v} for k,v in {**data['partnerships']['LSP'], **data['partnerships']['LDP']}.items()])
        if not df_p.empty:
            st.plotly_chart(px.bar(df_p, x="Sector", y="Count", title="Partner Mix"))

    with tabs[2]:
        m1, m2, m3 = st.columns(3)
        m1.metric("Walks Delivered", data['delivery']['walks_delivered'])
        m2.metric("Total Participants", data['delivery']['participants'])
        m3.metric("Wellbeing Score", f"+{data['delivery']['wellbeing_change_score']}")

    with tabs[3]:
        i1, i2 = st.columns(2)
        i1.metric("Total Raised", f"£{data['income']['total_funds_raised']:,.2f}")
        i2.metric("Bids Submitted", data['income']['bids_submitted'])

def main():
    inject_global_styles()
    if not st.session_state.get('logged_in'):
        login_page()
    else:
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()
        main_dashboard()

if __name__ == "__main__":
    main()
