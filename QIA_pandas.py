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
        month_data = pd.read_csv(csv_file_name, header=None, skiprows=1, names=['date', 'amount', 'description', 'not_known1', 'not_known2','type'],
                       parse_dates=True)
    
        if len(month_data) > 0:
            if bank_data is None:
                bank_data = month_data
            else:
                bank_data = pd.concat([month_data, bank_data])
    print(len(bank_data))
    '''    
    # now we have read the data but the format is not correct, so below
    # we reformat the types to the proper type
    new_bank_data = []
    for index in range(0, len(bank_data)):
        date_str = bank_data[index][0]
        year = int(date_str.split("/")[0])
        month = int(date_str.split("/")[1])
        day = int(date_str.split("/")[2])
        new_row = {
                    'date': date(year, month, day),
                    'amount': float(bank_data[index][1]),
                    'description_1': bank_data[index][2],
                    'description_2': bank_data[index][3],
                    'description_3': bank_data[index][4],
                    'type': bank_data[index][5],
        }
        if new_row['type'] == 'DEBIT':
            new_row['amount'] = new_row['amount'] * -1
        new_bank_data.append(new_row)

    return new_bank_data
    '''

if __name__ == "__main__":
    print("Welcome to QI Pandas Accounting System verion 0.1 by Todd V. Rovito rovitotv@gmail.com")
    # for raspberry pi rwind data is /home/rovitotv/data/QIA
    load_csv_data("/home/rovitotv/data/QIA_data/2020/")
