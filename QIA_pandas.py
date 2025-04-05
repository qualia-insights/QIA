# QIA - Qualia Insights Accouting 
# Copyright (C) 2025 Todd & Linda Rovito / Qualia Insights, LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import pandas as pd
from os import listdir
from os.path import isfile, join
import pathlib
import pdb
import sys
import locale

# docuemtnation URL for pandas 0.22 https://pandas.pydata.org/pandas-docs/version/0.22.0/
#
# bank data has the following fields:
#        date, amount, description_1, description_2, description_3,type

def load_csv_data(path_to_data):
    '''
        provided the path to the data load the data but skip the
        first line because it is garbage
    '''
    only_files = [f for f in listdir(path_to_data) if isfile(join(path_to_data, f))]
    only_files.sort()
    bank_data = None
    year_to_process_parts = pathlib.Path(path_to_data)
    year_to_process = year_to_process_parts.parts[-1]
    print("year to process: %s" % year_to_process)
    for file_index in range(0, len(only_files)):
        if only_files[file_index].startswith('income_1099' ) or '.swp' in only_files[file_index]:
            continue
        csv_file_name = path_to_data + "/" + only_files[file_index]
        print("processing %s" % csv_file_name)
        month_data = pd.read_csv(csv_file_name, header=None, skiprows=1, names=['date', 'amount', 'description_1',
            'description_2', 'description_3','type'],
            parse_dates=['date'])

        if len(month_data) > 0:
            # we need to check and make sure the data is from the proper year!
            # this in case doo doo brian downloads a csv file outside of the correct range
            start_day = pd.to_datetime('01.01.%s' % year_to_process)
            end_day = pd.to_datetime('12.31.%s' % year_to_process)
            month_data_between = month_data[month_data['date'].between(start_day, end_day)]
            if len(month_data_between) != len(month_data):
                print("month data includes data outside of the year %s" % year_to_process)
                sys.exit(200)
            if bank_data is None:
                bank_data = month_data
            else:
                bank_data = pd.concat([month_data, bank_data])
    # this is the power of pandas!
    # we can look up all the transaction type of "DEBIT" and change
    # multiple the amount by -1 in one line of CLEAR CODE
    bank_data.loc[bank_data.type == "DEBIT", 'amount'] *= -1
    return bank_data

def load_income_1099_csv(path_to_csv_file):
    income_data = pd.read_csv(path_to_csv_file, header=None, skiprows=1, 
            names=['company','tin','amount'])
    return income_data

def read_categories(path_to_categories_csv):
    '''
        reads the categories csv file, which will make it easier
        to assign categories in mass
    '''
    categories = pd.read_csv(path_to_categories_csv, header=None, names=['key','category'])
    return categories

def assign_categories(bank_data, categories_data):
    '''
        assigns the categories to each bank_data record based on information
        in categories data

        field names: ['date', 'amount', 'description_1', 'description_2', 'description_3','type'],

        if a category is mis-classified because of categories.csv not being right add this debug code:
                            if "9969 Debit Card Purchase Loves Travel S00004275 Dayton Oh" in bank_data.iat[i,2]:
                                print("category: %d" % c)

                            in the three if statements starting on line 77
        to print a specific row of the bank_data use this code:
            print(bank_data.iloc[[i]])
    '''
    bank_data['category'] = "" # add a new column category

    bank_categories = []
    for i in range(0, len(bank_data)):
        category = "unknown"
        #if i == 426:
        #    print(bank_data.iloc[[i]])
        for c in range(0, len(categories_data)):
            # check for rent
            if "CHECK " in bank_data.iat[i, 2]:
                if bank_data.iat[i, 1] == -127.00:
                    category = "rent"
                    break
                if bank_data.iat[i, 1] == -160.00:
                    category = "rent"
                    break
                if bank_data.iat[i, 1] == -240.00:
                    category = "rent"
                    break
                if "CHECK 143  REF. NO. 096162985" in bank_data.iat[i, 2]:
                    # for Taxes in 2020
                    category = "dont_count"
                if "CHECK 144  REF. NO. 090826555" in bank_data.iat[i, 2]:
                    # for Taxes in 2020
                    category = "income"
                if "CHECK 147  REF. NO. L095758546" in bank_data.iat[i, 2]:
                    # for Taxes in 2021 client refund
                    category = "income"
                if "CHECK 148  REF. NO. 096175978" in bank_data.iat[i, 2]:
                    # for Taxes in 2021 check to Rovitos
                    category = "dont_count"
                if "CHECK 7215  REF. NO. 096709526" in bank_data.iat[i, 2]:
                    # for Taxes in 2021 check to Rovitos
                    category = "liscensing"
                if "CHECK 149  REF. NO. 089600434" in bank_data.iat[i, 2]:
                    # for Taxes in 2021 client refund
                    category = "income"
                if "CHECK 150  REF. NO. 095795498" in bank_data.iat[i, 2]:
                    # for Taxes in 2021 client refund
                    category = "income"
                if "CHECK 151  REF. NO. 095557625" in bank_data.iat[i, 2]:
                    # for Taxes in 2021 check to Rovitos
                    category = "dont_count"

            # check categories
            if categories_data.iat[c, 0].lower() in bank_data.iat[i, 2].lower():
                category = categories_data.iat[c, 1]
                break
            elif not pd.isnull(bank_data.iat[i, 3]) and categories_data.iat[c, 0].lower() in bank_data.iat[i, 3].lower():
                category = categories_data.iat[c, 1]
                break
            elif not pd.isnull(bank_data.iat[i, 4]) and categories_data.iat[c, 0].lower() in bank_data.iat[i, 4].lower():
                category = categories_data.iat[c, 1]
                break
        bank_data.iat[i, 6] = category
    return bank_data

# ******************************************************************************
# Debug functions to help figure out what categories things are in
def output_bank_data_sort_date_as_csv(bank_data, file_name):
    # fields:
    #   date, amount, description_1, description_2, description_3,type
    # output bank data
    bank_data.sort_values(by=('date'), ascending=True).to_csv(file_name)

def output_bank_data_filter_sort_date_as_csv(bank_data, category, file_name):
    # example of how you dump out a single category to see the detail as a csv file
    # trying to figure out why the postage is a positive $600 that is very odd
    category_data = bank_data.query('category == "%s"' % category).sort_values(by=('date'), ascending=True)
    category_data.to_csv(file_name)

def output_bank_data_filter_description_contains_sort_date_as_csv(bank_data, contains_str, file_name):
    contains_data = bank_data[bank_data['description_1'].str.contains(contains_str)].sort_values(by=('date'), ascending=True)
    contains_data.to_csv(file_name)

if __name__ == "__main__":
    print(locale.setlocale(locale.LC_ALL, ''))
    pd.options.display.width = 300
    pd.options.display.max_rows = 1000
    # options below make every float shown with print use commas
    pd.options.display.float_format = '{:,.2f}'.format 
    # pd.options.display.float_format = '${:,.2f}'.format # if you want to include $
    data_directory = "/home/rovitotv/code/qualia_insights/QIA_data/2024/"
    print("Welcome to QI Pandas Accounting System 2024 by Todd V. Rovito rovitotv@gmail.com")
    # for raspberry pi rwind data is /home/rovitotv/data/QIA
    bank_data = load_csv_data(data_directory)
    print("Number of bank_data rows: %d" % len(bank_data))
    categories_data = read_categories("/home/rovitotv/data/QIA_data/categories.csv")
    print("Number of categories_data rows: %d" % len(categories_data))
    bank_data = assign_categories(bank_data, categories_data)
    print("bank data with cateegories")
    print(bank_data.sort_values(by=('date'), ascending=True))
    # print unknowns and total $ amount on unknowns
    # print(bank_data)
    # pandas sure does make this easy!
    print("summary by category==============================================================================================")
    print(bank_data.groupby('category')['amount'].sum())
    total = bank_data['amount'].sum()
    print("Total (profit or loss): %s" % locale.currency(total, grouping=True))
    bank_data_dont_count = bank_data.query('category == "dont_count"')
    total_dont_count = bank_data_dont_count['amount'].sum()
    total_with_out_dont_count = total - total_dont_count
    print("Total (profit or loss) without dont_count: %s" % 
        locale.currency(total_with_out_dont_count, grouping=True))
    print("unknowns=========================================================================================================")
    bank_data_unknown = bank_data.query('category == "unknown"').sort_values(by=('date'), ascending=True)
    if len(bank_data_unknown) > 0:
        #print(bank_data_unknown)
        # field names: ['date', 'amount', 'description_1', 'description_2', 'description_3','type'],
        print(bank_data_unknown[['date','amount','description_1']])
    print("Number of unknowns: %d" % len(bank_data_unknown))
    print("Business Income - Gross Receipts================================================================================")
    income_data_1099_MISC = load_income_1099_csv(data_directory + "income_1099-MISC.csv")
    income_data_1099_NEC = load_income_1099_csv(data_directory + "income_1099-NEC.csv")
    income_data_1099_K = load_income_1099_csv(data_directory + "income_1099-K.csv")
    bank_data_income = bank_data.query('category == "income"')
    income_gross = bank_data_income['amount'].sum()
    income_1099_MISC = income_data_1099_MISC['amount'].sum()
    income_1099_NEC = income_data_1099_NEC['amount'].sum()
    income_1099_K = income_data_1099_K['amount'].sum()
    income_not_reports_1099 = income_gross - income_1099_MISC - income_1099_NEC - income_1099_K
    # print("Income Gross: $%9.2f" % income_gross)
    print("Income Gross: %s" % locale.currency(income_gross, grouping=True))
    print("Income 1099_NEC: %s" % locale.currency(income_1099_NEC, grouping=True))
    print("Income 1099_K: %s" % locale.currency(income_1099_K, grouping=True))
    print("Income 1099_MISC: %s" % locale.currency(income_1099_MISC, grouping=True))
    print("Gross receipts (not reports on form 1099-NEC, 1099-MISC or 1099-K): %s" 
            % locale.currency(income_not_reports_1099, grouping=True))

    # output_bank_data_filter_description_contains_sort_date_as_csv(bank_data, "CHECK", "/home/rovitotv/temp/bank_data_check.csv")
    output_bank_data_sort_date_as_csv(bank_data, "/home/rovitotv/temp/bank_data_all.csv")
