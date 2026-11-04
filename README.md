# File: README.md

# Multi Dataset Analysis

This script analyses sample data of Kisumu county Schools. 
Calculates the correlation of the schools infrustructure and class attendance datasets. 


## What It Does

- Loads two related datasets from sample DataFrames(attendance, infrustructure)
- Cleans, then merges the datasets on school name
- Calculates the correlation of class attendance vs shool infrustructure
- Plots the scatter plot for visual representation 


## Setup

```bash
pip install -r requirements.txt
```


## Usage

Run the program from the project's folder

```
python msa_microfinance_analysis.py
```


## How It Works

```Python

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
```


## Sample Output

```
======================KISUMU COUNTY SAMPLE SCHOOLS ANALYSIS=====================

               school_name  average_attendance_pct  county  num_classrooms          water_access
0  Nyalenda Primary School                    87.4  Kisumu            23.0  Rainwater harvesting
1   Kondele Primary School                    76.7  Kisumu            20.0                  None
2  Manyatta Primary School                    91.0  Kisumu            12.0                  None
3  Milimani Primary School                    92.5  Kisumu            24.0           Piped water
4  Mamboleo Primary School                     NaN  Kisumu            13.0                  None

Schools analysed: 25
Correlation:   -0.00

```

## Stack

Python, Pandas, Numpy 


