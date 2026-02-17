import os
import json
import requests
import time
from datetime import datetime

try:
    import tomllib  # py3.11+
except Exception:  # pragma: no cover
    tomllib = None

from supabase import create_client

BEACON_BASE_URL = "https://api.beaconcrm.org/v1/account/{account_id}"


def load_secrets():
    secrets = {}
    secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
    if os.path.exists(secrets_path) and tomllib:
        with open(secrets_path, "rb") as f:
            secrets = tomllib.load(f)
    return secrets


def get_env_or_secret(secrets, key):
    return os.getenv(key) or secrets.get(key)


def build_beacon_url(endpoint, account_id, base_url=None):
    base = (base_url or BEACON_BASE_URL).strip()
    if "{account_id}" in base:
        if not account_id:
            raise SystemExit("Missing BEACON_ACCOUNT_ID for base URL template.")
        base = base.format(account_id=account_id)
    base = base.rstrip("/")
    if endpoint.startswith("/"):
        return f"{base}{endpoint}"
    if base.endswith("/entities"):
        return f"{base}/{endpoint}"
    return f"{base}/entities/{endpoint}"


def extract_results(payload):
    if isinstance(payload, dict):
        if isinstance(payload.get("results"), list):
            return payload.get("results") or []
        if isinstance(payload.get("data"), list):
            return payload.get("data") or []
    if isinstance(payload, list):
        return payload
    return []

def extract_total_count(payload):
    if not isinstance(payload, dict):
        return None
    meta = payload.get("meta")
    if isinstance(meta, dict):
        total = meta.get("total")
        if isinstance(total, int):
            return total
    total = payload.get("total")
    if isinstance(total, int):
        return total
    return None

def extract_page_progress(payload):
    if not isinstance(payload, dict):
        return None, None
    meta = payload.get("meta")
    if isinstance(meta, dict):
        current_page = meta.get("current_page")
        total_pages = meta.get("total_pages")
        if isinstance(current_page, int) and isinstance(total_pages, int):
            return current_page, total_pages
    current_page = payload.get("current_page")
    total_pages = payload.get("total_pages")
    if isinstance(current_page, int) and isinstance(total_pages, int):
        return current_page, total_pages
    return None, None


def extract_entity(record):
    if isinstance(record, dict) and isinstance(record.get("entity"), dict):
        return record.get("entity") or {}
    return record if isinstance(record, dict) else {}


def fetch_all(endpoint, api_key, account_id, base_url=None, per_page=50, max_pages=200):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Beacon-Application": "developer_api",
    }
    all_rows = []
    page = 1
    while page <= max_pages:
        url = build_beacon_url(endpoint, account_id, base_url=base_url)
        params = {
            "page": page,
            "per_page": per_page,
            "sort_by": "created_at",
            "sort_direction": "desc",
        }
        resp = None
        for attempt in range(4):
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            if resp.status_code not in (429, 500, 502, 503, 504):
                break
            if attempt < 3:
                time.sleep(2 ** attempt)
        if resp is None:
            raise SystemExit(f"Beacon request failed for {endpoint}: no response")
        if resp.status_code >= 400:
            try:
                details = resp.json()
            except Exception:
                details = resp.text[:500]
            raise SystemExit(f"Beacon error {resp.status_code} for {endpoint}: {details}")
        data = resp.json()
        rows = extract_results(data)
        if not rows:
            break
        all_rows.extend(rows)
        if len(rows) < per_page:
            break
        total = extract_total_count(data)
        if isinstance(total, int) and len(all_rows) >= total:
            break
        current_page, total_pages = extract_page_progress(data)
        if isinstance(current_page, int) and isinstance(total_pages, int) and current_page >= total_pages:
            break
        page += 1
    return all_rows


def upsert_rows(table, rows, client):
    if not rows:
        return 0
    client.table(table).upsert(rows).execute()
    return len(rows)

def log_system_audit(client, action, details=None, region="Global"):
    try:
        client.table("audit_logs").insert({
            "user_email": "System",
            "action": action,
            "details": details or {},
            "region": region,
        }).execute()
    except Exception as e:
        # Keep sync resilient even if audit logging fails.
        print(f"Audit Log Error: {e}")


def main():
    secrets = load_secrets()
    supabase_url = get_env_or_secret(secrets, "SUPABASE_URL") or (secrets.get("supabase") or {}).get("url")
    supabase_key = get_env_or_secret(secrets, "SUPABASE_SERVICE_ROLE_KEY") or (secrets.get("supabase") or {}).get("key")
    beacon_key = get_env_or_secret(secrets, "BEACON_API_KEY")
    account_id = get_env_or_secret(secrets, "BEACON_ACCOUNT_ID")
    beacon_base_url = get_env_or_secret(secrets, "BEACON_BASE_URL")

    if not supabase_url or not supabase_key:
        raise SystemExit("Missing Supabase URL or key. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY.")
    if not beacon_key:
        raise SystemExit("Missing Beacon credentials. Set BEACON_API_KEY.")
    if not beacon_base_url and not account_id:
        raise SystemExit("Set BEACON_BASE_URL (preferred) or BEACON_ACCOUNT_ID.")

    client = create_client(supabase_url, supabase_key)

    sync_context = {
        "source": "beacon_api",
        "trigger": "github_actions",
        "workflow": os.getenv("GITHUB_WORKFLOW", "manual_or_unknown"),
        "run_id": os.getenv("GITHUB_RUN_ID"),
    }
    log_system_audit(client, "Data Sync Started", sync_context)

    try:
        datasets = {
            "people": fetch_all("person", beacon_key, account_id, base_url=beacon_base_url),
            "organisations": fetch_all("organization", beacon_key, account_id, base_url=beacon_base_url),
            "events": fetch_all("event", beacon_key, account_id, base_url=beacon_base_url),
            "payments": fetch_all("payment", beacon_key, account_id, base_url=beacon_base_url),
            "subscriptions": fetch_all("subscription", beacon_key, account_id, base_url=beacon_base_url),
            "grants": fetch_all("grant", beacon_key, account_id, base_url=beacon_base_url),
        }

        count_people = upsert_rows(
            "beacon_people",
            [
                {"id": e.get("id"), "payload": e, "created_at": e.get("created_at")}
                for e in [extract_entity(p) for p in datasets["people"]]
                if e.get("id")
            ],
            client,
        )

        count_orgs = upsert_rows(
            "beacon_organisations",
            [
                {"id": e.get("id"), "payload": e, "created_at": e.get("created_at")}
                for e in [extract_entity(o) for o in datasets["organisations"]]
                if e.get("id")
            ],
            client,
        )

        count_events = upsert_rows(
            "beacon_events",
            [
                {
                    "id": x.get("id"),
                    "payload": x,
                    "start_date": x.get("start_date") or x.get("date") or x.get("created_at"),
                    "region": (x.get("c_region") or [x.get("region")] or [None])[0],
                }
                for x in [extract_entity(e) for e in datasets["events"]]
                if x.get("id")
            ],
            client,
        )

        payment_entities = {}
        for p in datasets["payments"]:
            e = extract_entity(p)
            rec_id = e.get("id")
            if rec_id:
                payment_entities[rec_id] = e
        for s in datasets["subscriptions"]:
            e = extract_entity(s)
            rec_id = e.get("id")
            if rec_id and rec_id not in payment_entities:
                payment_entities[rec_id] = e

        count_payments = upsert_rows(
            "beacon_payments",
            [
                {"id": x.get("id"), "payload": x, "payment_date": x.get("payment_date") or x.get("date") or x.get("created_at")}
                for x in payment_entities.values()
                if x.get("id")
            ],
            client,
        )

        count_grants = upsert_rows(
            "beacon_grants",
            [
                {"id": x.get("id"), "payload": x, "close_date": x.get("close_date") or x.get("award_date") or x.get("created_at")}
                for x in [extract_entity(g) for g in datasets["grants"]]
                if x.get("id")
            ],
            client,
        )

        summary = {
            "people": count_people,
            "organisations": count_orgs,
            "events": count_events,
            "payments": count_payments,
            "grants": count_grants,
            "synced_at": datetime.utcnow().isoformat() + "Z",
        }
        log_system_audit(client, "Data Sync Completed", {**sync_context, **summary})
        print(json.dumps(summary, indent=2))
    except Exception as e:
        log_system_audit(client, "Data Sync Failed", {**sync_context, "error": str(e)})
        raise


if __name__ == "__main__":
    main()
