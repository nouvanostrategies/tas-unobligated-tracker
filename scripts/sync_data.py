import os
import json
import requests
from datetime import datetime

DATA_FILE = "data/dashboard_data.json"

FUNCTION_150_TAS_MASTER = [
    # Agency 011
    {"tas": "011-0700", "agency_code": "011", "agency": "Presidential Funds (USADF)", "account_name": "United States African Development Foundation", "context": "USADF (Independent Foreign Assistance Agency)"},
    {"tas": "011-1022", "agency_code": "011", "agency": "Presidential Funds (State/INL)", "account_name": "International Narcotics Control and Law Enforcement (INCLE)", "context": "State Dept (INL)"},
    {"tas": "011-1081", "agency_code": "011", "agency": "Presidential Funds (State/DoD)", "account_name": "International Military Education and Training (IMET)", "context": "Policy: State / Exec: DoD"},
    {"tas": "011-1082", "agency_code": "011", "agency": "Presidential Funds (State/DoD)", "account_name": "Foreign Military Financing (FMF)", "context": "Policy: State / Exec: DoD"},
    {"tas": "011-3100", "agency_code": "011", "agency": "Presidential Funds (IAF)", "account_name": "Inter-American Foundation", "context": "IAF (Independent Foreign Assistance Agency)"},

    # Agency 012
    {"tas": "012-2278", "agency_code": "012", "agency": "USDA / Food Aid", "account_name": "Title II (Food for Peace / FFP)", "context": "USDA / Joint with USAID BHA"},
    {"tas": "012-2900", "agency_code": "012", "agency": "USDA / Food Aid", "account_name": "McGovern-Dole International Food for Education", "context": "USDA Foreign Agricultural Service"},
    {"tas": "012-4049", "agency_code": "012", "agency": "USDA / Food Aid", "account_name": "P.L. 480 Direct Credit Financing Account", "context": "USDA Foreign Agricultural Service"},

    # Agency 019
    {"tas": "019-0102", "agency_code": "019", "agency": "Department of State", "account_name": "IBWC: Salaries & Expenses", "context": "International Boundary and Water Commission"},
    {"tas": "019-0106", "agency_code": "019", "agency": "Department of State", "account_name": "IBWC: Construction", "context": "International Boundary and Water Commission"},
    {"tas": "019-0107", "agency_code": "019", "agency": "Department of State", "account_name": "International Fisheries Commissions", "context": "Bureau of Oceans & Environmental Affairs"},
    {"tas": "019-0108", "agency_code": "019", "agency": "Department of State", "account_name": "Embassy Security, Construction, and Maintenance (ESCM)", "context": "Bureau of Overseas Buildings Operations"},
    {"tas": "019-0111", "agency_code": "019", "agency": "Department of State", "account_name": "Protection of Foreign Missions and Officials (PFMO)", "context": "Bureau of Diplomatic Security"},
    {"tas": "019-0112", "agency_code": "019", "agency": "Department of State", "account_name": "Educational and Cultural Exchange Programs (ECA)", "context": "Bureau of Educational and Cultural Affairs"},
    {"tas": "019-0113", "agency_code": "019", "agency": "Department of State", "account_name": "Diplomatic and Consular Programs (D&CP)", "context": "Core State Dept Operations"},
    {"tas": "019-0114", "agency_code": "019", "agency": "Department of State", "account_name": "Office of Inspector General (State OIG)", "context": "Independent State Dept Oversight"},
    {"tas": "019-0522", "agency_code": "019", "agency": "Department of State", "account_name": "Contributions to International Organizations (CIO)", "context": "Bureau of International Organization Affairs"},
    {"tas": "019-0523", "agency_code": "019", "agency": "Department of State", "account_name": "Contributions for International Peacekeeping Activities (CIPA)", "context": "Bureau of International Organization Affairs"},
    {"tas": "019-0601", "agency_code": "019", "agency": "Department of State", "account_name": "Repatriation Loans Program Account", "context": "Bureau of Consular Affairs"},
    {"tas": "019-0820", "agency_code": "019", "agency": "Department of State", "account_name": "Buying Power Maintenance Account", "context": "Foreign Exchange Rate Fluctuations"},
    {"tas": "019-1030", "agency_code": "019", "agency": "Department of State", "account_name": "Global Health Programs (GHP - State)", "context": "Office of PEPFAR Coordinator"},
    {"tas": "019-1082", "agency_code": "019", "agency": "Department of State", "account_name": "Nonproliferation, Anti-terrorism, Demining and Related (NADR)", "context": "ISN, CT, and PM Bureaus"},
    {"tas": "019-1085", "agency_code": "019", "agency": "Department of State", "account_name": "Peacekeeping Operations (PKO)", "context": "Bureau of Political-Military Affairs"},
    {"tas": "019-1121", "agency_code": "019", "agency": "Department of State", "account_name": "Democracy Fund (DF)", "context": "Bureau of Democracy, Human Rights, and Labor"},
    {"tas": "019-1122", "agency_code": "019", "agency": "Department of State", "account_name": "National Security Investment Programs (NSIP)", "context": "Security Infrastructure Programs"},
    {"tas": "019-1143", "agency_code": "019", "agency": "Department of State", "account_name": "Migration and Refugee Assistance (MRA)", "context": "Bureau of Population, Refugees, and Migration"},
    {"tas": "019-1145", "agency_code": "019", "agency": "Department of State", "account_name": "Emergency Refugee and Migration Assistance Fund (ERMA)", "context": "Bureau of Population, Refugees, and Migration"},
    {"tas": "019-1200", "agency_code": "019", "agency": "Department of State", "account_name": "East-West Center", "context": "Asian/Pacific Educational Institution"},
    {"tas": "019-1209", "agency_code": "019", "agency": "Department of State", "account_name": "The Asia Foundation", "context": "Non-profit Grantee for Rule of Law"},
    {"tas": "019-4239", "agency_code": "019", "agency": "Department of State", "account_name": "Repatriation Loans Credit Financing Account", "context": "Bureau of Consular Affairs"},
    {"tas": "019-4519", "agency_code": "019", "agency": "Department of State", "account_name": "Working Capital Fund (State WCF)", "context": "Shared IT & Administrative Services"},

    # Agency 071
    {"tas": "071-0100", "agency_code": "071", "agency": "DFC", "account_name": "DFC Program Account", "context": "DFC Direct Functions"},
    {"tas": "071-4470", "agency_code": "071", "agency": "DFC", "account_name": "DFC Corporate Capital Account", "context": "DFC Admin & Equity Account"},

    # Agency 072
    {"tas": "072-0300", "agency_code": "072", "agency": "USAID", "account_name": "Capital Investment Fund (CIF)", "context": "M/CIO IT Infrastructure"},
    {"tas": "072-0306", "agency_code": "072", "agency": "USAID", "account_name": "Assistance for Europe, Eurasia, and Central Asia (AEECA)", "context": "Bureau for Europe and Eurasia"},
    {"tas": "072-0307", "agency_code": "072", "agency": "USAID", "account_name": "Complex Crises Fund (Allocation/Sub-account)", "context": "Program/Regional Sub-account"},
    {"tas": "072-0400", "agency_code": "072", "agency": "USAID", "account_name": "Working Capital Fund (USAID WCF)", "context": "M Bureau IT & Shared Services"},
    {"tas": "072-1000", "agency_code": "072", "agency": "USAID", "account_name": "Operating Expenses of USAID (USAID OE)", "context": "Core Operating Budget"},
    {"tas": "072-1002", "agency_code": "072", "agency": "USAID", "account_name": "Foreign Service Retirement and Disability Fund", "context": "Foreign Service Retirement Trust"},
    {"tas": "072-1007", "agency_code": "072", "agency": "USAID", "account_name": "Office of Inspector General (USAID OIG)", "context": "Independent USAID Oversight"},
    {"tas": "072-1015", "agency_code": "072", "agency": "USAID", "account_name": "Complex Crises Fund (CCF - Main Treasury TAS)", "context": "Bureau for CPS"},
    {"tas": "072-1021", "agency_code": "072", "agency": "USAID", "account_name": "Development Assistance (DA)", "context": "Sustainable Development Programs"},
    {"tas": "072-1027", "agency_code": "072", "agency": "USAID", "account_name": "Transition Initiatives (TI - Main Treasury TAS)", "context": "Office of Transition Initiatives"},
    {"tas": "072-1033", "agency_code": "072", "agency": "USAID", "account_name": "Global Health Programs (GHP - USAID)", "context": "Bureau for Global Health"},
    {"tas": "072-1035", "agency_code": "072", "agency": "USAID", "account_name": "International Disaster Assistance (IDA)", "context": "Bureau for Humanitarian Assistance"},
    {"tas": "072-1036", "agency_code": "072", "agency": "USAID", "account_name": "Transition Initiatives (Allocation/Sub-account)", "context": "Program/Regional Sub-account"},
    {"tas": "072-1037", "agency_code": "072", "agency": "USAID", "account_name": "Economic Support Fund (ESF)", "context": "Strategic Economic Aid"},
    {"tas": "072-1250", "agency_code": "072", "agency": "USAID", "account_name": "Housing & Urban Credit Guarantee Financing Account", "context": "Legacy Development Credit Account"},
    {"tas": "072-4340", "agency_code": "072", "agency": "USAID", "account_name": "Development Credit Authority Financing Account (DCA)", "context": "Legacy Credit Guarantee Account"},

    # Agency 084 & 095
    {"tas": "084-0100", "agency_code": "084", "agency": "Peace Corps", "account_name": "Peace Corps Operating Expenses", "context": "Peace Corps"},
    {"tas": "095-2750", "agency_code": "095", "agency": "MCC", "account_name": "Millennium Challenge Corporation (MCC)", "context": "MCC"}
]

def fetch_openomb_apportionments():
    url = "https://openomb.org/api/v1/files/recent"
    target_tas_codes = [item["tas"] for item in FUNCTION_150_TAS_MASTER]
    filtered_items = []
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            results = response.json().get("results", [])
            for item in results:
                title = item.get("title", "")
                filename = item.get("filename", "")
                if any(tas in title or tas in filename for tas in target_tas_codes):
                    filtered_items.append(item)
    except Exception as e:
        print(f"Warning: OpenOMB fetch failed ({e}).")
    return filtered_items

def generate_tas_budgetary_data():
    dataset = []
    for item in FUNCTION_150_TAS_MASTER:
        base_total = 1200000000 if any(k in item["tas"] for k in ["1021", "1037", "1035", "1143"]) else 250000000
        unobs = int(base_total * 0.12)
        apportioned = int(unobs * 0.75)
        unapportioned = int(unobs * 0.18)
        expired = int(unobs * 0.07)

        dataset.append({
            "tas": item["tas"],
            "agency_code": item["agency_code"],
            "agency": item["agency"],
            "account_name": item["account_name"],
            "context": item["context"],
            "fy": "2026",
            "total_budgetary_resources": base_total,
            "unobligated_balance": unobs,
            "apportioned_unobligated": apportioned,
            "unapportioned_unobligated": unapportioned,
            "expired_unobligated": expired,
            "status": "Active"
        })
    return dataset

def build_merged_dataset():
    openomb_items = fetch_openomb_apportionments()
    balances = generate_tas_budgetary_data()
    
    payload = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "apportionments": openomb_items,
        "sample_tas_balances": balances
    }
    
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Data successfully saved to {DATA_FILE} ({len(balances)} target TAS accounts)")

if __name__ == "__main__":
    build_merged_dataset()
