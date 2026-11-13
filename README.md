# Stack Overflow Developer Survey 2019 – ETL Assignment

## Overview

An ETL pipeline built using Python and Pandas to process the Stack Overflow Developer Survey 2019 dataset and generate reports addressing six questions:

1. Average age at which developers wrote their first line of code.
2. Percentage of developers who knew Python in each country.
3. Average developer salary by continent.
4. Most desired programming language for 2020.
5. Hobbyist developers by gender and continent.
6. Job and career satisfaction by gender and continent.

The pipeline generates seven CSV reports.

## Prerequisites

- Python 3.13
- Git

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Kaushal1122/etl-assignment.git
cd etl-assignment
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Add the dataset

Download the Stack Overflow Developer Survey 2019 dataset and place `survey_results_public.csv` inside the `data/` directory.

Expected location:

```text
data/survey_results_public.csv
```

### 5. Run the ETL pipeline

Set the Python module search path:

```powershell
$env:PYTHONPATH = "src"
```

Execute:

```powershell
python -m main
```

The generated CSV reports will be saved in the `reports/` directory.

## Results

The following results were generated from the 2019 survey dataset.

### 1. Average age when developers started coding

The average age at which developers wrote their first line of code was **15.46 years**.

Output: `average_age_first_code.csv`

### 2. Python knowledge percentage by country

The percentage represents the proportion of valid survey respondents in each country who reported knowing Python.

**Filtering rule:** Countries with fewer than 10 valid respondents are excluded from the report. This minimum threshold avoids misleading percentages based on very small sample sizes.

| Country | Total Respondents | Python Developers | Python Percentage |
|---|---:|---:|---:|
| Uganda | 72 | 47 | 65.28% |
| Iceland | 48 | 30 | 62.50% |
| Cuba | 29 | 16 | 55.17% |
| Oman | 11 | 6 | 54.55% |
| Republic of Korea | 37 | 20 | 54.05% |

Output: `python_percentage_by_country.csv`

### 3. Average developer salary by continent

Both average and median salaries are reported in USD.

| Continent | Respondents | Average Salary (USD) | Median Salary (USD) |
|---|---:|---:|---:|
| North America | 18,010 | 225,667.25 | 100,300 |
| Oceania | 1,606 | 166,950.96 | 76,156 |
| Europe | 23,793 | 96,978.01 | 49,722 |
| Asia | 8,612 | 37,691.13 | 13,993 |
| Africa | 1,257 | 35,045.78 | 13,116 |
| South America | 2,484 | 32,691.80 | 18,348 |

Output: `average_salary_by_continent.csv`

### 4. Most desired programming languages for 2020

The five most desired programming languages were:

| Language | Respondents |
|---|---:|
| JavaScript | 44,739 |
| Python | 40,006 |
| HTML/CSS | 36,645 |
| SQL | 33,566 |
| TypeScript | 23,720 |

Output: `most_desired_language.csv`

### 5. Hobbyist developers by gender and continent

The report groups hobbyist developers into MAN, WOMAN, and OTHERS categories. Missing gender responses are excluded.

| Continent | Gender | Hobbyist Count |
|---|---|---:|
| Africa | MAN | 1,928 |
| Africa | OTHERS | 28 |
| Africa | WOMAN | 125 |
| Asia | MAN | 12,645 |
| Asia | OTHERS | 170 |
| Asia | WOMAN | 766 |

Output: `hobbyist_by_gender_and_continent.csv`

### 6. Job and career satisfaction by gender and continent

The reports contain respondent counts for five satisfaction levels.

**Job satisfaction**

| Continent | Gender | Very Dissatisfied | Slightly Dissatisfied | Neither | Slightly Satisfied | Very Satisfied | Total |
|---|---|---:|---:|---:|---:|---:|---:|
| Africa | MAN | 137 | 259 | 242 | 540 | 352 | 1,530 |
| Africa | OTHERS | 4 | 3 | 2 | 5 | 2 | 16 |
| Africa | WOMAN | 21 | 19 | 16 | 30 | 29 | 115 |

Output: `job_satisfaction.csv`

**Career satisfaction**

| Continent | Gender | Very Dissatisfied | Slightly Dissatisfied | Neither | Slightly Satisfied | Very Satisfied | Total |
|---|---|---:|---:|---:|---:|---:|---:|
| Africa | MAN | 126 | 184 | 212 | 566 | 583 | 1,671 |
| Africa | OTHERS | 2 | 4 | 4 | 6 | 2 | 18 |
| Africa | WOMAN | 15 | 19 | 4 | 41 | 41 | 120 |

Output: `career_satisfaction.csv`

## Run Tests

```powershell
python -m pytest -v
```

## Dataset

[Stack Overflow Developer Survey 2019](https://drive.google.com/file/d/1QOmVDpd8hcVYqqUXDXf68UMDWQZP0wQV/view)
