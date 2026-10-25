import os
import json
import requests
from datetime import datetime

DATA_FILE = "data/dashboard_data.json"

# Master list of requested Function 150 International Affairs TAS accounts
FUNCTION_150_TAS_MASTER = [
    # Agency 011 - Funds Appropriated to the President
    {"tas": "011-0700", "agency_code": "011", "agency": "Presidential Funds (USADF)", "account_name": "United States African Development Foundation", "context": "USADF (Independent Foreign Assistance Agency)"},
    {"tas": "011-1022", "agency_code": "011", "agency": "Presidential Funds (State/INL)", "account_name": "International Narcotics Control and Law Enforcement (INCLE)", "context": "State Dept (Bureau of International Narcotics & Law Enforcement)"},
    {"tas": "011-1081", "agency_code": "011", "agency": "Presidential Funds (State/DoD)", "account_name": "International Military Education and Training (IMET)", "context": "Policy: State Dept / Execution: DoD (DSCA)"},
    {"tas": "011-1082", "agency_code": "011", "agency": "Presidential Funds (State/DoD)", "account_name": "Foreign Military Financing (FMF)", "context": "Policy: State Dept / Execution: DoD (DSCA)"},
    {"tas": "011-3100", "agency_code": "011", "agency": "Presidential Funds (IAF)", "account_name": "Inter-American Foundation", "context": "IAF (Independent Foreign Assistance Agency)"},

    # Agency 012 - Department of Agriculture
    {"tas": "012-2278", "agency_code": "012", "agency": "USDA / Foreign Food Assistance", "account_name": "Title II (Food for Peace / FFP)", "context": "USDA / Jointly administered with USAID (BHA)"},
    {"tas": "012-2900", "agency_code": "012", "agency": "USDA / Foreign Food Assistance", "account_name": "McGovern-Dole International Food for Education", "context": "USDA Foreign Agricultural Service"},
    {"tas": "012-4049", "agency_code": "012", "agency": "USDA / Foreign Food Assistance", "account_name": "P.L. 480 Direct Credit Financing Account", "context": "USDA Foreign Agricultural Service"},

    # Agency 019 - Department of State
    {"tas": "019-0102", "agency_code": "019", "agency": "Department of State", "account_name": "IBWC: Salaries & Expenses", "context": "International Boundary and Water Commission (U.S.-Mexico)"},
    {"tas": "019-0106", "agency_code": "019", "agency": "Department of State", "account_name": "IBWC: Construction", "context": "International Boundary and Water Commission (U.S.-Mexico)"},
    {"tas": "019-0107", "agency_code": "019", "agency": "Department of State", "account_name": "International Fisheries Commissions", "context": "Bureau of Oceans & Environmental/Scientific Affairs"},
    {"tas": "019-0108", "agency_code": "019", "agency": "Department of State", "account_name": "Embassy Security, Construction, and Maintenance (ESCM)", "context": "Bureau of Overseas Buildings Operations (OBO)"},
    {"tas": "019-0111", "agency_code": "019", "agency": "Department of State", "account_name": "Protection of Foreign Missions and Officials (PFMO)", "context": "Bureau of Diplomatic Security (DS)"},
    {"tas": "019-0112", "agency_code": "019", "agency": "Department of State", "account_name": "Educational and Cultural Exchange Programs (ECA)", "context": "Bureau of Educational and Cultural Affairs"},
    {"tas": "019-0113", "agency_code": "019", "agency": "Department of State", "account_name": "Diplomatic and Consular Programs (D&CP)", "context": "Core State Dept Operations & Diplomatic Programs"},
    {"tas": "019-0114", "agency_code": "019", "agency": "Department of State", "account_name": "Office of Inspector General (State OIG)", "context": "Independent State Dept Oversight"},
    {"tas": "019-0522", "agency_code": "019", "agency": "Department of State", "account_name": "Contributions to International Organizations (CIO)", "context": "Bureau of International Organization Affairs (IO)"},
    {"tas": "019-0523", "agency_code": "019", "agency": "Department of State", "account_name": "Contributions for International Peacekeeping Activities (CIPA)", "context": "Bureau of International Organization Affairs (IO)"},
    {"tas": "019-0601", "agency_code": "019", "agency": "Department of State", "account_name": "Repatriation Loans Program Account", "context": "Bureau of Consular Affairs (CA)"},
    {"tas": "019-0820", "agency_code": "019", "agency": "Department of State", "account_name": "Buying Power Maintenance Account", "context": "Foreign Exchange Rate Fluctuations"},
    {"tas": "019-1030", "agency_code": "019", "agency": "Department of State", "account_name": "Global Health Programs (GHP - State)", "context": "Office of the U.S. Global AIDS Coordinator (PEPFAR)"},
    {"tas": "019-1082", "agency_code": "019", "agency": "Department of State", "account_name": "Nonproliferation, Anti-terrorism, Demining and Related (NADR)", "context": "Bureaus of ISN, CT, and PM"},
    {"tas": "019-1085", "agency_code": "019", "agency": "Department of State", "account_name": "Peacekeeping Operations (PKO)", "context": "Bureau of Political-Military Affairs (PM)"},
    {"tas": "019-1121", "agency_code": "019", "agency": "Department of State", "account_name": "Democracy Fund (DF)", "context": "Bureau of Democracy, Human Rights, and Labor (DRL)"},
    {"tas": "019-1122", "agency_code": "019", "agency": "Department of State", "account_name": "National Security Investment Programs (NSIP)", "context": "Security & Infrastructure Programs"},
    {"tas": "019-1143", "agency_code": "019", "agency": "Department of State", "account_name": "Migration and Refugee Assistance (MRA)", "context": "Bureau of Population, Refugees, and Migration (PRM)"},
    {"tas": "019-1145", "agency_code": "019", "agency": "Department of State", "account_name": "Emergency Refugee and Migration Assistance Fund (ERMA)", "context": "Bureau of Population, Refugees, and Migration (PRM)"},
    {"tas": "019-1200", "agency_code": "019", "agency": "Department of State", "account_name": "East-West Center", "context": "Asian/Pacific Educational & Cultural Institution"},
    {"tas": "019-1209", "agency_code": "019", "agency": "Department of State", "account_name": "The Asia Foundation", "context": "Non-profit Grantee for Rule of Law & Governance"},
    {"tas": "019-4239", "agency_code": "019", "agency": "Department of State", "account_name": "Repatriation Loans Credit Financing Account", "context": "Bureau of Consular Affairs (CA)"},
    {"tas": "019-4519", "agency_code": "019", "agency": "Department of State", "account_name": "Working Capital Fund (State WCF)", "context": "Centralized IT, Administrative & Shared Services"},

    # Agency 071 - U.S. International Development Finance Corporation
    {"tas": "071-0100", "agency_code": "071", "agency": "DFC", "account_name": "DFC Program Account", "context": "DFC (Assumed OPIC & USAID DCA direct functions)"},
    {"tas": "071-4470", "agency_code": "071", "agency": "DFC", "account_name": "DFC Corporate Capital Account", "context": "DFC Administrative & Equity Investment Account"},

    # Agency 072 - U.S. Agency for International Development
    {"tas": "072-0300", "agency_code": "072", "agency": "USAID", "account_name": "Capital Investment Fund (CIF)", "context": "M/CIO IT Infrastructure & Physical Capital"},
    {"tas": "072-0306", "agency_code": "072", "agency": "USAID", "account_name": "Assistance for Europe, Eurasia, and Central Asia (AEECA)", "context": "Bureau for Europe and Eurasia (E&E)"},
    {"tas": "072-0307", "agency_code": "072", "agency": "USAID", "account_name": "Complex Crises Fund (Allocation/Sub-account)", "context": "Program/Regional Sub-account Tracking Symbol"},
    {"tas": "072-0400", "agency_code": "072", "agency": "USAID", "account_name": "Working Capital Fund (USAID WCF)", "context": "M Bureau IT & Administrative Shared Services"},
    {"tas": "072-1000", "agency_code": "072", "agency": "USAID", "account_name": "Operating Expenses of USAID (USAID OE)", "context": "Core Administrative & Operating Budget"},
    {"tas": "072-1002", "agency_code": "072", "agency": "USAID", "account_name": "Foreign Service Retirement and Disability Fund", "context": "USAID Foreign Service Retirement Trust Account"},
    {"tas": "072-1007", "agency_code": "072", "agency": "USAID", "account_name": "Office of Inspector General (USAID OIG
