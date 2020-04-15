import IndeedScrapeHelper
import csv
import datetime
import CityData as city
import pandas as pd
from JobPostModule import JobPost

# CUSTOMIZE YOUR SCRAPING BY EDITING THESE VARIABLES
search_terms = ('customer support', 'customer experience', 'amazon')  #  'data science', 'data center', 'IT', , 'microsoft', 'google', 'facebook', 'zoom', 'slack'
custom_search_locations = (('Washington', 'DC'), ('New York', 'NY'), ('Chicago', 'IL'), ('San Jose', 'CA'))
pages = 1
num_cities = 10

search_locations_usa = city.import_city_data()
# These parameters affect how the scrape will run
only_do_one = False  # if only_do_one is true, the scrape will query 1 indeed search page
export_to_csv = True  # as opposed to printing data in the console
use_custom_locations = False  # option to enter your own search locations instead of picking n top locations

# variables
master_job_list = []

# specify the url
if not only_do_one:
    for term in search_terms:
        print('Scraping...' + term)
        if use_custom_locations:
            for locale in custom_search_locations:
                print('        ...' + locale[0] + ' ' + locale[1])
                for page in range(0, pages):
                    target_url = IndeedScrapeHelper.get_indeed_url(term, page, locale[0], locale[1])
                    master_job_list.append(IndeedScrapeHelper.get_indeed_urls(target_url))
                    print('                 pg ' + str(page))
        else:  # using Census data for cities, sorted by population
            for city in range(0, num_cities):
                print('        ...' + search_locations_usa.loc[city, 'city'] + ' ' + search_locations_usa.loc[city, 'state_id'])
                for page in range(0, pages):
                    target_url = IndeedScrapeHelper.get_indeed_url(term, page, search_locations_usa.loc[city, 'city'], search_locations_usa.loc[city, 'state_id'])
                    master_job_list.append(IndeedScrapeHelper.get_indeed_urls(target_url))
                    print('                 pg ' + str(page))
else:
    target_url = IndeedScrapeHelper.get_indeed_url(search_terms[0], 1, search_locations_usa.loc[0, 'city'],
                                                   search_locations_usa.loc[0, 'state_id'])
    master_job_list.append(IndeedScrapeHelper.get_indeed_urls(target_url))

if export_to_csv:
    now = datetime.datetime.now()
    new_csv_file = open(
        "IndeedJobPostExport-" + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + ".csv", "w",
        newline='')
    writer = csv.writer(new_csv_file)
    fields = ['Name', 'Company', 'Location', 'Indeed Company Rating', 'Salary', 'Commitment', 'URL', 'Description']
    writer.writerow(fields)

print('Scrape complete.  Beginning to write data.')

for x in master_job_list:
    for y in x:
        IndeedScrapeHelper.complete_job_profile(y)
        if export_to_csv:
            #  new_row = [y.job_title, y.company, y.location, y.company_rating, y.salary, y.commitment_level, y.url,
            #           y.description.encode('utf-8', errors='replace')]
            new_row = [y.job_title, y.company, y.location, y.company_rating, y.salary, y.commitment_level, y.url,
                       y.description.encode('unicode_escape', errors='replace')]
            writer.writerow(new_row)
        else:
            print(str(y))

if export_to_csv:
    new_csv_file.close()

"""
███████╗ ██████╗ ██████╗ ██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██║ ██╔╝
█████╗  ██║   ██║██████╔╝█████╔╝
██╔══╝  ██║   ██║██╔══██╗██╔═██╗
██║     ╚██████╔╝██║  ██║██║  ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝                 
"""
