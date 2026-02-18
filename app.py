import streamlit as st
import pandas as pd
import json
import os
import requests
import time
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

        section[data-testid="stSidebar"] label[data-testid="stMarkdownContainer"] + div [role="radiogroup"] label {
            background: linear-gradient(90deg, #ff3d7f, #ff9f1c, #7bff6b, #00f5d4, #5a4dff);
            border-radius: 999px;
            padding: 6px 10px;
            color: #ffffff !important;
            border: 1px solid rgba(255,255,255,0.18);
            margin-bottom: 6px;
        }

        section[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {
            margin-right: 6px;
        }

        section[data-testid="stSidebar"] [role="radiogroup"] label[data-selected="true"] {
            box-shadow: 0 8px 22px rgba(122, 60, 255, 0.4);
        }

        /* Ensure radio/checkbox option text is always white */
        [role="radiogroup"] label,
        [role="radiogroup"] label span,
        [data-testid="stCheckbox"] label,
        [data-testid="stCheckbox"] label span {
            color: #ffffff !important;
        }

        /* Force BaseWeb internals (used by Streamlit radio/checkbox) */
        [data-baseweb="radio"] *,
        [data-baseweb="checkbox"] *,
        [data-testid="stRadio"] *,
        [data-testid="stCheckbox"] *,
        [data-testid="stSidebar"] [data-baseweb="radio"] *,
        [data-testid="stSidebar"] [data-baseweb="checkbox"] * {
            color: #ffffff !important;
            fill: #ffffff !important;
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

        .refresh-card {
            padding: 10px 12px;
            border-radius: 14px;
            margin-top: 10px;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .refresh-green {
            background: rgba(0, 245, 212, 0.18);
            color: #7bff6b;
            border-color: rgba(123, 255, 107, 0.5);
        }
        .refresh-amber {
            background: rgba(255, 159, 28, 0.2);
            color: #ffd166;
            border-color: rgba(255, 209, 102, 0.5);
        }
        .refresh-red {
            background: rgba(255, 61, 127, 0.2);
            color: #ff9fb5;
            border-color: rgba(255, 61, 127, 0.5);
        }

        .neon-callout {
            padding: 10px 14px;
            border-radius: 14px;
            background: linear-gradient(90deg, #00f5d4, #7bff6b, #ff9f1c, #ff3d7f, #5a4dff);
            color: #0c0c12;
            font-weight: 700;
            box-shadow: 0 12px 30px rgba(90, 77, 255, 0.45);
            text-align: center;
        }

        .overlay-message {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            z-index: 10000;
            padding: 12px 18px;
            border-radius: 999px;
            background: linear-gradient(90deg, #00f5d4, #7bff6b, #ff9f1c, #ff3d7f, #5a4dff);
            color: #0c0c12;
            font-weight: 700;
            font-size: 16px;
            box-shadow: 0 12px 30px rgba(90, 77, 255, 0.45);
            animation: overlay-fade 0.6s ease forwards;
            animation-delay: 7.5s;
        }
        @keyframes overlay-fade {
            0% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
            100% { opacity: 0; transform: translate(-50%, -50%) scale(0.98); }
        }

        .confetti-container {
            position: relative;
            height: 80px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        .confetti-piece {
            position: absolute;
            width: 10px;
            height: 14px;
            opacity: 0.9;
            animation: confetti-fall 1.6s ease-out forwards;
        }
        @keyframes confetti-fall {
            0% { transform: translateY(-20px) rotate(0deg); }
            100% { transform: translateY(120px) rotate(360deg); opacity: 0; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# --- DATABASE CONNECTION (HYBRID) ---

def get_db_connection():
    """
    Attempts to connect to Supabase.
    Returns ('supabase', client) if secrets exist.
    Returns ('local', None) otherwise.
    """
    if "supabase" in st.secrets:
        try:
            url = st.secrets["supabase"]["url"]
            key = st.secrets["supabase"]["key"]
            if key and key.startswith("eyJ"):
                try:
                    payload = key.split(".")[1]
                    padding = "=" * (-len(payload) % 4)
                    payload_bytes = payload + padding
                    import base64
                    decoded = json.loads(base64.b64decode(payload_bytes).decode("utf-8"))
                    st.session_state["supabase_role"] = decoded.get("role")
                except Exception:
                    st.session_state["supabase_role"] = "unknown"
            supabase: Client = create_client(url, key)
            return 'supabase', supabase
        except Exception as e:
            st.error(f"Supabase Configuration Error: {e}")
            return 'local', None
    return 'local', None

DB_TYPE, DB_CLIENT = get_db_connection()

def get_admin_client():
    if "supabase" not in st.secrets:
        return None
    try:
        url = st.secrets["supabase"]["url"]
        key = st.secrets["supabase"]["key"]
        return create_client(url, key)
    except Exception:
        return None

# --- AUDIT LOGGING HELPER ---
def log_audit_event(action, details=None):
    """Utility to record administrative actions to the audit log."""
    if DB_TYPE == 'supabase':
        try:
            DB_CLIENT.table("audit_logs").insert({
                "user_email": st.session_state.get("email", "System"),
                "action": action,
                "details": details or {},
                "region": st.session_state.get("region", "Global")
            }).execute()
        except Exception as e:
            # We print instead of st.error to avoid UI clutter on background ops
            print(f"Audit Log Error: {e}")

def log_audit_state_change(state_key, action, details=None):
    """Logs an event only when the tracked state payload changes."""
    payload = details or {}
    marker = json.dumps(payload, sort_keys=True, default=str)
    ss_key = f"_audit_state_{state_key}"
    if st.session_state.get(ss_key) == marker:
        return
    st.session_state[ss_key] = marker
    log_audit_event(action, payload)

# --- DATA HELPERS ---
def _clean_ts(value):
    if value is None:
        return None
    s = str(value).strip()
    return s if s else None

def _to_list(value):
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(v).strip() for v in value if str(v).strip()]
    try:
        if pd.isna(value):
            return []
    except Exception:
        pass
    s = str(value).strip()
    if not s:
        return []
    parts = [p.strip() for p in s.split(",") if p.strip()]
    return parts if parts else [s]

def _sanitize(obj):
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    try:
        if pd.isna(obj):
            return None
    except Exception:
        pass
    return obj

def _coerce_money(value):
    if value is None:
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        for key in ("value", "amount", "total", "gross", "net"):
            if key in value:
                coerced = _coerce_money(value.get(key))
                if coerced != 0.0:
                    return coerced
        for nested in value.values():
            coerced = _coerce_money(nested)
            if coerced != 0.0:
                return coerced
        return 0.0
    if isinstance(value, (list, tuple, set)):
        for item in value:
            coerced = _coerce_money(item)
            if coerced != 0.0:
                return coerced
        return 0.0
    s = str(value).replace("Â£", "").replace("£", "").replace(",", "").strip()
    try:
        return float(s)
    except Exception:
        return 0.0

def _norm_key(value):
    if value is None:
        return ""
    return "".join(ch for ch in str(value).lower() if ch.isalnum())

def _get_row_value(row, *keys):
    if not row or not keys:
        return None
    try:
        if any(k in row for k in keys):
            for k in keys:
                if k in row and row.get(k) not in [None, ""]:
                    return row.get(k)
    except Exception:
        pass

    normalized = {}
    for k, v in row.items():
        nk = _norm_key(k)
        if nk and nk not in normalized:
            normalized[nk] = v

    for k in keys:
        nk = _norm_key(k)
        if nk in normalized and normalized[nk] not in [None, ""]:
            return normalized[nk]
    return None

def _read_uploaded_csv(uploaded_file):
    if uploaded_file is None:
        return []
    try:
        df = pd.read_csv(uploaded_file)
    except Exception:
        df = pd.read_csv(uploaded_file, sep="\t")
    df = df.where(pd.notnull(df), None)
    return df.to_dict(orient="records")

def import_beacon_uploads(admin_client, uploads):
    now_iso = datetime.utcnow().isoformat() + "Z"

    people_rows = []
    people_seen = {}
    for r in uploads.get("people", []):
        payload = _sanitize(dict(r))
        payload["id"] = _get_row_value(r, "Record ID", "ID", "Id")
        payload["created_at"] = _clean_ts(_get_row_value(r, "Created date", "Created", "Created at"))
        payload["type"] = _to_list(_get_row_value(r, "Type", "Person type", "Role", "Roles", "Tags", "Category"))
        payload["c_region"] = _to_list(_get_row_value(r, "Region", "Location (region)", "Location (Region)", "Location Region", "Region (region)", "Region (Region)"))
        if payload.get("id"):
            people_seen[payload["id"]] = {"id": payload["id"], "payload": payload, "created_at": payload.get("created_at"), "updated_at": now_iso}

    org_rows = []
    org_seen = {}
    for r in uploads.get("organization", []):
        payload = _sanitize(dict(r))
        payload["id"] = _get_row_value(r, "Record ID", "ID", "Id")
        payload["created_at"] = _clean_ts(_get_row_value(r, "Created date", "Created", "Created at"))
        payload["type"] = _get_row_value(r, "Type", "Organisation type", "Organization type", "Category")
        payload["c_region"] = _to_list(_get_row_value(r, "Region", "Location (region)", "Location (Region)", "Location Region", "Region (region)", "Region (Region)"))
        if payload.get("id"):
            org_seen[payload["id"]] = {"id": payload["id"], "payload": payload, "created_at": payload.get("created_at"), "updated_at": now_iso}

    event_rows = []
    event_seen = {}
    for r in uploads.get("event", []):
        payload = _sanitize(dict(r))
        payload["id"] = _get_row_value(r, "Record ID", "ID", "Id")
        payload["start_date"] = _clean_ts(_get_row_value(r, "Start date", "Start", "Date", "Event date"))
        payload["type"] = _get_row_value(r, "Type", "Event type", "Activity type", "Category")
        payload["c_region"] = _to_list(_get_row_value(r, "Location (region)", "Location (Region)", "Location Region", "Region", "Region (region)", "Region (Region)"))
        payload["number_of_attendees"] = _get_row_value(r, "Number of attendees", "Attendees", "Participants", "Total participants", "Participant count")
        if payload.get("id"):
            event_seen[payload["id"]] = {
                "id": payload["id"],
                "payload": payload,
                "start_date": payload.get("start_date"),
                "region": (payload.get("c_region") or [None])[0],
                "updated_at": now_iso
            }

    payment_rows = []
    payment_seen = {}
    for r in uploads.get("payment", []):
        payload = _sanitize(dict(r))
        payload["id"] = _get_row_value(r, "Record ID", "ID", "Id")
        payload["payment_date"] = _clean_ts(_get_row_value(r, "Payment date", "Date", "Received date"))
        payload["amount"] = _get_row_value(r, "Amount (value)", "Amount", "Value")
        if payload.get("id"):
            payment_seen[payload["id"]] = {"id": payload["id"], "payload": payload, "payment_date": payload.get("payment_date"), "updated_at": now_iso}

    grant_rows = []
    grant_seen = {}
    for r in uploads.get("grant", []):
        payload = _sanitize(dict(r))
        payload["id"] = _get_row_value(r, "Record ID", "ID", "Id")
        payload["close_date"] = _clean_ts(_get_row_value(r, "Award date", "Close date", "Decision date"))
        payload["amount"] = _get_row_value(r, "Amount granted (value)", "Amount requested (value)", "Value (value)", "Amount", "Value")
        payload["stage"] = _get_row_value(r, "Stage", "Status", "Grant stage")
        if payload.get("id"):
            grant_seen[payload["id"]] = {"id": payload["id"], "payload": payload, "close_date": payload.get("close_date"), "updated_at": now_iso}

    people_rows = list(people_seen.values())
    org_rows = list(org_seen.values())
    event_rows = list(event_seen.values())
    payment_rows = list(payment_seen.values())
    grant_rows = list(grant_seen.values())

    if people_rows:
        admin_client.table("beacon_people").upsert(people_rows, on_conflict="id").execute()
    if org_rows:
        admin_client.table("beacon_organisations").upsert(org_rows, on_conflict="id").execute()
    if event_rows:
        admin_client.table("beacon_events").upsert(event_rows, on_conflict="id").execute()
    if payment_rows:
        admin_client.table("beacon_payments").upsert(payment_rows, on_conflict="id").execute()
    if grant_rows:
        admin_client.table("beacon_grants").upsert(grant_rows, on_conflict="id").execute()

    return {
        "people": len(people_rows),
        "organisations": len(org_rows),
        "events": len(event_rows),
        "payments": len(payment_rows),
        "grants": len(grant_rows),
    }

def _get_secret_or_env(key, default=None):
    try:
        if key in st.secrets:
            return st.secrets.get(key) or default
    except Exception:
        pass
    return os.getenv(key, default)

def _build_beacon_url(base_url, account_id, endpoint):
    base = (base_url or "").strip()
    if not base:
        base = "https://api.beaconcrm.org/v1/account/{account_id}"
    if "{account_id}" in base:
        if not account_id:
            raise ValueError("Missing BEACON_ACCOUNT_ID for base URL template.")
        base = base.format(account_id=account_id)
    base = base.rstrip("/")
    if endpoint.startswith("/"):
        return f"{base}{endpoint}"
    if base.endswith("/entities"):
        return f"{base}/{endpoint}"
    return f"{base}/entities/{endpoint}"

def _extract_result_list(response_json):
    if isinstance(response_json, list):
        return response_json
    if not isinstance(response_json, dict):
        return []
    if isinstance(response_json.get("results"), list):
        return response_json.get("results") or []
    if isinstance(response_json.get("data"), list):
        return response_json.get("data") or []
    return []

def _extract_total_count(response_json):
    if not isinstance(response_json, dict):
        return None
    meta = response_json.get("meta")
    if isinstance(meta, dict):
        total = meta.get("total")
        if isinstance(total, int):
            return total
    total = response_json.get("total")
    if isinstance(total, int):
        return total
    return None

def _extract_page_progress(response_json):
    if not isinstance(response_json, dict):
        return None, None
    meta = response_json.get("meta")
    if isinstance(meta, dict):
        current_page = meta.get("current_page")
        total_pages = meta.get("total_pages")
        if isinstance(current_page, int) and isinstance(total_pages, int):
            return current_page, total_pages
    current_page = response_json.get("current_page")
    total_pages = response_json.get("total_pages")
    if isinstance(current_page, int) and isinstance(total_pages, int):
        return current_page, total_pages
    return None, None

def _extract_entity(record):
    if isinstance(record, dict) and isinstance(record.get("entity"), dict):
        return record.get("entity") or {}
    return record if isinstance(record, dict) else {}

def _extract_region_tags(record):
    candidates = []
    for key in (
        "c_region",
        "region",
        "Region",
        "location_region",
        "location",
        "Location (region)",
        "Location Region",
    ):
        if key in record and record.get(key) not in [None, ""]:
            candidates.extend(_to_list(record.get(key)))
    if isinstance(record.get("address"), list):
        for addr in record.get("address"):
            if isinstance(addr, dict):
                if addr.get("region"):
                    candidates.extend(_to_list(addr.get("region")))
                if addr.get("country"):
                    candidates.extend(_to_list(addr.get("country")))
    seen = set()
    out = []
    for item in candidates:
        s = str(item).strip()
        if s and s.lower() not in seen:
            seen.add(s.lower())
            out.append(s)
    return out

def _fetch_beacon_entities(base_url, api_key, account_id, endpoint, per_page=50, max_pages=200):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Beacon-Application": "developer_api",
    }
    all_rows = []
    page = 1
    while page <= max_pages:
        url = _build_beacon_url(base_url, account_id, endpoint)
        params = {
            "page": page,
            "per_page": per_page,
            "sort_by": "created_at",
            "sort_direction": "desc",
        }
        resp = None
        for attempt in range(4):
            resp = requests.get(url, headers=headers, params=params, timeout=45)
            if resp.status_code not in (429, 500, 502, 503, 504):
                break
            if attempt < 3:
                time.sleep(2 ** attempt)
        if resp is None:
            raise RuntimeError(f"Beacon API request failed for {endpoint}: no response")
        if resp.status_code >= 400:
            try:
                details = resp.json()
            except Exception:
                details = resp.text[:500]
            raise RuntimeError(f"Beacon API error {resp.status_code} for {endpoint}: {details}")
        payload = resp.json()
        rows = _extract_result_list(payload)
        if not rows:
            break
        all_rows.extend(rows)
        if len(rows) < per_page:
            break
        total = _extract_total_count(payload)
        if isinstance(total, int) and len(all_rows) >= total:
            break
        current_page, total_pages = _extract_page_progress(payload)
        if isinstance(current_page, int) and isinstance(total_pages, int) and current_page >= total_pages:
            break
        page += 1
    return all_rows

def run_beacon_api_smoke_test():
    beacon_key = _get_secret_or_env("BEACON_API_KEY")
    beacon_base_url = _get_secret_or_env("BEACON_BASE_URL")
    beacon_account_id = _get_secret_or_env("BEACON_ACCOUNT_ID")
    if not beacon_key:
        raise RuntimeError("Missing BEACON_API_KEY in Streamlit secrets or environment.")
    if not beacon_base_url and not beacon_account_id:
        raise RuntimeError("Set BEACON_BASE_URL (preferred) or BEACON_ACCOUNT_ID.")

    endpoint = "person"
    url = _build_beacon_url(beacon_base_url, beacon_account_id, endpoint)
    headers = {
        "Authorization": f"Bearer {beacon_key}",
        "Content-Type": "application/json",
        "Beacon-Application": "developer_api",
    }
    params = {
        "page": 1,
        "per_page": 1,
        "sort_by": "created_at",
        "sort_direction": "desc",
    }

    started = time.time()
    resp = requests.get(url, headers=headers, params=params, timeout=45)
    elapsed_ms = int((time.time() - started) * 1000)

    try:
        payload = resp.json()
    except Exception:
        payload = {}

    if resp.status_code >= 400:
        details = payload if isinstance(payload, dict) and payload else (resp.text[:500] or "No details")
        raise RuntimeError(f"Beacon smoke test failed ({resp.status_code}): {details}")

    records = _extract_result_list(payload)
    has_records_array = isinstance(records, list)

    has_data_array = isinstance(payload, dict) and isinstance(payload.get("data"), list)
    has_meta = isinstance(payload, dict) and isinstance(payload.get("meta"), dict)
    meta = payload.get("meta") if isinstance(payload, dict) else {}
    required_meta_keys = ("current_page", "per_page", "total")
    missing_meta_keys = [k for k in required_meta_keys if not isinstance(meta, dict) or k not in meta]
    docs_compliant_shape = has_data_array and has_meta and len(missing_meta_keys) == 0

    # Accept older Beacon response shapes while still surfacing docs-compliance status.
    if not has_records_array:
        raise RuntimeError(
            "Beacon smoke test response does not include a records array "
            "(expected either data[] or results[])."
        )

    current_page, total_pages = _extract_page_progress(payload)
    total = _extract_total_count(payload)
    if current_page is None:
        current_page = params["page"]
    if total is None:
        total = len(records)
    if total_pages is None:
        per_page = params["per_page"]
        total_pages = max(1, int((total + per_page - 1) / per_page)) if isinstance(total, int) else 1

    return {
        "status_code": resp.status_code,
        "response_time_ms": elapsed_ms,
        "endpoint": endpoint,
        "records_in_page": len(records),
        "meta": {
            "current_page": current_page,
            "per_page": meta.get("per_page") if isinstance(meta, dict) else params["per_page"],
            "total": total,
            "total_pages": total_pages,
        },
        "checks": {
            "has_records_array": has_records_array,
            "has_data_array": has_data_array,
            "has_meta": has_meta,
            "required_meta_present": len(missing_meta_keys) == 0,
            "docs_compliant_shape": docs_compliant_shape,
            "legacy_compatible_shape": has_records_array and not docs_compliant_shape,
        },
    }

def sync_beacon_api_to_supabase(admin_client, progress_callback=None):
    def _status_text(progress, message):
        return f"{int(progress)}% | {message}"

    def _report(progress, message):
        if progress_callback:
            progress_callback(progress, _status_text(progress, message))

    total_started = time.time()
    now_iso = datetime.utcnow().isoformat() + "Z"
    beacon_key = _get_secret_or_env("BEACON_API_KEY")
    beacon_base_url = _get_secret_or_env("BEACON_BASE_URL")
    beacon_account_id = _get_secret_or_env("BEACON_ACCOUNT_ID")
    if not beacon_key:
        raise RuntimeError("Missing BEACON_API_KEY in Streamlit secrets or environment.")

    fetch_plan = [
        ("people", "person", "people"),
        ("organisations", "organization", "organisations"),
        ("events", "event", "events"),
        ("payments", "payment", "payments"),
        ("subscriptions", "subscription", "subscriptions"),
        ("grants", "grant", "grants"),
    ]
    datasets = {}
    fetch_breakdown_ms = {}
    fetch_started = time.time()
    _report(5, "Starting Beacon API sync...")
    for idx, (dataset_key, endpoint, label) in enumerate(fetch_plan):
        fetch_start = 5 + int((idx / len(fetch_plan)) * 45)
        fetch_end = 5 + int(((idx + 1) / len(fetch_plan)) * 45)
        _report(fetch_start, f"Fetching Beacon {label} ({idx + 1} of {len(fetch_plan)} datasets)...")
        endpoint_started = time.time()
        datasets[dataset_key] = _fetch_beacon_entities(
            beacon_base_url, beacon_key, beacon_account_id, endpoint
        )
        fetch_breakdown_ms[dataset_key] = int((time.time() - endpoint_started) * 1000)
        _report(fetch_end, f"Fetched Beacon {label}: {len(datasets[dataset_key])} records.")
    fetch_duration_ms = int((time.time() - fetch_started) * 1000)

    _report(55, "Transforming Beacon records...")
    transform_started = time.time()

    people_seen = {}
    for row in datasets["people"]:
        entity = _sanitize(_extract_entity(row))
        rec_id = entity.get("id")
        if not rec_id:
            continue
        entity["id"] = rec_id
        entity["created_at"] = _clean_ts(entity.get("created_at"))
        entity["type"] = _to_list(entity.get("type"))
        if not entity.get("c_region"):
            entity["c_region"] = _extract_region_tags(entity)
        people_seen[rec_id] = {"id": rec_id, "payload": entity, "created_at": entity.get("created_at"), "updated_at": now_iso}

    org_seen = {}
    for row in datasets["organisations"]:
        entity = _sanitize(_extract_entity(row))
        rec_id = entity.get("id")
        if not rec_id:
            continue
        entity["id"] = rec_id
        entity["created_at"] = _clean_ts(entity.get("created_at"))
        if isinstance(entity.get("type"), list):
            entity["type"] = ", ".join([str(v) for v in entity.get("type") if str(v).strip()])
        if not entity.get("c_region"):
            entity["c_region"] = _extract_region_tags(entity)
        org_seen[rec_id] = {"id": rec_id, "payload": entity, "created_at": entity.get("created_at"), "updated_at": now_iso}

    event_seen = {}
    for row in datasets["events"]:
        entity = _sanitize(_extract_entity(row))
        rec_id = entity.get("id")
        if not rec_id:
            continue
        entity["id"] = rec_id
        entity["start_date"] = _clean_ts(entity.get("start_date") or entity.get("date") or entity.get("created_at"))
        if not entity.get("c_region"):
            entity["c_region"] = _extract_region_tags(entity)
        entity["type"] = entity.get("type") or entity.get("event_type") or entity.get("category")
        entity["number_of_attendees"] = entity.get("number_of_attendees") or entity.get("attendees") or entity.get("participant_count")
        event_seen[rec_id] = {
            "id": rec_id,
            "payload": entity,
            "start_date": entity.get("start_date"),
            "region": (entity.get("c_region") or [None])[0],
            "updated_at": now_iso,
        }

    payment_seen = {}
    for row in datasets["payments"] + datasets["subscriptions"]:
        entity = _sanitize(_extract_entity(row))
        rec_id = entity.get("id")
        if not rec_id:
            continue
        if rec_id in payment_seen:
            continue
        entity["id"] = rec_id
        entity["payment_date"] = _clean_ts(entity.get("payment_date") or entity.get("date") or entity.get("created_at"))
        entity["amount"] = entity.get("amount") or entity.get("value")
        payment_seen[rec_id] = {"id": rec_id, "payload": entity, "payment_date": entity.get("payment_date"), "updated_at": now_iso}

    grant_seen = {}
    for row in datasets["grants"]:
        entity = _sanitize(_extract_entity(row))
        rec_id = entity.get("id")
        if not rec_id:
            continue
        entity["id"] = rec_id
        entity["close_date"] = _clean_ts(entity.get("close_date") or entity.get("award_date") or entity.get("created_at"))
        entity["amount"] = entity.get("amount") or entity.get("amount_granted") or entity.get("value")
        entity["stage"] = entity.get("stage") or entity.get("status")
        grant_seen[rec_id] = {"id": rec_id, "payload": entity, "close_date": entity.get("close_date"), "updated_at": now_iso}

    people_rows = list(people_seen.values())
    org_rows = list(org_seen.values())
    event_rows = list(event_seen.values())
    payment_rows = list(payment_seen.values())
    grant_rows = list(grant_seen.values())
    transform_duration_ms = int((time.time() - transform_started) * 1000)

    total_records = len(people_rows) + len(org_rows) + len(event_rows) + len(payment_rows) + len(grant_rows)
    synced_records = 0

    upsert_started = time.time()
    _report(68, f"Preparing import: {synced_records} out of {total_records} records synced.")
    _report(72, f"Upserting people ({len(people_rows)}) and organisations ({len(org_rows)})...")
    if people_rows:
        admin_client.table("beacon_people").upsert(people_rows, on_conflict="id").execute()
        synced_records += len(people_rows)
        _report(76, f"People upserted: {synced_records} out of {total_records} records synced.")
    if org_rows:
        admin_client.table("beacon_organisations").upsert(org_rows, on_conflict="id").execute()
        synced_records += len(org_rows)
        _report(80, f"Organisations upserted: {synced_records} out of {total_records} records synced.")

    _report(84, f"Upserting events ({len(event_rows)}) and payments ({len(payment_rows)})...")
    if event_rows:
        admin_client.table("beacon_events").upsert(event_rows, on_conflict="id").execute()
        synced_records += len(event_rows)
        _report(88, f"Events upserted: {synced_records} out of {total_records} records synced.")
    if payment_rows:
        admin_client.table("beacon_payments").upsert(payment_rows, on_conflict="id").execute()
        synced_records += len(payment_rows)
        _report(92, f"Payments upserted: {synced_records} out of {total_records} records synced.")

    _report(94, f"Upserting grants ({len(grant_rows)})...")
    if grant_rows:
        admin_client.table("beacon_grants").upsert(grant_rows, on_conflict="id").execute()
        synced_records += len(grant_rows)
        _report(97, f"Grants upserted: {synced_records} out of {total_records} records synced.")
    upsert_duration_ms = int((time.time() - upsert_started) * 1000)

    _report(100, f"Beacon API sync complete. {synced_records} out of {total_records} records synced.")
    total_duration_ms = int((time.time() - total_started) * 1000)

    return {
        "people": len(people_rows),
        "organisations": len(org_rows),
        "events": len(event_rows),
        "payments": len(payment_rows),
        "grants": len(grant_rows),
        "synced_at": now_iso,
        "fetch_duration_ms": fetch_duration_ms,
        "transform_duration_ms": transform_duration_ms,
        "upsert_duration_ms": upsert_duration_ms,
        "total_duration_ms": total_duration_ms,
        "fetch_breakdown_ms": fetch_breakdown_ms,
    }

# --- LOCAL FILE HELPERS (Fallback) ---

def load_local_json(filepath, default_content):
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            json.dump(default_content, f, indent=4)
        return default_content
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default_content

def save_local_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def init_files():
    # 1. LOCAL INITIALIZATION
    if DB_TYPE == 'local':
        if not os.path.exists(CASE_STUDIES_FILE):
            save_local_json(CASE_STUDIES_FILE, [])
        if not os.path.exists(USER_DB_FILE):
            default_db = {
                "users": [
                    {
                        "name": "Scott Harvey-Whittle",
                        "email": "scott.harvey-whittle@mindovermountains.org.uk",
                        "password": "ArthurMillwood01!", 
                        "role": "Admin",
                        "region": "Global"
                    }
                ]
            }
            save_local_json(USER_DB_FILE, default_db)
            
    # 2. SUPABASE INITIALIZATION
    elif DB_TYPE == 'supabase':
        # No-op: auth users are managed in Supabase Auth.
        # Roles/regions are stored in public tables.
        pass

# --- AUTHENTICATION LOGIC ---

def verify_user(email, password):
    email = email.strip().lower()
    password = password.strip()

    if not email or not password:
        return "missing_fields", None, None, None, None
    
    # A. SUPABASE STRATEGY
    if DB_TYPE == 'supabase':
        try:
            auth_resp = DB_CLIENT.auth.sign_in_with_password({"email": email, "password": password})
            if not auth_resp or not auth_resp.user:
                return "user_not_found", None, None, None, None
            user_id = auth_resp.user.id

            role_resp = DB_CLIENT.table('user_roles') \
                .select("region, name, must_change_password, roles(name)") \
                .eq("user_id", user_id) \
                .execute()
            if not role_resp.data:
                return "user_not_found", None, None, None, None
            role_row = role_resp.data[0]
            role_name = (role_row.get("roles") or {}).get("name")
            region = role_row.get("region", "Global")
            display_name = role_row.get("name") or auth_resp.user.email
            must_change = bool(role_row.get("must_change_password", False))
            return "success", role_name, region, display_name, must_change
        except Exception as e:
            msg = str(e)
            if "Invalid login credentials" in msg:
                return "wrong_password", None, None, None, None
            st.error(f"Database Error: {e}")
            return "error", None, None, None, None

    # B. LOCAL STRATEGY
    else:
        db_data = load_local_json(USER_DB_FILE, {"users": []})
        users_list = db_data.get("users", [])
        
        for i, user in enumerate(users_list):
            if str(user.get('email', '')).strip().lower() == email:
                stored_pw = str(user.get('password', '')).strip()
                
                # Self-healing plain text check
                if not stored_pw.startswith('$pbkdf2-sha256'):
                    if stored_pw == password:
                        new_hash = pbkdf2_sha256.hash(stored_pw)
                        users_list[i]['password'] = new_hash
                        db_data["users"] = users_list
                        save_local_json(USER_DB_FILE, db_data)
                        return "success", user.get('role'), user.get('region', 'Global'), user.get('name', email), False
                    return "wrong_password", None, None, None, None
                
                try:
                    if pbkdf2_sha256.verify(password, stored_pw):
                        return "success", user.get('role'), user.get('region', 'Global'), user.get('name', email), False
                except ValueError:
                    pass
                return "wrong_password", None, None, None, None
                
        return "user_not_found", None, None, None, None

def create_user(name, email, password, role, region):
    email = email.strip().lower()
    hashed_pw = pbkdf2_sha256.hash(password)
    
    if DB_TYPE == 'supabase':
        try:
            admin_client = get_admin_client()
            if not admin_client:
                st.error("Admin client not available. Check Supabase secrets.")
                return False
            # Create auth user (requires service role key)
            user_resp = admin_client.auth.admin.create_user({
                "email": email,
                "password": password,
                "email_confirm": True
            })
            user_id = user_resp.user.id

            # Look up role id
            role_resp = admin_client.table("roles").select("id").eq("name", role).execute()
            if not role_resp.data:
                return False
            role_id = role_resp.data[0]["id"]

            # Insert role mapping
            admin_client.table('user_roles').insert({
                "user_id": user_id,
                "role_id": role_id,
                "region": region,
                "email": email,
                "name": name,
                "must_change_password": True
            }).execute()

            # --- AUDIT LOG ---
            log_audit_event("User Created", {"target_email": email, "role": role, "region": region})
            
            return True
        except Exception as e:
            st.error(f"Error creating user: {e}")
            return False
    else:
        db_data = load_local_json(USER_DB_FILE, {"users": []})
        users_list = db_data.get("users", [])
        for user in users_list:
            if user.get('email', '').strip().lower() == email:
                return False
        
        users_list.append({
            "name": name, 
            "email": email, 
            "password": hashed_pw, 
            "role": role, 
            "region": region
        })
        db_data["users"] = users_list
        save_local_json(USER_DB_FILE, db_data)
        return True

def update_user_role(email, new_role, audit_reason=None, audit_confirmed=False):
    email = email.strip().lower()
    if DB_TYPE == 'supabase':
        admin_client = get_admin_client()
        if not admin_client:
            return
        role_resp = admin_client.table("roles").select("id").eq("name", new_role).execute()
        if not role_resp.data:
            return
        role_id = role_resp.data[0]["id"]
        admin_client.table('user_roles').update({"role_id": role_id}).eq('email', email).execute()
        
        # --- AUDIT LOG ---
        details = {"target_email": email, "new_role": new_role}
        if audit_reason:
            details["reason"] = audit_reason
        details["confirmed"] = bool(audit_confirmed)
        log_audit_event("Role Updated", details)
        
    else:
        db_data = load_local_json(USER_DB_FILE, {"users": []})
        users_list = db_data.get("users", [])
        for user in users_list:
            if user.get('email', '').strip().lower() == email:
                user['role'] = new_role
                save_local_json(USER_DB_FILE, db_data)
                return

def delete_user(email, audit_reason=None, audit_confirmed=False):
    email = email.strip().lower()
    if DB_TYPE == 'supabase':
        admin_client = get_admin_client()
        if not admin_client:
            return
        # Remove mapping and auth user
        role_resp = admin_client.table('user_roles').select("user_id").eq('email', email).execute()
        if role_resp.data:
            user_id = role_resp.data[0]["user_id"]
            admin_client.table('user_roles').delete().eq('email', email).execute()
            admin_client.auth.admin.delete_user(user_id)
            
            # --- AUDIT LOG ---
            details = {"target_email": email}
            if audit_reason:
                details["reason"] = audit_reason
            details["confirmed"] = bool(audit_confirmed)
            log_audit_event("User Deleted", details)
            
    else:
        db_data = load_local_json(USER_DB_FILE, {"users": []})
        users_list = db_data.get("users", [])
        new_list = [u for u in users_list if u.get('email', '').strip().lower() != email]
        if len(new_list) < len(users_list):
            db_data["users"] = new_list
            save_local_json(USER_DB_FILE, db_data)

def reset_password(email, new_password):
    email = email.strip().lower()
    new_hash = pbkdf2_sha256.hash(new_password)
    
    if DB_TYPE == 'supabase':
        admin_client = get_admin_client()
        if not admin_client:
            return
        role_resp = admin_client.table('user_roles').select("user_id").eq('email', email).execute()
        if role_resp.data:
            user_id = role_resp.data[0]["user_id"]
            admin_client.auth.admin.update_user_by_id(user_id, {"password": new_password})
            
            # --- AUDIT LOG ---
            log_audit_event("Password Reset", {"target_email": email})

    else:
        db_data = load_local_json(USER_DB_FILE, {"users": []})
        users_list = db_data.get("users", [])
        for user in users_list:
            if user.get('email', '').strip().lower() == email:
                user['password'] = new_hash
                save_local_json(USER_DB_FILE, db_data)
                return

def get_all_users():
    if DB_TYPE == 'supabase':
        try:
            response = DB_CLIENT.table('user_roles').select("name, email, region, roles(name)").execute()
            rows = []
            for r in response.data or []:
                rows.append({
                    "name": r.get("name"),
                    "email": r.get("email"),
                    "role": (r.get("roles") or {}).get("name"),
                    "region": r.get("region")
                })
            return rows
        except:
            return []
    else:
        db_data = load_local_json(USER_DB_FILE, {"users": []})
        # Return simplified list without passwords
        return [{k: v for k, v in u.items() if k != 'password'} for u in db_data.get("users", [])]

# --- CASE STUDIES (CRUD) ---

def add_case_study(title, content, region, study_date=None):
    if study_date is None:
        dt = datetime.now()
    elif isinstance(study_date, datetime):
        dt = study_date
    else:
        dt = datetime.combine(study_date, datetime.min.time())
    date_added = dt.strftime("%Y-%m-%d %H:%M:%S")
    if DB_TYPE == 'supabase':
        DB_CLIENT.table('case_studies').insert({
            "title": title,
            "content": content,
            "region": region,
            "date_added": date_added
        }).execute()
    else:
        studies = load_local_json(CASE_STUDIES_FILE, [])
        studies.append({
            "title": title,
            "content": content,
            "region": region,
            "date_added": date_added
        })
        save_local_json(CASE_STUDIES_FILE, studies)

def get_case_studies(region_filter=None, start_date=None, end_date=None):
    if DB_TYPE == 'supabase':
        try:
            query = DB_CLIENT.table('case_studies').select("*")
            # If region is global (admin view), we might fetch all, but usually we filter by dash region
            # If the user's view region is not Global, we filter
            if region_filter and region_filter != "Global":
                query = query.eq('region', region_filter)
            if start_date:
                query = query.gte('date_added', start_date.strftime("%Y-%m-%d %H:%M:%S"))
            if end_date:
                query = query.lte('date_added', end_date.strftime("%Y-%m-%d %H:%M:%S"))
            
            response = query.execute()
            return response.data
        except:
            return []
    else:
        all_studies = load_local_json(CASE_STUDIES_FILE, [])
        if region_filter and region_filter != "Global":
            all_studies = [s for s in all_studies if s.get('region') == region_filter]
        if start_date or end_date:
            def _in_range(s):
                try:
                    dt = datetime.strptime(s.get('date_added', ''), "%Y-%m-%d %H:%M:%S")
                except Exception:
                    return False
                if start_date and dt < start_date:
                    return False
                if end_date and dt > end_date:
                    return False
                return True
            all_studies = [s for s in all_studies if _in_range(s)]
        return all_studies

# --- BEACON CRM INTEGRATION (LIVE) ---

@st.cache_data(show_spinner=False, ttl=300)
def compute_kpis(region, people, organisations, events, payments, grants):
    # 2. Filter Helpers
    def get_region_tags(record):
        return _to_list(record.get('c_region'))

    def is_in_region(record):
        if region == "Global":
            return True
        tags = get_region_tags(record)
        if not tags and record.get("region"):
            tags = _to_list(record.get("region"))
        return any(region.lower() in str(t).lower() for t in tags)

    # 3. Process People (Governance)
    region_people = [p for p in people if is_in_region(p)]
    
    # Fuzzy match for volunteers
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
            
    # Proxy: If no specific "steering" tag found, fallback to total or mock logic
    steering_group_proxy = len(steering_volunteers) if steering_volunteers else len(volunteers)

    # 4. Process Organisations (Partnerships)
    region_orgs = [o for o in organisations if is_in_region(o)]
    org_id_to_region = {o.get('id'): True for o in region_orgs if o.get('id') is not None}
    
    lsp_counts = {}
    ldp_counts = {}
    corporate_count = 0
    
    for org in region_orgs:
        org_type = str(org.get('type') or "").strip()
        if not org_type:
            continue
        
        # Determine strategic vs delivery
        if any(x in org_type.lower() for x in ["university", "trust", "political", "parliamentary", "media", "nhs", "prescriber"]):
            lsp_counts[org_type] = lsp_counts.get(org_type, 0) + 1
        else:
            ldp_counts[org_type] = ldp_counts.get(org_type, 0) + 1
            
        # Specific count for corporate
        if "business" in org_type.lower() or "corporate" in org_type.lower():
            corporate_count += 1

    # 5. Process Income
    region_grants = []
    for g in grants:
        org_link = g.get('organization')
        linked_id = None
        if isinstance(org_link, dict): linked_id = org_link.get('id')
        elif isinstance(org_link, str): linked_id = org_link
        
        if linked_id and linked_id in org_id_to_region:
            region_grants.append(g)
        elif region == "Global":
            region_grants.append(g)
            
    # Fuzzy match for grant stages
    bids_submitted = sum(1 for g in region_grants if any(x in str(g.get('stage')).lower() for x in ['submitted', 'review', 'pending']))
    funds_raised_grants = sum(_coerce_money(g.get('amount')) for g in region_grants if str(g.get('stage')).lower() == 'won')
    
    def _payment_in_region(payment):
        if region == "Global":
            return True
        if is_in_region(payment):
            return True
        return False

    region_payments = [p for p in payments if _payment_in_region(p)]
    total_payments = sum(_coerce_money(p.get('amount')) for p in region_payments)
    
    total_funds = funds_raised_grants + total_payments

    # 6. Process Delivery (Events)
    region_events = [e for e in events if is_in_region(e)]

    def _to_int(value):
        if value is None:
            return 0
        s = str(value).strip().replace(",", "")
        if not s:
            return 0
        try:
            return int(float(s))
        except ValueError:
            return 0

    def _event_type(event_row):
        for key in ("type", "Type", "Event type", "Activity type", "Category"):
            val = event_row.get(key)
            if val is not None and str(val).strip():
                return str(val).lower()
        return ""

    def _event_attendees(event_row):
        for key in (
            "number_of_attendees",
            "Number of attendees",
            "Attendees",
            "Participants",
            "Total participants",
            "Participant count",
            "Number attending",
        ):
            val = event_row.get(key)
            if val is not None and str(val).strip():
                return _to_int(val)
        return 0
    
    walks_delivered = 0
    participants = 0
    delivery_event_count = 0
    for e in region_events:
        e_type = _event_type(e)
        if any(x in e_type for x in ['walk', 'retreat', 'delivery', 'session', 'hike', 'trek']):
            walks_delivered += 1
            delivery_event_count += 1
            participants += _event_attendees(e)

    # Fallback: if event labels are inconsistent, treat all region events as delivered.
    if walks_delivered == 0 and region_events:
        walks_delivered = len(region_events)
        participants = sum(_event_attendees(e) for e in region_events)

    return {
        "region": region,
        "last_updated": datetime.now().strftime("%H:%M:%S"),
        "governance": {
            "steering_group_active": steering_group_proxy > 0, 
            "steering_members": steering_group_proxy,
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
            "wellbeing_change_score": 0,
            "demographics": {"General": participants if participants > 0 else 1} 
        },
        "income": {
            "bids_submitted": bids_submitted,
            "total_funds_raised": total_funds,
            "corporate_partners": corporate_count,
            "in_kind_value": 0 
        },
        "comms": {
            "press_releases": 0,
            "media_coverage": 0,
            "newsletters_sent": 0,
            "open_rate": 0
        },
        "_debug": {
            "region_people": len(region_people),
            "volunteers": len(volunteers),
            "steering_volunteers": len(steering_volunteers),
            "region_events": len(region_events),
            "walk_events": walks_delivered,
            "participants": participants,
            "region_grants": len(region_grants),
            "bids_submitted": bids_submitted,
            "delivery_events_tagged": delivery_event_count
        },
        "_raw_income": {
            "payments": region_payments,
            "grants": region_grants
        }
    }


def get_mock_data(region):
    return {
        "region": region,
        "last_updated": datetime.now().strftime("%H:%M:%S"),
        "governance": {
            "steering_group_active": True, 
            "steering_members": 8,
            "volunteers_new": 12
        },
        "partnerships": {
            "LSP": {"Charity": 5, "Health": 3, "Social Prescribing": 2, "Corporate": 1, "University": 1, "Statutory": 4},
            "LDP": {"Charity": 10, "Health": 6, "Social Prescribing": 8, "Corporate": 2, "University": 0, "Statutory": 2},
            "active_referrals": 15,
            "networks_sat_on": 4
        },
        "delivery": {
            "walks_delivered": 45,
            "participants": 320,
            "bursary_participants": 15,
            "wellbeing_change_score": 1.4,
            "demographics": {"Men": 20, "Young Adults": 30, "Carers": 15, "Ethnic Minorities": 10, "General": 25}
        },
        "income": {
            "bids_submitted": 5,
            "total_funds_raised": 25000,
            "corporate_partners": 2,
            "in_kind_value": 5000
        },
        "comms": {
            "press_releases": 3,
            "media_coverage": 5,
            "newsletters_sent": 12,
            "open_rate": 42.5
        }
    }

def fetch_supabase_data(region, start_date=None, end_date=None):
    if DB_TYPE != 'supabase':
        return None

    def _apply_date_filter(query, field):
        if start_date:
            query = query.gte(field, start_date.isoformat())
        if end_date:
            query = query.lte(field, end_date.isoformat())
        return query

    def _fetch_all_rows(table, columns, date_field=None, batch_size=1000):
        rows = []
        offset = 0
        while True:
            q = DB_CLIENT.table(table).select(columns)
            if date_field:
                q = _apply_date_filter(q, date_field)
            chunk = q.range(offset, offset + batch_size - 1).execute().data or []
            rows.extend(chunk)
            if len(chunk) < batch_size:
                break
            offset += batch_size
        return rows

    try:
        people_rows = _fetch_all_rows("beacon_people", "payload, created_at", "created_at")
        org_rows = _fetch_all_rows("beacon_organisations", "payload, created_at", "created_at")
        # For events, we need the region column as well to ensure robust mapping.
        event_rows = _fetch_all_rows("beacon_events", "payload, start_date, region", "start_date")
        payment_rows = _fetch_all_rows("beacon_payments", "payload, payment_date", "payment_date")
        grant_rows = _fetch_all_rows("beacon_grants", "payload, close_date", "close_date")
    except Exception as e:
        st.error(f"Supabase Data Error: {e}")
        return None

    people = []
    for r in people_rows:
        payload = r.get("payload") or {}
        if r.get("created_at") and not payload.get("created_at"):
            payload["created_at"] = r.get("created_at")
        people.append(payload)

    organisations = []
    for r in org_rows:
        payload = r.get("payload") or {}
        if r.get("created_at") and not payload.get("created_at"):
            payload["created_at"] = r.get("created_at")
        organisations.append(payload)

    events = []
    for r in event_rows:
        payload = r.get("payload") or {}
        if r.get("start_date") and not payload.get("start_date"):
            payload["start_date"] = r.get("start_date")
        
        # Ensure c_region is populated
        if r.get("region") and not payload.get("c_region"):
            payload["c_region"] = [r.get("region")]
            
        events.append(payload)

    payments = []
    for r in payment_rows:
        payload = r.get("payload") or {}
        if r.get("payment_date") and not payload.get("payment_date"):
            payload["payment_date"] = r.get("payment_date")
        payments.append(payload)

    grants = []
    for r in grant_rows:
        payload = r.get("payload") or {}
        if r.get("close_date") and not payload.get("close_date"):
            payload["close_date"] = r.get("close_date")
        grants.append(payload)

    result = compute_kpis(region, people, organisations, events, payments, grants)
    result["_source"] = "supabase"
    return result

def get_last_refresh_timestamp():
    if DB_TYPE != 'supabase':
        return None
    try:
        tables = [
            "beacon_people",
            "beacon_organisations",
            "beacon_events",
            "beacon_payments",
            "beacon_grants",
        ]
        latest = None
        for t in tables:
            resp = DB_CLIENT.table(t).select("updated_at").order("updated_at", desc=True).limit(1).execute()
            if resp.data:
                ts = resp.data[0].get("updated_at")
                if ts:
                    # Parse ISO timestamp
                    try:
                        if ts.endswith("Z"):
                            ts = ts[:-1] + "+00:00"
                        dt = datetime.fromisoformat(ts)
                    except Exception:
                        dt = None
                    if dt and (latest is None or dt > latest):
                        latest = dt
        return latest
    except Exception:
        return None

# --- UI COMPONENTS ---

def login_page():
    st.markdown("## Login")
    st.markdown(
        "<div class='neon-callout'>Please sign in with your email address.</div>",
        unsafe_allow_html=True
    )
    
    if DB_TYPE == 'local':
        st.warning("Running in Local Mode. Add Supabase secrets to enable Cloud Database.")
        
    with st.form("login_form"):
        st.text_input("Email Address", key="login_email")
        st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Login")
    
    if st.button("Forgot password?"):
        email = st.session_state.get("login_email", "").strip().lower()
        if not email:
            st.error("Please enter your email address first.")
        else:
            if DB_TYPE == 'supabase':
                try:
                    DB_CLIENT.table("password_reset_requests").insert({
                        "email": email,
                        "status": "pending"
                    }).execute()
                    st.success("Request sent. An admin will set a temporary password.")
                except Exception as e:
                    st.error(f"Could not submit request: {e}")
            else:
                st.error("Password reset is only available in Supabase mode.")

    if submitted:
        email = st.session_state.get("login_email", "")
        password = st.session_state.get("login_password", "")
        status, role, region, name, must_change = verify_user(email, password)
        if status == "success":
            st.session_state['logged_in'] = True
            st.session_state['name'] = name
            st.session_state['email'] = email
            st.session_state['role'] = role
            st.session_state['region'] = region
            st.session_state['force_password_change'] = bool(must_change)
            st.rerun()
        elif status == "missing_fields":
            st.error("Please enter your email and password.")
        elif status == "user_not_found":
            st.error("User not found.")
        else:
            st.error("Invalid password.")

def password_change_page():
    st.markdown("## Change Password")
    st.info("Please set a new password to continue.")

    temp_password = st.text_input("Temporary Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Update Password"):
        if not temp_password or not new_password or not confirm_password:
            st.error("Please complete all fields.")
            return
        if new_password != confirm_password:
            st.error("New passwords do not match.")
            return

        email = st.session_state.get("email")
        try:
            # Verify temp password by re-auth
            auth_resp = DB_CLIENT.auth.sign_in_with_password({"email": email, "password": temp_password})
            if not auth_resp or not auth_resp.user:
                st.error("Temporary password is incorrect.")
                return
            user_id = auth_resp.user.id

            # Update auth password (requires service role key)
            admin_client = get_admin_client()
            if not admin_client:
                st.error("Admin client not available. Check Supabase secrets.")
                return
            admin_client.auth.admin.update_user_by_id(user_id, {"password": new_password})

            # Clear must_change_password flag
            admin_client.table("user_roles").update({"must_change_password": False}).eq("user_id", user_id).execute()

            st.session_state['force_password_change'] = False
            st.success("Password updated. Please continue.")
            st.rerun()
        except Exception as e:
            st.error(f"Password update failed: {e}")

def admin_dashboard():
    st.title("Admin Dashboard")
    st.caption(f"Database Mode: {DB_TYPE.upper()}")
    if st.session_state.get("supabase_role"):
        st.caption(f"Supabase key role: {st.session_state.get('supabase_role')}")

    # --- PASSWORD RESET REQUESTS ---
    with st.expander("Password Reset Requests", expanded=False):
        if DB_TYPE == 'supabase':
            try:
                admin_client = get_admin_client()
                if not admin_client:
                    st.error("Admin client not available. Check Supabase secrets.")
                    reqs = []
                else:
                    reqs = admin_client.table("password_reset_requests") \
                    .select("id, email, status, created_at") \
                    .eq("status", "pending") \
                    .order("created_at", desc=True) \
                    .execute().data or []
            except Exception as e:
                reqs = []
                st.error(f"Could not load requests: {e}")
            if reqs:
                req_emails = [r["email"] for r in reqs]
                selected_email = st.selectbox("Pending requests", req_emails)
                temp_pw = st.text_input("Temporary Password", type="password", key="reset_temp_pw")
                if st.button("Set Temporary Password"):
                    if not temp_pw:
                        st.error("Please enter a temporary password.")
                    else:
                        try:
                            user_row = admin_client.table("user_roles").select("user_id").eq("email", selected_email).execute()
                            if not user_row.data:
                                st.error("User not found for that email.")
                            else:
                                user_id = user_row.data[0]["user_id"]
                                admin_client.auth.admin.update_user_by_id(user_id, {"password": temp_pw})
                                admin_client.table("user_roles").update({"must_change_password": True}).eq("user_id", user_id).execute()
                                admin_client.table("password_reset_requests").update({"status": "completed"}).eq("email", selected_email).execute()
                                st.success("Temporary password set. User will be prompted to change it on next login.")
                        except Exception as e:
                            st.error(f"Failed to reset password: {e}")
            else:
                st.info("No pending requests.")
        else:
            st.info("Password reset requests are available only in Supabase mode.")

    # --- USER MANAGEMENT ---
    with st.expander("Create New User", expanded=False):
        c1, c2 = st.columns(2)
        new_name = c1.text_input("Full Name")
        new_email = c2.text_input("Email")
        c3, c4 = st.columns(2)
        new_pw = c3.text_input("Password", type="password")
        new_role = c4.selectbox("Role", ["RPL", "Manager", "Admin"])
        new_region = st.text_input("Region (e.g., North West)")
        
        if st.button("Create User"):
            if new_email and new_pw:
                if create_user(new_name, new_email, new_pw, new_role, new_region):
                    st.success(f"User {new_email} created!")
                    st.rerun()
                else:
                    st.error("User with this email already exists.")
            else:
                st.error("Please fill in email and password.")

    # List Users
    users_data = get_all_users()
    if users_data:
        df_users = pd.DataFrame(users_data)
        with st.expander("Existing Users & Actions", expanded=False):
            st.dataframe(df_users, use_container_width=True)
            
            if not df_users.empty:
                user_emails = df_users['email'].tolist()
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.subheader("Reset Password")
                    target_email = st.selectbox("Select User", user_emails, key="reset_sel")
                    reset_pw = st.text_input("New Password", type="password", key="reset_pw")
                    if st.button("Reset Password"):
                        reset_password(target_email, reset_pw)
                        st.success(f"Password updated.")
                
                with col2:
                    st.subheader("Update Role")
                    target_role_email = st.selectbox("Select User", user_emails, key="role_sel")
                    new_role_update = st.selectbox("New Role", ["RPL", "Manager", "Admin"], key="role_up")
                    role_reason = st.text_input("Reason for role change", key="role_reason")
                    role_confirm = st.checkbox("I confirm this role change", key="role_confirm")
                    if st.button("Update Role"):
                        if not role_reason.strip():
                            st.error("Please provide a reason for the role update.")
                        elif not role_confirm:
                            st.error("Please confirm the role update.")
                        else:
                            update_user_role(
                                target_role_email,
                                new_role_update,
                                audit_reason=role_reason.strip(),
                                audit_confirmed=True,
                            )
                            st.success("Role updated.")
                            st.rerun()

                with col3:
                    st.subheader("Delete User")
                    target_del = st.selectbox("Select User", user_emails, key="del_sel")
                    delete_reason = st.text_input("Reason for deletion", key="delete_reason")
                    delete_confirm = st.checkbox("I confirm this user deletion", key="delete_confirm")
                    if st.button("Delete User", type="primary"):
                        if not delete_reason.strip():
                            st.error("Please provide a reason for deletion.")
                        elif not delete_confirm:
                            st.error("Please confirm user deletion.")
                        else:
                            delete_user(
                                target_del,
                                audit_reason=delete_reason.strip(),
                                audit_confirmed=True,
                            )
                            st.success("User deleted.")
                            st.rerun()

    # --- SYSTEM ACTIONS ---
    st.markdown("---")
    st.subheader("System Actions")
    with st.expander("Sync Performance", expanded=False):
        if DB_TYPE == 'supabase':
            try:
                perf_resp = (
                    DB_CLIENT.table("audit_logs")
                    .select("created_at, action, details")
                    .in_("action", ["Data Sync Completed", "Data Sync Failed"])
                    .order("created_at", desc=True)
                    .limit(100)
                    .execute()
                )
                perf_rows = perf_resp.data or []
            except Exception:
                perf_rows = []

            completed = []
            for row in perf_rows:
                if row.get("action") != "Data Sync Completed":
                    continue
                details = row.get("details") or {}
                if details.get("source") != "beacon_api":
                    continue
                completed.append({
                    "created_at": row.get("created_at"),
                    "details": details,
                })

            if completed:
                latest = completed[0]
                latest_details = latest.get("details") or {}
                c_perf1, c_perf2, c_perf3, c_perf4 = st.columns(4)
                c_perf1.metric("Last Total", f"{latest_details.get('total_duration_ms', 0) / 1000:.1f}s")
                c_perf2.metric("Fetch", f"{latest_details.get('fetch_duration_ms', 0) / 1000:.1f}s")
                c_perf3.metric("Transform", f"{latest_details.get('transform_duration_ms', 0) / 1000:.1f}s")
                c_perf4.metric("Upsert", f"{latest_details.get('upsert_duration_ms', 0) / 1000:.1f}s")

                recent = completed[:10]
                if recent:
                    avg_total = sum(int((x.get("details") or {}).get("total_duration_ms") or 0) for x in recent) / len(recent)
                    st.caption(f"Average total duration (last {len(recent)} successful syncs): {avg_total / 1000:.1f}s")

                last_sync_raw = latest.get("created_at") or latest_details.get("synced_at")
                last_sync_ts = pd.to_datetime(last_sync_raw, utc=True, errors="coerce")
                if pd.isna(last_sync_ts):
                    last_sync_label = "Unknown"
                else:
                    last_sync_label = last_sync_ts.strftime("%d/%m/%Y %H:%M UTC")
                sync_type = "Automatic" if (latest_details.get("trigger") == "github_actions") else "Manual"
                st.caption(f"Last successful sync: {last_sync_label} | Type: {sync_type}")
            else:
                st.info("No completed Beacon sync performance records found yet.")
        else:
            st.info("Sync performance is available only in Supabase mode.")

    st.subheader("Beacon API Sync")
    if DB_TYPE == 'supabase':
        admin_client = get_admin_client()
        if admin_client:
            col_smoke, col_sync = st.columns(2)
            if col_smoke.button("Run Beacon API Smoke Test"):
                try:
                    log_audit_event("Beacon Smoke Test Started", {"source": "beacon_api"})
                    smoke_result = run_beacon_api_smoke_test()
                    log_audit_event("Beacon Smoke Test Completed", {"source": "beacon_api", **smoke_result})
                    if smoke_result.get("checks", {}).get("docs_compliant_shape"):
                        st.success(
                            f"Smoke test passed ({smoke_result['status_code']}) in "
                            f"{smoke_result['response_time_ms']} ms."
                        )
                    else:
                        st.warning(
                            f"Smoke test passed with legacy response shape "
                            f"({smoke_result['status_code']}) in {smoke_result['response_time_ms']} ms."
                        )
                    st.json(smoke_result)
                except Exception as e:
                    log_audit_event("Beacon Smoke Test Failed", {"source": "beacon_api", "error": str(e)})
                    st.error(f"Smoke test failed: {e}")

            if col_sync.button("Sync Beacon API to Database"):
                sync_progress = st.progress(0, text="Starting Beacon API sync...")
                try:
                    log_audit_event("Data Sync Started", {"source": "beacon_api"})

                    def _sync_ui_progress(progress, message):
                        sync_progress.progress(int(max(0, min(100, progress))), text=message)

                    result = sync_beacon_api_to_supabase(admin_client, progress_callback=_sync_ui_progress)
                    log_audit_event("Data Sync Completed", {"source": "beacon_api", **result})
                    sync_progress.progress(100, text="Beacon API sync complete.")
                    st.success(
                        "API sync complete. "
                        f"Updated: People {result.get('people', 0)}, "
                        f"Organisations {result.get('organisations', 0)}, "
                        f"Events {result.get('events', 0)}, "
                        f"Payments {result.get('payments', 0)}, "
                        f"Grants {result.get('grants', 0)}. "
                        f"Synced at: {result.get('synced_at', 'n/a')}"
                    )
                    st.cache_data.clear()
                except Exception as e:
                    sync_progress.progress(100, text="Beacon API sync failed.")
                    log_audit_event("Data Sync Failed", {"source": "beacon_api", "error": str(e)})
                    st.error(f"API sync failed: {e}")
        else:
            st.info("Admin client not available. Check Supabase secrets.")
    else:
        st.info("API sync is available only in Supabase mode.")

    st.subheader("Beacon CSV Upload")
    if DB_TYPE == 'supabase':
        admin_client = get_admin_client()
        if admin_client:
            if st.button("Upload Beacon Exports"):
                log_audit_event("CSV Upload Opened", {"source": "beacon_csv"})
                st.session_state["show_upload_dialog"] = True

            if st.session_state.get("show_upload_dialog"):
                @st.dialog("Upload Beacon Exports")
                def _upload_dialog():
                    people_file = st.file_uploader("People CSV", type=["csv"])
                    org_file = st.file_uploader("Organisation CSV", type=["csv"])
                    event_file = st.file_uploader("Event CSV", type=["csv"])
                    payment_file = st.file_uploader("Payment CSV", type=["csv"])
                    grant_file = st.file_uploader("Grant CSV", type=["csv"])

                    if st.button("Import"):
                        log_audit_event("Data Import Started", {"source": "beacon_csv"})
                        uploads = {
                            "people": _read_uploaded_csv(people_file),
                            "organization": _read_uploaded_csv(org_file),
                            "event": _read_uploaded_csv(event_file),
                            "payment": _read_uploaded_csv(payment_file),
                            "grant": _read_uploaded_csv(grant_file),
                        }
                        result = import_beacon_uploads(admin_client, uploads)
                        
                        # --- AUDIT LOG ---
                        log_audit_event("Data Imported", {"source": "beacon_csv", **result})
                        
                        st.success(f"Imported: {result}")
                        st.session_state["show_upload_dialog"] = False
                _upload_dialog()
        else:
            st.info("Admin client not available. Check Supabase secrets.")
    else:
        st.info("CSV upload is available only in Supabase mode.")
    col_sys_1, col_sys_2 = st.columns([1, 3])
    refresh_reason = col_sys_2.text_input("Reason for full refresh", key="refresh_reason")
    refresh_confirm = col_sys_2.checkbox("I confirm full dashboard cache refresh", key="refresh_confirm")
    with col_sys_1:
        if st.button("Refresh All Dashboard Data"):
            if not refresh_reason.strip():
                st.error("Please provide a reason for full refresh.")
            elif not refresh_confirm:
                st.error("Please confirm full dashboard refresh.")
            else:
                log_audit_event(
                    "Dashboard Refresh",
                    {
                        "scope": "all_cached_data",
                        "reason": refresh_reason.strip(),
                        "confirmed": True,
                    },
                )
                st.cache_data.clear()
                st.success("Cache cleared. Reloading...")
                st.rerun()

    # --- AUDIT LOG UI ---
    st.markdown("---")
    with st.expander("System Audit Log", expanded=False):
        if DB_TYPE == 'supabase':
            # 1. Build Query
            query = DB_CLIENT.table("audit_logs").select("*").order("created_at", desc=True).limit(200)

            # 2. Fetch & Display
            try:
                resp = query.execute()
                data = resp.data
                
                if data:
                    df_log = pd.DataFrame(data)

                    # Search & Filter Controls
                    col_search, col_filter = st.columns([3, 1])
                    search_term = col_search.text_input(
                        "Search Logs (User, Action, or Details)",
                        placeholder="e.g. 'Data Sync Completed' or 'scott@...'"
                    )
                    action_options = ["All"] + sorted(df_log["action"].dropna().astype(str).unique().tolist())
                    action_filter = col_filter.selectbox("Filter by Action", action_options)
                    if action_filter != "All":
                        df_log = df_log[df_log["action"] == action_filter]
                    
                    # Convert timestamps to readable format
                    df_log['created_at'] = pd.to_datetime(df_log['created_at']).dt.strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Client-side Search (for flexibility with JSON/Text columns)
                    if search_term:
                        search_term = search_term.lower()
                        mask = (
                            df_log['user_email'].str.lower().str.contains(search_term) |
                            df_log['action'].str.lower().str.contains(search_term) |
                            df_log['details'].astype(str).str.lower().str.contains(search_term)
                        )
                        df_log = df_log[mask]

                    st.dataframe(
                        df_log[['created_at', 'user_email', 'action', 'details', 'region']], 
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No logs found.")
            except Exception as e:
                st.error(f"Failed to load logs: {e}")
        else:
            st.info("Audit logging is only enabled in Supabase mode.")

def get_time_filters():
    st.sidebar.markdown("### Time Filters")
    timeframe = st.sidebar.selectbox(
        "Timeframe",
        ["All Time", "Year", "Quarter", "Month", "Week", "Custom Range"],
        index=0
    )

    today = datetime.now().date()
    start_date = None
    end_date = None

    def _month_range(year, month):
        start = datetime(year, month, 1)
        if month == 12:
            end = datetime(year + 1, 1, 1) - pd.Timedelta(days=1)
        else:
            end = datetime(year, month + 1, 1) - pd.Timedelta(days=1)
        return start, end

    if timeframe == "All Time":
        start_date = None
        end_date = None
    elif timeframe == "Year":
        year = st.sidebar.selectbox("Year", list(range(today.year, today.year - 5, -1)))
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
    elif timeframe == "Quarter":
        year = st.sidebar.selectbox("Year", list(range(today.year, today.year - 5, -1)))
        quarter = st.sidebar.selectbox("Quarter", ["Q1", "Q2", "Q3", "Q4"])
        q_start_month = {"Q1": 1, "Q2": 4, "Q3": 7, "Q4": 10}[quarter]
        start_date, end_date = _month_range(year, q_start_month)
        _, end_date = _month_range(year, q_start_month + 2)
    elif timeframe == "Month":
        year = st.sidebar.selectbox("Year", list(range(today.year, today.year - 5, -1)))
        month = st.sidebar.selectbox("Month", list(range(1, 13)))
        start_date, end_date = _month_range(year, month)
    elif timeframe == "Week":
        # Week starts on Monday
        current_week_start = today - pd.Timedelta(days=today.weekday())
        week_start = st.sidebar.date_input(
            "Week starting (Monday)",
            value=current_week_start
        )
        if week_start.weekday() != 0:
            st.sidebar.warning("Week start adjusted to Monday.")
            week_start = week_start - pd.Timedelta(days=week_start.weekday())
        week_end = week_start + pd.Timedelta(days=6)
        start_date = datetime.combine(week_start, datetime.min.time())
        end_date = datetime.combine(week_end, datetime.max.time())
        st.sidebar.caption(f"Week: {week_start} to {week_end}")
    else:
        custom_start = st.sidebar.date_input("Start date", value=today - pd.Timedelta(days=30))
        custom_end = st.sidebar.date_input("End date", value=today)
        if custom_end < custom_start:
            st.sidebar.error("End date must be on or after start date.")
        elif (custom_end - custom_start).days > 92:
            st.sidebar.error("Date range must be 3 months or less.")
        else:
            start_date = datetime.combine(custom_start, datetime.min.time())
            end_date = datetime.combine(custom_end, datetime.max.time())

    if start_date and end_date:
        st.sidebar.caption(f"Filtering: {start_date.date()} to {end_date.date()}")
    elif timeframe == "All Time":
        st.sidebar.caption("Filtering: All time")

    log_audit_state_change(
        "time_filters",
        "Dashboard Filter Changed",
        {
            "timeframe": timeframe,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        },
    )

    return timeframe, start_date, end_date


def main_dashboard():
    # Sidebar Info
    hour = datetime.now().hour
    if hour < 12:
        greeting = "Good morning"
    elif hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    st.sidebar.title(f"{greeting}, {st.session_state['name']}")
    st.sidebar.info(f"Role: {st.session_state['role']}")
    
    # --- REGION FILTER ---
    st.sidebar.markdown("### Region Filter")
    role = st.session_state.get('role')
    default_region = st.session_state.get('region') or "Global"
    if role in ["Admin", "Manager", "RPL"]:
        all_regions = st.sidebar.checkbox("All Regions", value=True)
        if all_regions:
            region_val = "Global"
        else:
            region_options = ["North of England", "South of England", "Midlands", "Wales", "Other"]
            default_index = region_options.index(default_region) if default_region in region_options else 0
            region_val = st.sidebar.selectbox("Region", region_options, index=default_index)
    else:
        region_val = default_region
    st.sidebar.caption(f"Region: {region_val}")

    timeframe, start_date, end_date = get_time_filters()
    
    
    data = fetch_supabase_data(region_val, start_date=start_date, end_date=end_date)
    if not data:
        st.error("No Supabase data found for the selected filters.")
        return

    st.title(f"Region Dashboard: {data['region']}")
    # Removed header metadata captions per request
    st.markdown('<div class="section-card"><span class="badge">Live KPI Overview</span></div>', unsafe_allow_html=True)

    show_debug = False
    if st.session_state.get("role") in ["Admin", "Manager", "RPL"]:
        show_debug = st.sidebar.checkbox("Show KPI Debug", value=False)
    if show_debug:
        debug = data.get("_debug") or {}
        st.subheader("KPI Debug Counts")
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("People in Region", debug.get("region_people", 0))
        d2.metric("Volunteers", debug.get("volunteers", 0))
        d3.metric("Steering Volunteers", debug.get("steering_volunteers", 0))
        d4.metric("Events in Region", debug.get("region_events", 0))
        e1, e2, e3, e4 = st.columns(4)
        e1.metric("Walk Events", debug.get("walk_events", 0))
        e2.metric("Participants", debug.get("participants", 0))
        e3.metric("Grants in Region", debug.get("region_grants", 0))
        e4.metric("Bids Submitted", debug.get("bids_submitted", 0))
    

    # Tabs
    tab_gov, tab_part, tab_del, tab_inc, tab_com, tab_case = st.tabs([
        "Governance", "Partnerships", "Delivery", "Income", "Comms", "Case Studies"
    ])

    # --- A. Governance ---
    with tab_gov:
        st.header("Governance & Infrastructure")
        c1, c2, c3 = st.columns(3)
        c1.metric("Steering Group Active", "Yes" if data['governance']['steering_group_active'] else "No")
        c2.metric("Active Volunteers", data['governance']['steering_members'])
        c3.metric("New Volunteers", data['governance']['volunteers_new'])

    # --- B. Partnerships ---
    with tab_part:
        st.header("Partnerships & Influence")
        data_lsp = [{"Sector": k, "Count": v, "Type": "Strategic (LSP)"} for k, v in data['partnerships']['LSP'].items()]
        data_ldp = [{"Sector": k, "Count": v, "Type": "Delivery (LDP)"} for k, v in data['partnerships']['LDP'].items()]
        
        if not data_lsp and not data_ldp:
            st.info("No Organisation data found for this region.")
        else:
            df_partners = pd.DataFrame(data_lsp + data_ldp)
            fig = px.bar(df_partners, x="Sector", y="Count", color="Type", barmode="group",
                         title="Partner Breakdown: Strategic vs Delivery")
            st.plotly_chart(fig, use_container_width=True)
        
        c1, c2 = st.columns(2)
        c1.metric("Active Orgs in Region", data['partnerships']['active_referrals'])
        c2.metric("Network Memberships", data['partnerships']['networks_sat_on'])

    # --- C. Delivery ---
    with tab_del:
        st.header("Delivery, Reach & Impact")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Walks Delivered", data['delivery']['walks_delivered'])
        m2.metric("Total Participants", data['delivery']['participants'])
        m3.metric("Bursary Participants", data['delivery']['bursary_participants'])
        m4.metric("Avg Wellbeing Change", f"+{data['delivery']['wellbeing_change_score']}")
        
        st.subheader("Demographics")
        df_demo = pd.DataFrame(list(data['delivery']['demographics'].items()), columns=['Group', 'Count'])
        fig_pie = px.pie(df_demo, values='Count', names='Group', title="Representation from Groups")
        st.plotly_chart(fig_pie)

    # --- D. Income ---
    with tab_inc:
        st.header("Income & Funding")
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Total Funds Raised", f"£{data['income']['total_funds_raised']:,.2f}")
            st.metric("In-Kind Value", f"£{data['income']['in_kind_value']:,}")
        with c2:
            st.metric("Bids Submitted", data['income']['bids_submitted'])
            st.metric("Corporate Partners", data['income']['corporate_partners'])

        st.subheader("Income Over Time")
        raw_income = (data.get("_raw_income") or {})
        payments = raw_income.get("payments") or []
        grants = raw_income.get("grants") or []

        def _to_float(val):
            return _coerce_money(val)

        rows = []
        for p in payments:
            rows.append({
                "date": p.get("payment_date"),
                "amount": _to_float(p.get("amount")),
                "source": "Payments"
            })
        for g in grants:
            rows.append({
                "date": g.get("close_date"),
                "amount": _to_float(g.get("amount")),
                "source": "Grants"
            })

        if rows:
            df_income = pd.DataFrame(rows)
            df_income["date"] = pd.to_datetime(df_income["date"], errors="coerce")
            df_income = df_income.dropna(subset=["date"])

            if not df_income.empty:
                # Choose grouping based on timeframe selection
                if timeframe == "Week":
                    freq = "D"
                    title = "Daily Income (Week)"
                elif timeframe == "Month":
                    freq = "D"
                    title = "Daily Income (Month)"
                elif timeframe == "Quarter":
                    freq = "W-MON"
                    title = "Weekly Income (Quarter)"
                elif timeframe == "Year":
                    freq = "M"
                    title = "Monthly Income (Year)"
                elif timeframe == "Custom Range" and start_date and end_date:
                    days = (end_date.date() - start_date.date()).days
                    if days <= 31:
                        freq = "D"
                        title = "Daily Income (Custom Range)"
                    else:
                        freq = "W-MON"
                        title = "Weekly Income (Custom Range)"
                else:
                    freq = "M"
                    title = "Monthly Income (All Time)"

                df_income = df_income.groupby([pd.Grouper(key="date", freq=freq), "source"], as_index=False)["amount"].sum()
                fig_income = px.line(
                    df_income,
                    x="date",
                    y="amount",
                    color="source",
                    markers=True,
                    title=title
                )
                st.plotly_chart(fig_income, use_container_width=True)
            else:
                st.info("No dated income records found for this period.")
        else:
            st.info("No income records found for this period.")

    # --- E. Comms ---
    with tab_com:
        st.header("Communications & Profile")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Press Releases", data['comms']['press_releases'])
        c2.metric("Media Coverage", data['comms']['media_coverage'])
        c3.metric("Newsletters Sent", data['comms']['newsletters_sent'])
        c4.metric("Open Rate", f"{data['comms']['open_rate']}%")

    # --- CASE STUDIES ---
    with tab_case:
        case_studies_page(
            allow_upload=False,
            start_date=start_date,
            end_date=end_date,
            region_override=region_val
        )

def case_studies_page(allow_upload=True, start_date=None, end_date=None, region_override=None):
    st.header("Case Studies & Reviews")
    if st.session_state.get("case_study_saved"):
        import random
        variants = [
            "Case study saved. Mind Over Mountains is transforming lives through the outdoors.",
            "Case study saved. Another step forward for mental health with Mind Over Mountains.",
            "Case study saved. This is the impact Mind Over Mountains makes every day.",
            "Case study saved. Proof that Mind Over Mountains is changing lives for the better.",
            "Case study saved. Real stories of hope powered by Mind Over Mountains.",
            "Case study saved. Positive change and stronger wellbeing with Mind Over Mountains.",
            "Case study saved. A reminder of the incredible work Mind Over Mountains delivers.",
        ]
        message = random.choice(variants)
        import streamlit.components.v1 as components
        fireworks_html = """
        <html>
        <body style="margin:0;background:transparent;overflow:hidden;">
          <canvas id="fw"></canvas>
          <script>
          const iframe = window.frameElement;
          if (iframe) {
            iframe.style.position = 'fixed';
            iframe.style.top = '0';
            iframe.style.left = '0';
            iframe.style.width = '100vw';
            iframe.style.height = '100vh';
            iframe.style.zIndex = '9999';
            iframe.style.pointerEvents = 'none';
            iframe.style.border = '0';
          }
          const canvas = document.getElementById('fw');
          const ctx = canvas.getContext('2d');
          function resize(){
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
          }
          resize(); window.addEventListener('resize', resize);
          const colors = ['#00f5d4','#7bff6b','#ff9f1c','#ff3d7f','#5a4dff','#ffd166'];
          const fireworks = [];
          function spawn(){
            const x = Math.random()*canvas.width*0.8 + canvas.width*0.1;
            const y = Math.random()*canvas.height*0.5 + canvas.height*0.1;
            const particles = [];
            for(let i=0;i<120;i++){
              const angle = Math.random()*Math.PI*2;
              const speed = Math.random()*7 + 2;
              particles.push({
                x,y,
                vx: Math.cos(angle)*speed,
                vy: Math.sin(angle)*speed,
                life: Math.random()*60+40,
                color: colors[(Math.random()*colors.length)|0]
              });
            }
            fireworks.push(particles);
          }
          let last = 0;
          function animate(ts){
            if(ts - last > 160){ spawn(); last = ts; }
            ctx.clearRect(0,0,canvas.width,canvas.height);
            for(let f=fireworks.length-1; f>=0; f--){
              const particles = fireworks[f];
              for(let p=particles.length-1; p>=0; p--){
                const part = particles[p];
                part.x += part.vx;
                part.y += part.vy;
                part.vy += 0.05;
                part.life -= 1;
                ctx.fillStyle = part.color;
                ctx.fillRect(part.x, part.y, 3, 3);
                if(part.life <= 0) particles.splice(p,1);
              }
              if(particles.length === 0) fireworks.splice(f,1);
            }
            requestAnimationFrame(animate);
          }
          requestAnimationFrame(animate);
          setTimeout(()=>{ if(iframe) iframe.style.display = 'none'; }, 4500);
          </script>
        </body>
        </html>
        """
        components.html(fireworks_html, height=10, scrolling=False)
        st.markdown(
            f"<div class='overlay-message'>{message}</div>",
            unsafe_allow_html=True
        )
        st.session_state["case_study_saved"] = False
    if allow_upload:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        # Add new
        with st.expander("Upload New Case Study"):
            with st.form("case_study_form"):
                cs_title = st.text_input("Title")
                cs_content = st.text_area("Story / Testimonial")
                cs_date = st.date_input("Case Study Date", value=datetime.now().date())
                cs_region = st.selectbox(
                    "Region",
                    ["North of England", "South of England", "Midlands", "Wales", "Global", "Other"]
                )
                cs_submitted = st.form_submit_button("Submit Case Study")
                
                if cs_submitted:
                    if cs_title and cs_content:
                        add_case_study(cs_title, cs_content, cs_region, cs_date)
                        st.session_state["case_study_saved"] = True
                        st.rerun()
                    else:
                        st.error("Please provide both a title and content.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Display Studies (Filtered by Region or Global Admin)
    view_region = region_override or st.session_state.get('region', 'Global')
    if st.session_state['role'] == 'Admin' and view_region == 'Global':
        display_studies = get_case_studies(None, start_date=start_date, end_date=end_date) # Get All
    else:
        display_studies = get_case_studies(view_region, start_date=start_date, end_date=end_date)

        if display_studies:
            # Sort by date added (oldest -> newest)
            display_studies.sort(key=lambda x: x.get('date_added', ''), reverse=False)
            for study in display_studies:
                with st.container():
                    st.markdown(f"#### {study['title']}")
                    st.caption(f"Date: {study.get('date_added','')} | Region: {study.get('region','')}")
                    st.info(study['content'])
        else:
            st.write("No case studies found.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN APP FLOW ---
def main():
    inject_global_styles()
    init_files()
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        login_page()
    else:
        if st.session_state.get('force_password_change'):
            password_change_page()
            return
        if st.sidebar.button("Logout", key="logout"):
            log_audit_event("Logout", {"from": "dashboard"})
            st.session_state['logged_in'] = False
            st.rerun()
        
        badge_ts = datetime.now().strftime("%Y%m%d%H%M")
        st.sidebar.markdown(
            f"[![Keep The Dashboard Awake]"
            f"(https://github.com/Scott-MoM/RPL-KPIs/actions/workflows/keep-streamlit-awake.yml/badge.svg?branch=main&t={badge_ts})"
            f"](https://github.com/Scott-MoM/RPL-KPIs/actions/workflows/keep-streamlit-awake.yml)"
        )
        st.sidebar.markdown(
            f"[![Nightly Beacon Sync]"
            f"(https://github.com/Scott-MoM/RPL-KPIs/actions/workflows/nightly-beacon-sync.yml/badge.svg?branch=main&t={badge_ts})"
            f"](https://github.com/Scott-MoM/RPL-KPIs/actions/workflows/nightly-beacon-sync.yml)"
        )

        # Last Data Refresh card
        last_refresh = get_last_refresh_timestamp()
        if last_refresh:
            hours = (datetime.now(last_refresh.tzinfo) - last_refresh).total_seconds() / 3600.0
            if hours <= 24:
                cls = "refresh-green"
            elif hours <= 72:
                cls = "refresh-amber"
            else:
                cls = "refresh-red"
            ts_str = last_refresh.strftime("%d/%m/%Y %H:%M")
            extra = ""
            if hours > 72:
                extra = "<br><strong>Data refresh needed</strong>"
            st.sidebar.markdown(
                f"<div class='refresh-card {cls}'>Last Data Refresh: {ts_str}{extra}</div>",
                unsafe_allow_html=True
            )
        else:
            st.sidebar.markdown(
                "<div class='refresh-card refresh-red'>Last Data Refresh: Unknown<br><strong>Data refresh needed</strong></div>",
                unsafe_allow_html=True
            )
            
        role = st.session_state.get('role')
        if role == 'Admin':
            view = st.sidebar.radio("View Mode", ["Admin Dashboard", "KPI Dashboard", "Case Studies"])
            log_audit_state_change("view_mode", "Dashboard View Changed", {"view": view, "role": role})
            if view == "Admin Dashboard":
                admin_dashboard()
            elif view == "KPI Dashboard":
                main_dashboard()
            else:
                timeframe, start_date, end_date = get_time_filters()
                case_studies_page(allow_upload=True, start_date=start_date, end_date=end_date)
        elif role == 'Manager':
            view = st.sidebar.radio("View Mode", ["KPI Dashboard", "Case Studies"])
            log_audit_state_change("view_mode", "Dashboard View Changed", {"view": view, "role": role})
            if view == "KPI Dashboard":
                main_dashboard()
            else:
                timeframe, start_date, end_date = get_time_filters()
                case_studies_page(allow_upload=True, start_date=start_date, end_date=end_date)
        else:
            view = st.sidebar.radio("View Mode", ["KPI Dashboard", "Case Studies"])
            log_audit_state_change("view_mode", "Dashboard View Changed", {"view": view, "role": role})
            if view == "KPI Dashboard":
                main_dashboard()
            else:
                timeframe, start_date, end_date = get_time_filters()
                case_studies_page(allow_upload=True, start_date=start_date, end_date=end_date)

if __name__ == "__main__":
    main()


