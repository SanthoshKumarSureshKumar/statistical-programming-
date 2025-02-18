
import pandas as pd

# Set display options
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)

# Load the data
df = pd.read_csv('ss13hil.csv')

# Table 1: Statistics of HINCP grouped by HHT
hht_map = {1: 'Married couple household',
           2: 'Other family household:Male householder, no wife present',
           3: 'Other family household:Female householder, no husband present',
           4: 'Nonfamily household:Male householder:Living alone',
           5: 'Nonfamily household:Female householder:Living alone',
           6: 'Nonfamily household:Male householder:Not living alone',
           7: 'Nonfamily household:Female householder:Not living alone'}

df['HHT_DESC'] = df['HHT'].map(hht_map)
table1 = df.groupby('HHT_DESC')['HINCP'].agg(['mean', 'std', 'count', 'min', 'max']).sort_values('mean', ascending=False)
table1.index.name = 'HHT - Household/family type'

# Table 2: HHL vs ACCESS Frequency Table
hhl_map = {1: 'English only', 2: 'Spanish', 3: 'Other Indo-European languages',
           4: 'Asian and Pacific Island languages', 5: 'Other language'}
access_map = {1: 'Yes w/ Subsrc.', 2: 'Yes, wo/ Subsrc.', 3: 'No'}

df['HHL'] = df['HHL'].map(hhl_map)
df['ACCESS'] = df['ACCESS'].map(access_map)

table2 = pd.pivot_table(df, values='WGTP', index='HHL', columns='ACCESS', 
                        aggfunc='sum', fill_value=0, margins=True)
table2 = table2.div(table2.loc['All', 'All'], axis=0)

# Sort the rows in descending order based on the 'Yes w/ Subsrc.' column
table2_sorted = table2.sort_values(by='Yes w/ Subsrc.', ascending=False)

# Move the 'All' row to the bottom
all_row = table2_sorted.loc['All']
table2_sorted = pd.concat([table2_sorted.drop('All'), pd.DataFrame(all_row).T])

def format_percentage(value):
    return f"{value:.2%}"

table2_sorted = table2_sorted.map(format_percentage)
table2_sorted.index.name = 'HHL - Household language'

# Reorder columns
column_order = ['Yes w/ Subsrc.', 'Yes, wo/ Subsrc.', 'No', 'All']
table2_sorted = table2_sorted.reindex(columns=column_order)

# Table 3: Quantile Analysis of HINCP
df['HINCP_QUANTILE'] = pd.qcut(df['HINCP'], q=3, labels=['low', 'medium', 'high'])
table3 = df.groupby('HINCP_QUANTILE', observed=True).agg({
    'HINCP': ['min', 'max', 'mean'],
    'WGTP': 'sum'
})

# Rename columns
table3.columns = ['min', 'max', 'mean', 'household_count']
table3.index.name = 'HINCP'


# Print results
print("\n*** Table 1 - Descriptive Statistics of HINCP, grouped by HHT ***")
print(table1)
print("\n*** Table 2 - HHL vs. ACCESS - Frequency Table ***")
print(table2_sorted)
print("\n*** Table 3 - Quantile Analysis of HINCP - Household income (past 12 months) ***")
print(table3)
