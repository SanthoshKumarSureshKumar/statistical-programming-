print("DATA-51100, Fall 2024")
print("NAME: Santhosh Kumar Suresh Kumar")
print("PROGRAMMING ASSIGNMENT #3")
print("\n")

import numpy as np

def load_data(filename):
    # Load data from CSV file and split into features and labels
    data = np.loadtxt(filename, delimiter=',', dtype=str)
    features = data[:, :4].astype(float)  # First 4 columns as floats
    labels = data[:, 4]  # Last column as strings
    return features, labels

def find_nearest_neighbor(train_features, test_features):
    # Calculate distances between test point and all training points
    # Using broadcasting to compute distances efficiently
    diff = train_features[:, np.newaxis] - test_features
    distances = np.sqrt(np.sum(diff**2, axis=2))
    # Find index of minimum distance for each test point
    return np.argmin(distances.T, axis=1)

def main():
    # Print column headers
    print("\n#, True, Predicted")

    # Load training and testing data
    train_features, train_labels = load_data('iris-training-data.csv')
    test_features, test_labels = load_data('iris-testing-data.csv')

    # Find nearest neighbors
    nearest_indices = find_nearest_neighbor(train_features, test_features)
    
    # Get predictions using nearest neighbor indices
    predictions = train_labels[nearest_indices]

    # Print results
    for i, (true_label, pred_label) in enumerate(zip(test_labels, predictions), 1):
        print(f"{i},{true_label},{pred_label}")

    # Calculate and print accuracy
    accuracy = np.mean(predictions == test_labels) * 100
    print(f"\nAccuracy: {accuracy:.2f}%")

# Call the main function
main()