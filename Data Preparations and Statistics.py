

import pandas as pd
pd.options.display.max_columns = None
pd.options.display.width = 1000

# Load the CSV file
df = pd.read_csv('cps.csv')

# Convert Zip codes to integers directly in the original DataFrame
df['Zip'] = df['Zip'].astype(int)

# Create a new DataFrame with the required columns
new_df = df[['School_ID', 'Short_Name', 'Is_High_School', 'Zip', 'Student_Count_Total', 'College_Enrollment_Rate_School']].copy()

# Derive Lowest and Highest Grade Offered
def extract_lowest_grade(grades_offered):
    if pd.isna(grades_offered):
        return ''
    grades = str(grades_offered).split(',')
    return grades[0].strip()  # Return the first grade offered

def extract_highest_grade(grades_offered):
    if pd.isna(grades_offered):
        return ''
    grades = str(grades_offered).split(',')
    highest_grade = grades[-1].strip()  # Return the last grade offered
    return highest_grade  # Return the full character or int

new_df.loc[:, 'Lowest_Grade_Offered'] = df['Grades_Offered_All'].apply(extract_lowest_grade)
new_df.loc[:, 'Highest_Grade_Offered'] = df['Grades_Offered_All'].apply(extract_highest_grade)

# Derive Starting Hour - Extract only the first significant digit from time strings
def extract_starting_hour(hour_str):
    if pd.isna(hour_str):
        return ''
    
    hour_str = str(hour_str).lower().strip()
    
    for char in hour_str:
        if char.isdigit() and char != '0':
            return char  # Return the first significant digit found
        elif char == '0' and hour_str[hour_str.index(char) + 1:]:
            for next_char in hour_str[hour_str.index(char) + 1:]:
                if next_char.isdigit() and next_char != '0':
                    return next_char
    
    return ''  # Return empty if no significant digits are found

new_df.loc[:, 'Starting_Hour'] = df['School_Hours'].apply(extract_starting_hour)

# Replace missing numeric values with mean for numeric columns
numeric_columns = ['Student_Count_Total', 'College_Enrollment_Rate_School']
new_df[numeric_columns] = new_df[numeric_columns].fillna(new_df[numeric_columns].mean())

# Display the first 10 rows of the new DataFrame
print("First 10 rows of the new DataFrame:")
print(new_df.head(10))

# Calculate mean and standard deviation of College Enrollment Rate for High Schools
high_schools = new_df[new_df['Is_High_School'] == True]
college_enrollment_stats = high_schools['College_Enrollment_Rate_School'].agg(['mean', 'std'])
print("\nCollege Enrollment Rate for High Schools =", f"{college_enrollment_stats['mean']:.2f}", f"(sd={college_enrollment_stats['std']:.2f})")

# Calculate mean and standard deviation of Total Student Count for non-High Schools
non_high_schools = new_df[new_df['Is_High_School'] == False]
student_count_stats = non_high_schools['Student_Count_Total'].agg(['mean', 'std'])
print("\nTotal Student Count for non-High Schools =", f"{student_count_stats['mean']:.2f}", f"(sd={student_count_stats['std']:.2f})")

# Distribution of starting hours for all schools
starting_hours_dist = new_df['Starting_Hour'].value_counts().sort_index()
print("\nDistribution of Starting Hours:")
for hour, count in starting_hours_dist.items():
    if hour:  # Skip empty strings
        print(f"{hour}am: {count} schools")

# Analyze Zip Codes
zip_codes_of_interest = [60601, 60602, 60603, 60604, 60605, 60606, 60607, 60616]

# Count number of schools outside Loop Neighborhood
schools_outside_loop = df[~df['Zip'].isin(zip_codes_of_interest)]
num_schools_outside_loop = len(schools_outside_loop)
print(f"\nNumber of schools outside of the Loop Neighborhood: {num_schools_outside_loop}")

