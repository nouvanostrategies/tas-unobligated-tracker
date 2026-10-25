import os
import json
import requests
from datetime import datetime

DATA_FILE = "data/dashboard_data.json"
FISCAL_YEARS = ["2024", "2025", "2026", "2027"]

FUNCTION_150_TAS_MASTER = [
    # Agency 011 - Funds Appropriated to the President
    {"tas": "011-0700", "agency_code": "011", "agency": "Presidential Funds (USADF)", "account_name": "United States African Development Foundation", "context": "USADF (Independent Agency)"},
    {"tas": "011-1022", "agency_code": "011", "agency": "Presidential Funds (State/INL)", "account_name": "International Narcotics Control and Law Enforcement (INCLE)", "context": "State Dept (INL)"},
    {"tas": "011-1081", "agency_code": "011", "agency": "Presidential Funds (State/DoD)", "account_name": "International Military Education and Training (IMET)", "context": "Policy: State / Exec: DoD"},
    {"tas": "011-1082", "agency_code": "011", "agency": "Presidential Funds (State/DoD)", "account_name": "Foreign Military Financing (FMF)", "context": "Policy: State / Exec: DoD"},
    {"tas": "011-3100", "agency_code": "011", "agency": "Presidential Funds (IAF)", "account_name": "Inter-American Foundation", "context": "IAF (Independent Agency)"},

    # Agency 012 - Department of Agriculture
    {"tas": "012-2278", "agency_code": "012", "agency": "USDA / Food Aid", "account_name": "Title II (Food for Peace / FFP)", "context": "USDA / Joint with USAID BHA"},
    {"tas": "012-2900", "agency_code": "012", "agency": "USDA / Food Aid", "account_name": "McGovern-Dole International Food for Education", "context": "USDA FAS"},
    {"tas": "012-4049", "agency_code": "012", "agency": "USDA / Food Aid", "account_name": "P.L. 480 Direct Credit Financing Account", "context": "USDA FAS"},

    # Agency 019 - Department of State
    {"tas": "019-0102", "agency_code": "019", "agency": "Department of State", "account_name": "IBWC: Salaries & Expenses", "context": "International Boundary & Water Comm"},
    {"tas": "019-0106", "agency_code": "019", "agency": "Department of State", "account_name": "IBWC: Construction", "context": "International Boundary & Water Comm"},
    {"tas": "019-0107", "agency_code": "019", "agency": "Department of State", "account_name": "International Fisheries Commissions", "context": "Bureau of Oceans & Environment"},
    {"tas": "019-0108", "agency_code": "019", "agency": "Department of State", "account_name": "Embassy Security, Construction, and Maintenance (ESCM)", "context": "Overseas Buildings Operations"},
    {"tas": "019-0111", "agency_code": "019", "agency": "Department of State", "account_name": "Protection of Foreign Missions and Officials (PFMO)", "context": "Bureau of Diplomatic Security"},
    {"tas": "019-0112", "agency_code": "019", "agency": "Department of State", "account_name": "Educational and Cultural Exchange Programs (ECA)", "context": "Bureau of Educational & Cultural Affairs"},
    {"tas": "019-0113", "agency_code": "019", "agency": "Department of State", "account_name": "Diplomatic and Consular Programs (D&CP)", "context": "Core State Dept Operations"},
    {"tas": "019-0114", "agency_code": "019", "agency": "Department of State", "account_name": "Office of Inspector General (State OIG)", "context": "Independent State Dept Oversight"},
    {"tas": "019-0522", "agency_code": "019", "agency": "Department of State", "account_name": "Contributions to International Organizations (CIO)", "context": "Bureau of Intl Organization Affairs"},
    {"tas": "019-0523", "agency_code": "019", "agency": "Department of State", "account_name": "Contributions for International Peacekeeping Activities (CIPA)", "context": "Bureau of Intl Organization Affairs"},
    {"tas": "019-0601", "agency_code": "019", "agency": "Department of State", "account_name": "Repatriation Loans Program Account", "context": "Bureau of Consular Affairs"},
    {"tas": "019-0820", "agency_code": "019", "agency": "Department of State", "account_name": "Buying Power Maintenance Account", "context": "Foreign Exchange Rate Fluctuations"},
    {"tas": "019-1030", "agency_code": "019", "agency": "Department of State", "account_name": "Global Health Programs (GHP - State)", "context": "PEPFAR Coordinator"},
    {"tas": "019-1082", "agency_code": "019", "agency": "Department of State", "account_name": "Nonproliferation, Anti-terrorism, Demining and Related (NADR)", "context": "ISN, CT, and PM Bureaus"},
    {"tas": "019-1085", "agency_code": "019", "agency": "Department of State", "account_name": "Peacekeeping Operations (PKO)", "context": "Bureau of Political-Military Affairs"},
    {"tas": "019-1121", "agency_code": "019", "agency": "Department of State", "account_name": "Democracy Fund (DF)", "context": "Bureau of DRL"},
    {"tas": "019-1122", "agency_code": "019", "agency": "Department of State", "account_name": "National Security Investment Programs (NSIP)", "context": "Security Infrastructure Programs"},
    {"tas": "019-1143", "agency_code": "019", "agency": "Department of State", "account_name": "Migration and Refugee Assistance (MRA)", "context": "Bureau of PRM"},
    {"tas": "019-1145", "agency_code": "019", "agency": "Department of State", "account_name": "Emergency Refugee and Migration Assistance Fund (ERMA)", "context": "Bureau of PRM"},
    {"tas": "019-1200", "agency_code": "019", "agency": "Department of State", "account_name": "East-West Center", "context": "Educational Institution"},
    {"tas": "019-1209", "agency_code": "019", "agency": "Department of State", "account_name": "The Asia Foundation", "context": "Rule of Law Grantee"},
    {"tas": "019-4239", "agency_code": "019", "agency": "Department of State", "account_name": "Repatriation Loans Credit Financing Account", "context": "Bureau of Consular Affairs"},
    {"tas": "019-4519", "agency_code": "019", "agency": "Department of State", "account_name": "Working Capital Fund (State WCF)", "context": "Shared IT & Administrative Services"},

    # Agency 071 - U.S. International Development Finance Corporation
    {"tas": "071-0100", "agency_code": "071", "agency": "DFC", "account_name": "DFC Program Account", "context": "DFC Direct Functions"},
    {"tas": "071-4470", "agency_code": "071", "agency": "DFC", "account_name": "DFC Corporate Capital Account", "context": "DFC Admin & Equity Account"},

    # Agency 072 - U.S. Agency for International Development
    {"tas": "072-0300", "agency_code": "072", "agency": "USAID", "account_name": "Capital Investment Fund (CIF)", "context": "M/CIO IT Infrastructure"},
    {"tas": "072-0306", "agency_code": "072", "agency": "USAID", "account_name": "Assistance for Europe, Eurasia, and Central Asia (AEECA)", "context": "Bureau for Europe and Eurasia"},
    {"tas": "072-0307", "agency_code": "072", "agency": "USAID", "account_name": "Complex Crises Fund (Allocation/Sub-account)", "context": "Sub-account Tracking"},
    {"tas": "072-0400", "agency_code": "072", "agency": "USAID", "account_name": "Working Capital Fund (USAID WCF)", "context": "M Bureau IT & Shared Services"},
    {"tas": "072-1000", "agency_code": "072", "agency": "USAID", "account_name": "Operating Expenses of USAID (USAID OE)", "context": "Core Operating Budget"},
    {"tas": "072-1002", "agency_code": "072", "agency": "USAID", "account_name": "Foreign Service Retirement and Disability Fund", "context": "Retirement Trust Account"},
    {"tas": "072-1007", "agency_code": "072", "agency": "USAID", "account_name": "Office of Inspector General (USAID OIG)", "context": "Independent Oversight"},
    {"tas": "072-1015", "agency_code": "072", "agency": "USAID", "account_name": "Complex Crises Fund (CCF - Main Treasury TAS)", "context": "Bureau for CPS"},
    {"tas": "072-1021", "agency_code": "072", "agency": "USAID", "account_name": "Development Assistance (DA)", "context": "Sustainable Development Programs"},
    {"tas": "072-1027", "agency_code": "072", "agency": "USAID", "account_name": "Transition Initiatives (TI - Main Treasury TAS)", "context": "Office of Transition Initiatives"},
    {"tas": "072-1033", "agency_code": "072", "agency": "USAID", "account_name": "Global Health Programs (GHP - USAID)", "context": "Bureau for Global Health"},
    {"tas": "072-1035", "agency_code": "072", "agency": "USAID", "account_name": "International Disaster Assistance (IDA)", "context": "Bureau for Humanitarian Assistance"},
    {"tas": "072-1036", "agency_code": "072", "agency": "USAID", "account_name": "Transition Initiatives (Allocation/Sub-account)", "context": "Sub-account Tracking"},
    {"tas": "072-1037", "agency_code": "072", "agency": "USAID", "account_name": "Economic Support Fund (ESF)", "context": "Strategic Economic Aid"},
    {"tas": "072-1250", "agency_code": "072", "agency": "USAID", "account_name": "Housing & Urban Credit Guarantee Financing Account", "context": "Legacy Credit Account"},
    {"tas": "072-4340", "agency_code": "072", "agency": "USAID", "account_name": "Development Credit Authority Financing Account (DCA)", "context": "Legacy Credit Guarantee"},

    # Agency 084 & 095 - Partner Agencies
    {"tas": "084-0100", "agency_code": "084", "agency": "Peace Corps", "account_name": "Peace Corps Operating Expenses", "context": "Peace Corps"},
    {"tas": "095-2750", "agency_code": "095", "agency": "MCC", "account_name": "Millennium Challenge Corporation (MCC)", "context": "MCC"}
]

# Explicit baseline values ($) for all accounts to prevent identical fallbacks
TAS_EXPLICIT_BASELINES = {
    "011-0700": 45_000_000,
    "011-1022": 1_420_000_000,
    "011-1081": 112_000_000,
    "011-1082": 6_100_000_000,
    "011-3100": 48_000_000,
    "012-2278": 1_750_000_000,
    "012-2900": 245_000_000,
    "012-4049": 85_000_000,
    "019-0102": 55_000_000,
    "019-0106": 32_000_000,
    "019-0107": 62_000_000,
    "019-0108": 1_980_000_000,
    "019-0111": 38_000_000,
    "019-0112": 775_000_000,
    "019-0113": 3_850_000_000,
    "019-0114": 130_000_000,
    "019-0522": 1_480_000_000,
    "019-0523": 1_260_000_000,
    "019-0601": 12_000_000,
    "019-0820": 25_000_000,
    "019-1030": 5_720_000_000,
    "019-1082": 890_000_000,
    "019-1085": 510_000_000,
    "019-1121": 340_000_000,
    "019-1122": 115_000_000,
    "019-1143": 3_920_000_000,
    "019-1145": 100_000_000,
    "019-1200": 22_000_000,
    "019-1209": 20_000_000,
    "019-4239": 15_000_000,
    "019-4519": 410_000_000,
    "071-0100": 820_000_000,
    "071-4470": 190_000_000,
    "072-0300": 260_000_000,
    "072-0306": 870_000_000,
    "072-0307": 65_000_000,
    "072-0400": 140_000_000,
    "072-1000": 1_680_000_000,
    "072-1002": 155_000_000,
    "072-1007": 98_000_000,
    "072-1015": 60_000_000,
    "072-1021": 4_350_000_000,
    "072-1027": 105_000_000,
    "072-1033": 3_950_000_000,
    "072-1035": 4_520_000_000,
    "072-1036": 90_000_000,
    "072-1037": 3_620_000_000,
    "072-1250": 40_000_000,
    "072-4340": 75_000_000,
    "084-0100": 430_000_000,
    "095-2750": 930_000_000,
}

def generate_tas_budgetary_data():
    dataset = []
    
    for item in FUNCTION_150_TAS_MASTER:
        tas_code = item["tas"]
        base_authority = TAS_EXPLICIT_BASELINES.get(
            tas_code, 
            (abs(hash(tas_code)) % 400 + 50) * 1_000_000
        )

        for fy in FISCAL_YEARS:
            fy_multiplier = 1.0 + (int(fy) - 2024) * 0.035
            total_res = int(base_authority * fy_multiplier)
            
            # Rate variation per account and fiscal year (7% to 16%)
            unobs_rate = 0.07 + (abs(hash(tas_code + fy)) % 10) / 100.0
            unobs = int(total_res * unobs_rate)
            
            apportioned = int(unobs * 0.78)
            unapportioned = int(unobs * 0.16)
            expired = max(0, unobs - (apportioned + unapportioned))

            dataset.append({
                "tas": tas_code,
                "agency_code": item["agency_code"],
                "agency": item["agency"],
                "account_name": item["account_name"],
                "context": item["context"],
                "fy": fy,
                "total_budgetary_resources": total_res,
                "unobligated_balance": unobs,
                "apportioned_unobligated": apportioned,
                "unapportioned_unobligated": unapportioned,
                "expired_unobligated": expired,
                "status": "Active"
            })
            
    return dataset

def build_merged_dataset():
    balances = generate_tas_budgetary_data()
    payload = {
        "last_updated": datetime.utcnow().isoformat() + "Z",
        "apportionments": [],
        "sample_tas_balances": balances
    }
    
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Data successfully saved to {DATA_FILE} ({len(balances)} TAS records generated)")

if __name__ == "__main__":
    build_merged_dataset()
