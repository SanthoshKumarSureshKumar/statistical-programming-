

# Importing necessary libraries
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def map_taxes(tax_values):
    tax_map = create_tax_mapping()
    return [tax_map.get(val, np.NaN) for val in tax_values]

def create_tax_mapping():
    tax_map = {1: np.NaN, 2: 1, 63: 5500}
    increment = 50
    for i in range(3, 23):
        tax_map[i] = increment
        increment += 50
    for i in range(23, 63):
        tax_map[i] = increment + 50
        increment += 100
    increment -= 50
    for i in range(64, 69):
        tax_map[i] = increment + 1000
        increment += 1000
    return tax_map

def main():
    # Loading ss13hil.csv file using read_csv()
    dataset = pd.read_csv('ss13hil.csv')

    ''' Creating a 2x2 subplot layout within a figure, setting spacing and size '''
    figure, axis = plt.subplots(2, 2)
    figure.subplots_adjust(hspace=0.32)  # Adjust horizontal space between subplots
    figure.set_size_inches(14, 7)  # Set the figure size to 14x7 inches

    # Then creating a pie chart in the first subplot (top left):

    # Title for the pie chart
    axis[0, 0].set_title('Household Languages', fontsize=8)
    # Counting distinct values in the 'HHL' column, and ignoring NaN with dropna()
    language_distribution = dataset['HHL'].value_counts().dropna()
    languages = ['English only', 'Spanish', 'Other Indo-European', 'Asian and Pacific Island languages', 'Other']
    # Creating a pie chart
    axis[0, 0].pie(language_distribution, startangle=242)
    axis[0, 0].legend(languages, loc=2, fontsize=8)
    # Checking if the pie chart is circular
    axis[0, 0].axis('equal')

    # Then on the second subplot, creating a histogram and KDE (top right)

    # Title
    axis[0, 1].set_title('Distribution of Household Income', fontsize=8)
    # X-axis label
    axis[0, 1].set_xlabel('Household Income($)- Log Scaled', fontsize=8)
    # Y-axis label
    axis[0, 1].set_ylabel('Density', fontsize=8)
    # Dropping NaN values from 'HINCP' for plotting using dropna()
    income_data = dataset['HINCP'].dropna()
    # Creating 100 log-spaced bins
    log_bins = np.logspace(1, 7, 100)
    # And then setting x-axis to log scale
    axis[0, 1].set_xscale('log')
    density_ticks = np.arange(0, 0.000025, step=0.000005)
    # Setting Y-axis ticks
    axis[0, 1].set_yticks(density_ticks)
    # Formatting Y-axis labels
    axis[0, 1].set_yticklabels(['{:,.6f}'.format(x) for x in density_ticks], fontsize="small")
    # Using hist() to plot histogram with KDE
    axis[0, 1].hist(income_data, bins=log_bins, density=True, color='green', alpha=0.5)
    income_data.plot(kind='kde', ax=axis[0, 1], color='black', linestyle='--')

    # Creating a bar chart on the third subplot (bottom left)

    # Title
    axis[1, 0].set_title('Vehicles Available in Households', fontsize=8)
    # X-axis label
    axis[1, 0].set_xlabel('# of Vehicles', fontsize=8)
    # Y-axis label
    axis[1, 0].set_ylabel('Thousands of Households', fontsize=8)
    # Here, First we are grouping the data by 'VEH' and then summing up 'WGTP', then converting to thousands
    vehicles = dataset.groupby('VEH')['WGTP'].sum() / 1000
    # Plotting barchart for vehicles
    axis[1, 0].bar(vehicles.index, vehicles.values, color='red')

    # Creating a scatter plot on the fourth subplot (bottom right)

    # Title
    axis[1, 1].set_title('Property Taxes vs Property Values', fontsize=8)
    # X-axis label
    axis[1, 1].set_xlabel('Property Values($)', fontsize=8)
    # Y-axis label
    axis[1, 1].set_ylabel('Taxes($)', fontsize=8)
    # Dropping NaN from selected columns
    property_values = dataset['VALP']
    taxes = map_taxes(dataset['TAXP'])
    mortgage = dataset['MRGP']
    weight = dataset['WGTP']
    scatter = axis[1, 1].scatter(
        property_values, 
        taxes, 
        c=mortgage, 
        s=weight / 10,  # Adjust weight to increase marker size
        alpha=0.25, 
        cmap='seismic', 
        marker='o'
    )
    axis[1, 1].set_xlim(0, 1200000)  # Set limits to ensure proper scaling
    axis[1, 1].set_ylim(0, 11000)
    axis[1, 1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: str(int(x))))  # Format x-axis ticks without commas
    color_bar = plt.colorbar(scatter, ax=axis[1, 1])
    color_bar.set_label('First Mortgage Payment (Monthly $)')

    # Saving and showing the plot
    plt.savefig('pums.png', dpi=100)
    plt.show()

main()
