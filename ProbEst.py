print("DATA-51100, Fall 2024")
print("NAME: Santhosh Kumar Suresh Kumar")
print("PROGRAMMING ASSIGNMENT #4")
print("\n")

# Import pandas library for data manipulation
import pandas as pd

# Load the cars dataset from CSV file
cars_df = pd.read_csv('cars.csv')

# Extract unique makes and aspiration types
makes = cars_df['make'].unique()
aspirations = cars_df['aspiration'].unique()


# Calculate and display conditional probabilities of aspiration by make
for make in makes:
    # Create subset of cars for current make
    make_subset = cars_df[cars_df['make'] == make]
    total_make_count = len(make_subset)
    
    # Iterate through aspiration types
    for aspiration in aspirations:
        # Count cars with specific make and aspiration
        aspiration_count = len(make_subset[make_subset['aspiration'] == aspiration])
        
        # Calculate and print conditional probability
        prob = (aspiration_count / total_make_count) * 100
        print(f"Prob(aspiration={aspiration}|make={make}) = {prob:.2f}%")
        
# Add a blank line between the two output groups        
print()
        
# Calculate and display probabilities of makes
total_cars = len(cars_df)
for make in makes:
    # Count cars for each make and calculate probability
    make_count = len(cars_df[cars_df['make'] == make])
    prob = (make_count / total_cars) * 100
    print(f"Prob(make={make}) = {prob:.2f}%")