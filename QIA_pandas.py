import pandas as pd
from os import listdir
from os.path import isfile, join

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
    '''
    categories = []
    with open(path_to_categories_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            categories.append(row)
    '''
    return categories

if __name__ == "__main__":
    print("Welcome to QI Pandas Accounting System verion 0.2 by Todd V. Rovito rovitotv@gmail.com")
    # for raspberry pi rwind data is /home/rovitotv/data/QIA
    bank_data = load_csv_data("/home/rovitotv/data/QIA_data/2020/")
    categories_data = read_categories("/home/rovitotv/data/QIA_data/categories.csv")