# Stack Overflow Developer Survey 2019 – ETL Assignment

## Overview

An ETL pipeline built using Python and Pandas to process the Stack Overflow Developer Survey 2019 dataset and generate reports addressing the following questions:

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

## Run Tests

```powershell
python -m pytest -v
```

## Dataset

[Stack Overflow Developer Survey 2019](https://drive.google.com/file/d/1QOmVDpd8hcVYqqUXDXf68UMDWQZP0wQV/view)

