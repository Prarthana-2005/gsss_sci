import pandas as pd
from datetime import datetime

# 1. Load dataset
df = pd.read_csv('employee.csv')

# 2. Inspect dataset
print("\n========== Dataset Info ==========")
print(df.info())
print("\n========== Dataset Description ==========")
print(df.describe(include='all'))

# 3. Remove duplicates
df = df.drop_duplicates(subset=['EmpID'])

# 4. Handle missing salaries/job titles (simulate: fill with median salary, 'Unknown' job title)
df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
df['Salary'].fillna(df['Salary'].median(), inplace=True)
df['JobTitle'].fillna('Unknown', inplace=True)

# 5. Standardize department and job titles
dept_map = {
    'HR': 'HR',
    'Finance': 'Finance',
    'IT': 'IT',
    'Sales': 'Sales'
}
job_map = {
    'Software Engg': 'Software Engineer',
    'Software Engineer': 'Software Engineer',
    'Data Scientist': 'Data Scientist',
    'Accountant': 'Accountant',
    'Financial Analyst': 'Financial Analyst',
    'Senior Accountant': 'Senior Accountant',
    'System Administrator': 'System Administrator',
    'Sales Executive': 'Sales Executive',
    'Sales Manager': 'Sales Manager',
    'HR Manager': 'HR Manager',
    'HR Executive': 'HR Executive',
    'Recruiter': 'Recruiter'
}
df['Department'] = df['Department'].map(dept_map).fillna(df['Department'])
df['JobTitle'] = df['JobTitle'].map(job_map).fillna(df['JobTitle'])

# 6. Add YearsOfService column
today = datetime.today()
df['JoiningDate'] = pd.to_datetime(df['JoiningDate'], errors='coerce')
df['YearsOfService'] = ((today - df['JoiningDate']).dt.days / 365).round(1)

# 7. Department Aggregations
dept_summary = df.groupby('Department').agg(
    AvgSalary=('Salary', 'mean'),
    TotalSalary=('Salary', 'sum'),
    EmployeeCount=('EmpID', 'count')
).reset_index()

# 8. Job Title Aggregations
job_summary = df.groupby('JobTitle').agg(
    AvgSalary=('Salary', 'mean'),
    HighestPaid=('Salary', 'max')
).reset_index()

# Highest-paid employee per department
highest_paid = df.loc[df.groupby('Department')['Salary'].idxmax()][['Department', 'EmpID', 'Name', 'Salary']]

# 9. Export summaries
dept_summary.to_csv('dept_summary.csv', index=False)
job_summary.to_csv('job_summary.csv', index=False)
highest_paid.to_csv('highest_paid_per_dept.csv', index=False)

# 10. Beautiful output using tabulate
try:
    from tabulate import tabulate
    print("\n========== Department Summary ==========")
    print(tabulate(dept_summary, headers='keys', tablefmt='fancy_grid', showindex=False))
    print("\n========== Job Title Summary ==========")
    print(tabulate(job_summary, headers='keys', tablefmt='fancy_grid', showindex=False))
    print("\n========== Highest Paid Employee Per Department ==========")
    print(tabulate(highest_paid, headers='keys', tablefmt='fancy_grid', showindex=False))
except ImportError:
    print("\nInstall 'tabulate' for beautiful tables: pip install tabulate")
    print("\nDepartment Summary:\n", dept_summary)
    print("\nJob Title Summary:\n", job_summary)
    print("\nHighest Paid Employee Per Department:\n", highest_paid)

print("\n Data cleaning and aggregation complete.summerise exported.")