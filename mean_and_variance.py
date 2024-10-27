# initialising everthing
numbers = []    # List to store input numbers
count = 0       # Counter for number of inputs
mean = 0        # Variable to store the running mean
var=0           # Variable to store the running variance

# starting the while loop
while True:
    num = int(input("Enter a number, To exit give a negative number:  "))# Get user input
    
    if num < 0: # Exit loop if negative number is entered
        break
        
    numbers.append(num) # Add the number to the list
    count += 1          # Increment the counter
    
# For the first number, mean is the number itself and variance is 0
    if count == 1:
        mean = num
        print("Mean is ", mean)
        print("Variance is ",var)
        print("\n") #giving white space
        
# For subsequent numbers, update mean and variance
    else:
        prev_mean = mean    # Store the previous mean
        mean = prev_mean + (num - prev_mean)/count  # Update mean using formula
        print("Mean is ", mean)
      
        # Update variance using formula 
        var = ((count-2)/(count-1)) * var + ((num - prev_mean)**2)/count
        print("Variance is ",var)
        print("\n")
        
        