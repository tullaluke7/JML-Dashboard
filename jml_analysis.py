import pandas as pd

# Load data
hr = pd.read_csv("hr_feed.csv")
ad = pd.read_csv("ad_users.csv")
okta = pd.read_csv("okta_users.csv")

# Merge data for analysis
merged_ad = hr.merge(ad, on="employee_id", how="left", suffixes=("_hr", "_ad"))
merged_okta = hr.merge(okta, on="employee_id", how="left", suffixes=("_hr", "_okta"))

# Identify Orphaned Accounts (exist in AD/Okta but not HR)
orphan_ad = ad[~ad['employee_id'].isin(hr['employee_id'])]
orphan_okta = okta[~okta['employee_id'].isin(hr['employee_id'])]

# Identify Terminated but Still Active
terminated_ad = merged_ad[(merged_ad['status_hr'] == "Terminated") & (merged_ad['status_ad'] == "Active")]
terminated_okta = merged_okta[(merged_okta['status_hr'] == "Terminated") & (merged_okta['status_okta'] == "Active")]

# Identify Movers (department mismatch)
movers_ad = merged_ad[(merged_ad['department_hr'] != merged_ad['department_ad']) & merged_ad['department_ad'].notna()]
movers_okta = merged_okta[(merged_okta['department_hr'] != merged_okta['department_okta']) & merged_okta['department_okta'].notna()]

# Summary stats
print("=== JML Dashboard Summary ===")
print(f"Total HR Users: {len(hr)}")
print(f"Orphaned AD Accounts: {len(orphan_ad)}")
print(f"Orphaned Okta Accounts: {len(orphan_okta)}")
print(f"Terminated but Active in AD: {len(terminated_ad)}")
print(f"Terminated but Active in Okta: {len(terminated_okta)}")
print(f"Movers with mismatch in AD: {len(movers_ad)}")
print(f"Movers with mismatch in Okta: {len(movers_okta)}")

# Export reports
orphan_ad.to_csv("report_orphan_ad.csv", index=False)
orphan_okta.to_csv("report_orphan_okta.csv", index=False)
terminated_ad.to_csv("report_terminated_ad.csv", index=False)
terminated_okta.to_csv("report_terminated_okta.csv", index=False)
movers_ad.to_csv("report_movers_ad.csv", index=False)
movers_okta.to_csv("report_movers_okta.csv", index=False)
