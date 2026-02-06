import os
import json
import requests
from datetime import datetime

try:
    import tomllib  # py3.11+
except Exception:  # pragma: no cover
    tomllib = None

from supabase import create_client

BEACON_BASE_URL = "https://api.beaconcrm.org/v1/account/{account_id}/entity/"


def load_secrets():
    secrets = {}
    secrets_path = os.path.join(os.path.dirname(__file__), ".streamlit", "secrets.toml")
    if os.path.exists(secrets_path) and tomllib:
        with open(secrets_path, "rb") as f:
            secrets = tomllib.load(f)
    return secrets


def get_env_or_secret(secrets, key):
    return os.getenv(key) or secrets.get(key)


def fetch_all(endpoint, api_key, account_id):
    url = f"{BEACON_BASE_URL}{endpoint}".format(account_id=account_id)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Beacon-Application": "developer_api",
    }
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code >= 400:
        try:
            details = resp.json()
        except Exception:
            details = resp.text[:500]
        raise SystemExit(f"Beacon error {resp.status_code} for {endpoint}: {details}")
    data = resp.json()
    return data.get("data", [])


def upsert_rows(table, rows, client):
    if not rows:
        return 0
    client.table(table).upsert(rows).execute()
    return len(rows)


def main():
    secrets = load_secrets()
    supabase_url = get_env_or_secret(secrets, "SUPABASE_URL") or (secrets.get("supabase") or {}).get("url")
    supabase_key = get_env_or_secret(secrets, "SUPABASE_SERVICE_ROLE_KEY") or (secrets.get("supabase") or {}).get("key")
    beacon_key = get_env_or_secret(secrets, "BEACON_API_KEY")
    account_id = get_env_or_secret(secrets, "BEACON_ACCOUNT_ID")

    if not supabase_url or not supabase_key:
        raise SystemExit("Missing Supabase URL or key. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY.")
    if not beacon_key or not account_id:
        raise SystemExit("Missing Beacon credentials. Set BEACON_API_KEY and BEACON_ACCOUNT_ID.")

    client = create_client(supabase_url, supabase_key)

    datasets = {
        "people": fetch_all("person", beacon_key, account_id),
        "organisations": fetch_all("organization", beacon_key, account_id),
        "events": fetch_all("event", beacon_key, account_id),
        "payments": fetch_all("payment", beacon_key, account_id),
        "grants": fetch_all("grant", beacon_key, account_id),
    }

    count_people = upsert_rows(
        "beacon_people",
        [{"id": p.get("id"), "payload": p, "created_at": p.get("created_at")} for p in datasets["people"] if p.get("id")],
        client,
    )

    count_orgs = upsert_rows(
        "beacon_organisations",
        [{"id": o.get("id"), "payload": o, "created_at": o.get("created_at")} for o in datasets["organisations"] if o.get("id")],
        client,
    )

    count_events = upsert_rows(
        "beacon_events",
        [
            {
                "id": e.get("id"),
                "payload": e,
                "start_date": e.get("start_date"),
                "region": (e.get("c_region") or [None])[0],
            }
            for e in datasets["events"]
            if e.get("id")
        ],
        client,
    )

    count_payments = upsert_rows(
        "beacon_payments",
        [{"id": p.get("id"), "payload": p, "payment_date": p.get("payment_date")} for p in datasets["payments"] if p.get("id")],
        client,
    )

    count_grants = upsert_rows(
        "beacon_grants",
        [{"id": g.get("id"), "payload": g, "close_date": g.get("close_date")} for g in datasets["grants"] if g.get("id")],
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
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
