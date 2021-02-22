import pandas as pd
from os import listdir
from os.path import isfile, join

# docuemtnation URL for pandas 0.22 https://pandas.pydata.org/pandas-docs/version/0.22.0/

def load_csv_data(path_to_data):
    '''
        provided the path to the data load the data but skip the
        first line because it is garbage
    '''
    only_files = [f for f in listdir(path_to_data) if isfile(join(path_to_data, f))]
    only_files.sort()
    bank_data = None
    for file_index in range(0, len(only_files)):
        csv_file_name = path_to_data + "/" + only_files[file_index]
        print("processing %s" % csv_file_name)
        month_data = pd.read_csv(csv_file_name, header=None, skiprows=1, names=['date', 'amount', 'description_1', 
            'description_2', 'description_3','type'],
            parse_dates=True)
    
        if len(month_data) > 0:
            if bank_data is None:
                bank_data = month_data
            else:
                bank_data = pd.concat([month_data, bank_data])
    # this is the power of pandas!
    # we can look up all the transaction type of "DEBIT" and change
    # multiple the amount by -1 in one line of CLEAR CODE
    bank_data.loc[bank_data.type == "DEBIT", 'amount'] *= -1
    return bank_data
    
def read_categories(path_to_categories_csv):
    '''
        reads the categories csv file, which will make it easier
        to assign categories in mass
    '''
    categories = pd.read_csv(path_to_categories_csv, header=None, names=['key','category'])
    return categories
    
def assign_categories(bank_data, categories_data):
    '''
        asigns the categories to each bank_data record based on information
        in categories data
        
        field names: ['date', 'amount', 'description_1', 'description_2', 'description_3','type'],
    '''
    bank_data['category'] = "" # add a new column category
    
    bank_categories = []
    for i in range(0, len(bank_data)):
        category = "unknown"
        for c in range(0, len(categories_data)):
            # check for rent
            if "CHECK " in bank_data.iat[i, 2]:
                if bank_data.iat[i, 1] == -127.00:
                    category = "rent"
                    break
                if bank_data.iat[i, 1] == -160.00:
                    category = "rent"
                    break

            # check categories
            if categories_data.iat[c, 0].lower() in bank_data.iat[i, 2].lower():
                category = categories_data.iat[c, 1]
                break
            elif not pd.isnull(bank_data.iat[i, 3]) and categories_data.iat[c, 0].lower() in bank_data.iat[i, 3].lower():
                category = categories_data.iat[c, 1]
                break
            elif categories_data.iat[c, 0].lower() in bank_data.iat[i, 4].lower():
                category = categories_data.iat[c, 1]
                break
        bank_data.iat[i, 6] = category
    return bank_data


if __name__ == "__main__":
    pd.options.display.width = 300
    pd.options.display.max_rows = 200
    print("Welcome to QI Pandas Accounting System verion 0.2 by Todd V. Rovito rovitotv@gmail.com")
    # for raspberry pi rwind data is /home/rovitotv/data/QIA
    bank_data = load_csv_data("/home/rovitotv/data/QIA_data/2020/")
    print("Number of bank_data rows: %d" % len(bank_data))
    categories_data = read_categories("/home/rovitotv/data/QIA_data/categories.csv")
    print("Number of categories_data rows: %d" % len(categories_data))
    bank_data = assign_categories(bank_data, categories_data)
    # print unknowns and total $ amount on unknowns
    # print(bank_data)
    # pandas sure does make this easy!
    print("summary by category")
    print(bank_data.groupby('category')['amount'].sum())
    bank_data_unknown = bank_data.query('category == "unknown"').sort_values(by=('date'), ascending=True)
    print("Number of unknowns: %d" % len(bank_data_unknown))
    print(bank_data_unknown)