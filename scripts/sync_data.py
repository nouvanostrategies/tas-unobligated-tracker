import os
import json
import requests
from datetime import datetime

DATA_FILE = "data/dashboard_data.json"
FISCAL_YEARS = ["2024", "2025", "2026", "2027"]

# Master list of requested Function 150 International Affairs TAS accounts
FUNCTION_150_TAS_MASTER = [
    # Agency 011 - Funds Appropriated to the President
    {"tas": "011-0700", "agency_code": "011", "agency": "Presidential Funds (USADF)", "account_name": "United States African Development Foundation", "context": "USADF (Independent Foreign Assistance Agency)"},
    {"tas": "011-1022", "agency_code": "011", "agency": "Presidential Funds (State/INL)", "account_name": "International Narcotics Control and Law Enforcement (INCLE)", "context": "State Dept (INL)"},
    {"tas": "011-1081", "agency_code": "011", "agency": "Presidential Funds (State/DoD)", "account_name": "International Military Education and Training (IMET)", "context": "Policy: State / Exec: DoD"},
    {"tas": "011-1082", "agency_code": "011", "agency": "Presidential Funds (State/DoD)", "account_name": "Foreign Military Financing (FMF)", "context": "Policy: State / Exec: DoD"},
    {"tas": "011-3100", "agency_code": "011", "agency": "Presidential Funds (IAF)", "account_name": "Inter-American Foundation", "context": "IAF (Independent Foreign Assistance Agency)"},

    # Agency 012 - Department of Agriculture
    {"tas": "012-2278", "agency_code": "012", "agency": "USDA / Food Aid", "account_name": "Title II (Food for Peace / FFP)", "context": "USDA / Joint with USAID BHA"},
    {"tas": "012-2900", "agency_code": "012", "agency": "USDA / Food Aid", "account_name": "McGovern-Dole International Food for Education", "context": "USDA Foreign Agricultural Service"},
    {"tas": "012-4049", "agency_code": "012", "agency": "USDA / Food Aid", "account_name": "P.L. 480 Direct Credit Financing Account", "context": "USDA Foreign Agricultural Service"},

    # Agency 019 - Department of State
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
    {"tas": "019-1121", "agency_code": "019", "agency": "Department of State", "account
