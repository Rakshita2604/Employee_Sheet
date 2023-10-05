import pandas as pd

sheet_id = '1YN293Ie0V2Yddj-A742w7QwQoMyI2XsE'

df = pd.read_csv(
    f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")


print(df)
# Assuming that the column names in your CSV match the following
# You may need to adjust these column names based on your actual data
# Example: 'position status', 'time', 'time out', etc.
df.columns = [
    'position_ID', 'position_status', 'time', 'time_out', 'time_card_hours',
    'pay_cycle_start_date', 'pay_cycle_end_date', 'employee_name',
    'file_number'
]

# Sort the data by employee name and time
df.sort_values(['employee_name', 'time'], inplace=True)


# Convert 'time' and 'time_out' to datetime objects
df['time'] = pd.to_datetime(df['time'],format='%m/%d/%Y %H:%M %p')
df['time_out'] = pd.to_datetime(df['time_out'],format='%m/%d/%Y %H:%M %p')

# Calculate time differences between consecutive rows
df['time_diff'] = df.groupby('employee_name')['time'].diff()
df['time_abc']= df.groupby('employee_name')['time'].diff()


# Filter employees who worked for 7 consecutive days
consecutive_days = df[df['time_diff'].dt.days >= 1].groupby('employee_name').size()
employees_with_7_days = consecutive_days[consecutive_days >= 6].index.tolist()


# Filter employees with less than 10 hours between shifts but greater than 1 hour
df['time_diff_hours'] = df['time_diff'].dt.total_seconds() / 3600
short_breaks = df[(df['time_diff_hours'] < 10) &
(df['time_diff_hours'] > 1)]['employee_name'].unique()


# Filter employees who worked for more than 14 hours in a single shift
df['time_card_hours'] = df['time_abc'].dt.total_seconds() / 3600
long_shifts = df[df['time_card_hours'] > 14]['employee_name'].unique()


# Print the results
print("Employees who worked for 7 consecutive days:")
for employee in employees_with_7_days:
    print(employee)

print("\nEmployees with less than 10 hours between shifts but greater than 1 hour:")
for employee in short_breaks:
    print(employee)

print("\nEmployees who worked for more than 14 hours in a single shift:")
for employee in long_shifts:
   print(employee)
