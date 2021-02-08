'''
    Qualia Insights Accouting System V0.1

    By: Todd V. Rovito rovitotv@gmail.com

    Seems to work with Python 3!

Copyright (c) 2018, Todd V. Rovito and Linda L. Rovito
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import csv
import matplotlib # this code imports matplotlib without OpenGL
#matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from os import listdir
from os.path import isfile, join

def load_csv_data(path_to_data):
    '''
        provided the path to the data load the data but skip the
        first line because it is garbage
    '''
    only_files = [f for f in listdir(path_to_data) if isfile(join(path_to_data, f))]
    only_files.sort()
    bank_data = []
    for file_index in range(0, len(only_files)):
        csv_file_name = path_to_data + "/" + only_files[file_index]
        print("processing %s" % csv_file_name)
        with open(csv_file_name, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader, None) # skip the first row
            for row in csv_reader:
                bank_data.append(row)
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

def load_csv_data_multiple_years(path_to_data, start_year, end_year):
    '''
        provided the path to the data load the data but skip the
        first line because it is garbage.  start_year and end_year are
        provided to give user control over how many years of data required.
    '''
    bank_data = []
    new_bank_data = []
    for year_index in range(start_year, end_year+1):
        path = path_to_data + "/" + str(year_index) + "/"
        only_files = [f for f in listdir(path) if isfile(join(path, f))]
        only_files.sort()
        for file_index in range(0, len(only_files)):
            csv_file_name = path + "/" + only_files[file_index]
            print("processing %s" % csv_file_name)
            with open(csv_file_name, "r") as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader, None) # skip the first row
                for row in csv_reader:
                    bank_data.append(row)
        # now we have read the data but the format is not correct, so below
        # we reformat the types to the proper type
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

def read_categories(path_to_categories_csv):
    '''
        reads the categories csv file, which will make it easier
        to assign categories in mass
    '''
    categories = []
    with open(path_to_categories_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            categories.append(row)

    return categories

def assign_categories(bank_data, categories):
    '''
        asigns the categories to each bank_data record based on information
        in categories data
    '''
    bank_categories = []
    for i in range(0, len(bank_data)):
        category = "unknown"
        for c in range(0, len(categories)):
            # check for rent
            if "CHECK " in bank_data[i]['description_1']:
                if bank_data[i]['amount'] == -127.00:
                    category = "rent"
                    break
                if bank_data[i]['amount'] == -160.00:
                    category = "rent"
                    break

            # check categories
            if categories[c][0].lower() in bank_data[i]['description_1'].lower():
                category = categories[c][1]
                break
            elif categories[c][0].lower() in bank_data[i]['description_2'].lower():
                category = categories[c][1]
                break
            elif categories[c][0].lower() in bank_data[i]['description_3'].lower():
                category = categories[c][1]
                break
        bank_categories.append(category)


    return bank_categories

def print_unknown(bank_data, bank_categories):
    '''
        scans bank_categories looking for unknowns and printing them
    '''
    unknown_count = 0
    print("index\t\tdate\t\t\tamount\tdesccription_1\tdescription_2")
    for i in range(0, len(bank_data)):
        if bank_categories[i] == "unknown":
            print("%d\t\t\t%s\t$%5.2f\t%s\t%s" % (i, bank_data[i]['date'],
                bank_data[i]['amount'],
                bank_data[i]['description_1'],
                bank_data[i]['description_2']))
            unknown_count += 1
    print("unknown count/total count: %d/%d" % (unknown_count, len(bank_data)))

def print_bank_data(bank_data, bank_categories, month, year):
    '''
        print bank data and category for a given month and year.  This function
        is useful to figure out how data is being catorgized.
    '''
    print("index\t\tdate\t\t\tamount\t\t\t\tcategory\t\t\t\tdescription")
    for i in range(0, len(bank_data)):
        if bank_data[i]['date'].month == month and bank_data[i]['date'].year == year:
            print("%d\t\t\t%s\t$%5.2f\t\t\t\t%s\t\t\t\t%s" % (i, bank_data[i]['date'],
                bank_data[i]['amount'],
                bank_categories[i],
                bank_data[i]['description_1']))

def print_category_total(bank_data, bank_categories, year, month_start, month_end, make_plot = False):
        '''
            This function pretty prints the category totals by year, month and category.
        '''
        # gather all the data and put everything into a dictionary
        category_total = {}
        for bank_index in range(0, len(bank_data)):
            if bank_data[bank_index]['date'].year == year:
                if bank_data[bank_index]['date'].month >= month_start:
                    if bank_data[bank_index]['date'].month <= month_end:
                        # month range is correct now see if category exists as a dict key
                        if bank_categories[bank_index] in category_total.keys():
                            category_total[bank_categories[bank_index]] = category_total[bank_categories[bank_index]] + bank_data[bank_index]['amount']
                        else:
                            category_total[bank_categories[bank_index]] = bank_data[bank_index]['amount']

		# now that we have gathered the data lets pretty print the results
        print("year: %d month start: %d month end: %d" % (year, month_start, month_end))
        print("{0:20} {1:10}".format("category", "total"))
        profit = 0
        #for category_key in category_total:
        for category_key in sorted(category_total):
            #print("{0:20} {1:10f}".format(category_key, category_total[category_key]))
            print("{0:20}  ${1:,.2f}".format(category_key, category_total[category_key]))
            profit += category_total[category_key]

        print("{0:20} ${1:,.2f}".format("profit:", profit))

        # create a plot if enabled
        if make_plot:
            category_list = list(category_total.values())
            category_name = list(category_total.keys())
            fix, ax = plt.subplots()
            width = 0.35
            N = len(category_list)
            ind = np.arange(N)
            rects1 = ax.bar(ind, category_list, width, color='y')
            ax.set_ylabel('Amount')
            ax.set_title('Category Amount from Month %d to %d' % (month_start, month_end))
            ax.set_xticks(ind + (width/2))
            ax.set_xticklabels(category_name, rotation=90)
            plt.tight_layout()
            plt.show()

def html_categories_for_year(bank_data, bank_categories, html_directory):
	'''
		This function will create a html file of the categories by each month.
		html syntax for a table that is ugly
    <tr>
    <th>Firstname</th>
    <th>Lastname</th>
    <th>Age</th>
  </tr>
	'''
	html_header = '''
<!DOCTYPE html>
<html>
<head>
<style>
table, th, td {
    border: 1px solid black;
}
</style>
</head>
<body>

<table style="width:100%">
	'''

	html_footer = '''
</body>
</html>
	'''
	# go through the bank_data make html_detail files and adding up category totals
	html_file_name = html_directory + "/qia_categories_summary_table.html"
	html = ""
	with open(html_file_name, 'w') as html_file:
		html_file.write(html_header)
		# gather all the data and put everything into a dictionary
		category_total = {}
		for bank_index in range(0, len(bank_data)):
			if bank_categories[bank_index] in category_total.keys():
				category_total[bank_categories[bank_index]] = category_total[bank_categories[bank_index]] + bank_data[bank_index]['amount']
				# add the details to the html_detail_file
				html_detail_file_name = html_directory + "/" + bank_categories[bank_index] + ".html"
				with open(html_detail_file_name, 'a') as html_detail_file:
					html += "<tr>"
					html += "<td>%s</td><td>%06.2f</td><td>%s</td><td>%s</td><td>%s</td>" % (bank_data[bank_index]['date'],
						bank_data[bank_index]['amount'], bank_data[bank_index]['description_1'], bank_data[bank_index]['description_2'],
						bank_data[bank_index]['type'])
					html += "</tr>\n"
					html_detail_file.write(html)
					html = ""
			else:
				# new category so we have to create a record in the data dictionary
				# also need to create a new file because we have not seen it before
				category_total[bank_categories[bank_index]] = bank_data[bank_index]['amount']
				html_detail_file_name = html_directory + "/" + bank_categories[bank_index] + ".html"
				with open(html_detail_file_name, 'w') as html_detail_file:
					html_detail_file.write(html_header)
					html += "<p>\n"
					html += "<tr>"
					html += "<td><b>Date</b></td><td><b>Amount</b></td><td><b>Description_1</b></td><td><b>Description_2</b></td><td><b>Type</b></td>"
					html += "</tr>\n"
					html += "<tr>"
					html += "<td>%s</td><td>%06.2f</td><td>%s</td><td>%s</td><td>%s</td>" % (bank_data[bank_index]['date'],
						bank_data[bank_index]['amount'], bank_data[bank_index]['description_1'], bank_data[bank_index]['description_2'],
						bank_data[bank_index]['type'])
					html += "</tr>\n"
					html_detail_file.write(html)
					html = ""

		# sort the dictionary category_total and place into a list
		# https://stackoverflow.com/questions/20577840/python-dictionary-sorting-in-descending-order-based-on-values
		category_total_sorted_keys = sorted(category_total, key=category_total.get, reverse=True)

		# now we have to go through each of the categories and write a total line
		# close the table and the html_footer for the html_detail files
		for category_key in category_total_sorted_keys:
			html_detail_file_name = html_directory + "/" + category_key + ".html"
			with open(html_detail_file_name, 'a') as html_detail_file:
				# make a total line
				html = ""
				html += "<tr>"
				html += ("<td><b>Total</b></td><td><b>$%6.2f</b></td>" % category_total[category_key])
				html += "</tr>\n"
				html += "</table>\n"
				html += "</p>\n"
				html_detail_file.write(html)
				html_detail_file.write(html_footer)

		# now that we have gathered the data lets pretty print the results in a summary table
		# include a link to the detail file in the summary table
		# <a href="url">link text</a>
		profit = 0.0
		html = ""
		html += "<p>"
		html += "<tr>"
		html += "<td><b>Category</b></td><td><b>Amount</b></td>"
		html += "</tr>\n"
		for category_key in category_total_sorted_keys:
			html += "<tr>"
			html += ("<td><a href='./%s.html'>" % category_key)
			html += "{0:20}</a></td><td>${1:,.2f}</td>".format(category_key, category_total[category_key])
			html += "</tr>\n"
			#print("{0:20}  ${1:,.2f}".format(category_key, category_total[category_key]))
			profit += category_total[category_key]

		# make a profit line
		html += "<tr>"
		html += ("<td><b>Profit</b></td><td><b>$%6.2f</b></td>" % profit)
		html += "</tr>\n"
		html += "</table>\n"
		html += "</p>\n"
		html_file.write(html)

		# make a graph and save to a file
		#category_list = list(category_total.values())
		#category_name = list(category_total.keys())
		category_list = []
		category_name = []
		for category_key in category_total_sorted_keys:
			category_list.append(category_total[category_key])
			category_name.append(category_key)
		fix, ax = plt.subplots()
		width = 0.35
		N = len(category_list)
		ind = np.arange(N)
		rects1 = ax.bar(ind, category_list, width, color='y')
		ax.set_ylabel('Amount')
		ax.set_title('Category Amount from Month %d to %d' % (1, 12))
		ax.set_xticks(ind + (width/2))
		ax.set_xticklabels(category_name, rotation=90)
		plt.tight_layout()
		plt.savefig(html_directory + "/category_plot.png")

		#html = "<p><img src='category_plot.png' alt='category plot' width='500' height='377'></p>\n"
		html = "<p><img src='category_plot.png' alt='category plot' width=800 height=400></p>\n"
		html_file.write(html)
		html_file.write(html_footer)

if __name__ == "__main__":
    print("Welcome to QI Accounting System verion 0.1 by Todd V. Rovito rovitotv@gmail.com")
    # each year we have to change the year(s) as needed now we are working on 2017
    # we could use argparse and pass in a number of arguments but that is difficult to do
    # with iPad

    platform = "ChromeOS" # set this variable to platform "Pythonista" or "ChromeOS"
    if platform == "pythonista":
        # For Pythonista to get directory below you have to go into stash and do "echo $HOME"
        # maybe the path_to_data variable should be a command line argument? Then
        # program would work in Pythonista if called from command line and Raspberry Pi?
        path_to_data = '/private/var/mobile/Containers/Shared/AppGroup/524B360A-7D33-4D59-AF5D-C869970F37F4/Pythonista3/Documents/QIA/data/'
        bank_data = load_csv_data(path_to_data + "2017/")
        categories = read_categories(path_to_data + "categories.csv")
        bank_data_categories = assign_categories(bank_data, categories)
        print_unknown(bank_data, bank_data_categories)
        print_category_total(bank_data, bank_data_categories, 2017, 1, 12, True)
        html_categories_for_year(bank_data, bank_data_categories,
            "/private/var/mobile/Containers/Shared/AppGroup/524B360A-7D33-4D59-AF5D-C869970F37F4/Pythonista3/Documents/temp/")
    elif platform == "ChromeOS":
        # you have to change the user name to the appropriate user in your Crouton environment
        path_to_data = "/home/rovitotv/data/QIA_data/"
        bank_data = load_csv_data_multiple_years(path_to_data, 2017, 2019)
        categories = read_categories(path_to_data + "categories.csv")
        bank_data_categories = assign_categories(bank_data, categories)
        print_unknown(bank_data, bank_data_categories)
        # print_bank_data(bank_data, bank_data_categories, 6, 2019)
        print_category_total(bank_data, bank_data_categories, 2019, 1, 12, False)
