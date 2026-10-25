import os
import json
import requests
from datetime import datetime

DATA_FILE = "data/dashboard_data.json"

def fetch_openomb_apportionments():
    """Fetch recent apportionment records from OpenOMB API."""
    url = "https://openomb.org/api/v1/files/recent"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json().get("results", [])
    except Exception as e:
        print(f"Warning: OpenOMB fetch failed ({e}).")
    return []

def build_merged_dataset():
    """Construct merged JSON payload for the frontend dashboard."""
    openomb_items = fetch_openomb_apportionments()
    
    payload = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "apportionments": openomb_items,
        "sample_tas_balances": [
            {
                "tas": "072-1021",
                "agency": "USAID",
                "account_name": "Operating Expenses",
                "fy": "2026",
                "total_budgetary_resources": 1450000000,
                "unobligated_balance": 185000000,
                "apportioned_unobligated": 140000000,
                "unapportioned_unobligated": 30000000,
                "expired_unobligated": 15000000,
                "status": "Active"
            },
            {
                "tas": "019-1140",
                "agency": "Department of State",
                "account_name": "Diplomatic Programs",
                "fy": "2026",
                "total_budgetary_resources": 3800000000,
                "unobligated_balance": 410000000,
                "apportioned_unobligated": 320000000,
                "unapportioned_unobligated": 60000000,
                "expired_unobligated": 30000000,
                "status": "Active"
            }
        ]
    }
    
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Data successfully saved to {DATA_FILE}")

if __name__ == "__main__":
    build_merged_dataset()
