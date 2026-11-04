"""
Kisumu County Schools Attendance Data Analysis
----------------------------------------------
This script analyses sample data of Kisumu county Schools. 
Calculates the correlation of the schools infrustructure and class attendance datasets. 

Creates and saves a scatter plot showing correlation between attendance and number of classrooms.

Usage:
    python ksm_county_schools_data.py

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

rng = np.random.default_rng(42)

towns = ["Nyalenda", "Kondele", "Manyatta", "Milimani", "Mamboleo", "Kibuye",
          "Obunga", "Ahero", "Maseno", "Muhoroni", "Nyahera", "Chiga", "Kolwa",
          "Winam", "Kajulu", "Otonglo", "Kano", "Katito", "Sondu", "Awasi",
          "Nyakach", "Pap Onditi", "Seme", "Kombewa", "Holo", "Lela",
          "Railways", "Migosi", "Tom Mboya", "Dunga"]
schools = [f"{p} Primary School" for p in towns] 

n = len(schools)

attendance = pd.DataFrame({
    "school_name": schools,
    "average_attendance_pct": rng.normal(85, 8, n).clip(50, 100).round(1),
    "county": "Kisumu",
})

infrastructure = pd.DataFrame({
    "school": schools,
    "num_classrooms": rng.integers(6, 25, n).astype(float),
    "water_access": rng.choice(
        ["Borehole", "Piped water", "Rainwater harvesting", "River", "None"], n),
})

attendance.loc[2, "school_name"] = attendance.loc[2, "school_name"].upper()
attendance.loc[5, "school_name"] = attendance.loc[5, "school_name"] + "  "
attendance.loc[8, "school_name"] = attendance.loc[8, "school_name"].replace(" School", "")
attendance.loc[[3, 12], "county"] = "kisumu "

attendance.loc[[4, 11, 20], "average_attendance_pct"] = np.nan

infrastructure.loc[[7, 15], "num_classrooms"] = np.nan

attendance = pd.concat([attendance, attendance.iloc[[9]]], ignore_index=True)

attendance = attendance.drop_duplicates().reset_index(drop=True)

attendance["school_name"] = (
    attendance["school_name"]
    .str.strip()
    .str.title()
)
attendance.loc[~attendance["school_name"].str.endswith("School"), "school_name"] += " School"

attendance["county"] = attendance["county"].str.strip().str.title()

infrastructure["school"] = infrastructure["school"].str.strip().str.title()

merged = pd.merge(
    attendance,
    infrastructure,
    left_on="school_name",
    right_on="school",
    how="inner",
)
merged = merged.drop(columns="school")  

print("======================KISUMU COUNTY SAMPLE SCHOOLS ANALYSIS=====================")
print()
print(merged.head())
print()

analysis = merged.dropna(subset=["average_attendance_pct", "num_classrooms"])

r, p = stats.pearsonr(analysis["num_classrooms"], analysis["average_attendance_pct"])

print(f"Schools analysed: {len(analysis)}")
print(f"Correlation:   {r:.2f}")

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(analysis["num_classrooms"], analysis["average_attendance_pct"],
           color="#1F4E79", s=60)
slope, intercept = np.polyfit(analysis["num_classrooms"], analysis["average_attendance_pct"], 1)
x = np.linspace(analysis["num_classrooms"].min(), analysis["num_classrooms"].max(), 100)
ax.plot(x, slope * x + intercept, color="#FF6B6B", linewidth=2,
        label=f"Trend line (r = {r:.2f})")
ax.set_title("School Attendance vs Number of Classrooms (Kisumu County)")
ax.set_xlabel("Number of classrooms")
ax.set_ylabel("Average attendance (%)")
ax.legend()
plt.tight_layout()
plt.savefig("attendance_vs_classrooms.png", dpi=150)
