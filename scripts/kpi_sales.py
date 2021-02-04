import csv
from datetime import datetime

# Display the start date of script execution
print(datetime.now())

# Load data
input_file = open("data/randomized-transactions-202009.psv",
                  mode='r')

# Skip the header row of input data
next(input_file)

# Initialize two dictionaries: the first to store the store code and the turnover, then a second to store the couple
# (store code, product code) and the associate's turnover
code_magasin_ca = {}
codes_magasin_produit_ca = {}

# Browse the file line by line and save usefuls data to dictionaries to avoid consuming too much RAM
for line in input_file:
    *first_cols, identifiant_produit, code_magasin, _, ca = line.split(
        "|")
    # Set turnover default value in dictionaries to 0 to avoid KeyError if key doesn't exist yet...
    # .. And fill them with the corresponding values of float(ca)
    code_magasin_ca[code_magasin] = code_magasin_ca.get(code_magasin, 0) + float(
        ca)
    codes_magasin_produit_ca[code_magasin][identifiant_produit] = codes_magasin_produit_ca.setdefault(code_magasin,
                                                                                                      {}).setdefault(
        identifiant_produit, 0) + float(ca)

# Sort the first dictionary in descending order, keeping only the first 50 lines
sorted_code_magasin_ca = dict(
    sorted(code_magasin_ca.items(), key=lambda x: x[1], reverse=True)[:50])

# Write data into top-50-stores.csv file
with open('top-50-stores.csv', mode='w', newline='') as cf:
    top50_output = csv.writer(cf, delimiter='|')
    top50_output.writerow(['code_magasin', 'ca'])
    for key, value in sorted_code_magasin_ca.items():
        top50_output.writerow([key, value])

# Sort second dictionary in descending order using turnover, keeping only the first 100 lines of each
# codes_magasin_produit_ca[code_magasin][identifiant_produit]
sorted_codes_magasin_produit_ca = {key: dict(sorted(val.items(), key=lambda ele: ele[1], reverse=True)[:100])
                                   for key, val in codes_magasin_produit_ca.items()}

# Write data into top-products-by-stores/top-100-products-store-{store}.csv file for each store in dictionary
# sorted_codes_magasin_produit_ca
for store in sorted_codes_magasin_produit_ca:
    with open(f'top-products-by-store/top-100-products-store-{store}.csv', mode='w', newline='') as cf:
        top100_output = csv.writer(cf, delimiter='|')
        top100_output.writerow(['code_magasin', 'identifiant_produit', 'ca'])
        for value in sorted_codes_magasin_produit_ca[store]:
            top100_output.writerow(
                [store, value, sorted_codes_magasin_produit_ca[store][value]])

# Display the end date of script execution
print(datetime.now())  # 7 minutes --> 2021-02-04
