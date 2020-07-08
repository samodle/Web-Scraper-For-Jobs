from WebScraper import IndeedScrapeHelper
from WebScraper import MonsterScrapeHelper
import csv
import datetime
from CensusData import CityData as city
import boto3

# CUSTOMIZE YOUR SCRAPING BY EDITING THESE VARIABLES
master_list_of_search_terms = ('customer support', 'customer experience', 'data center', 'help desk', 'technician',
                               'slack', 'server', 'recruiter', 'computer', 'product', 'assistant', 'genius')

search_terms = master_list_of_search_terms[0:10]
custom_search_locations = (('Washington', 'DC'), ('New York', 'NY'), ('Chicago', 'IL'), ('San Jose', 'CA'))
pages = 20
num_cities = 50
jobs_per_csv = 10000
next_file_save_count = jobs_per_csv

search_locations_usa = city.import_city_data()
# These parameters affect how the scrape will run
only_do_one = True  # if only_do_one is true, the scrape will query 1 indeed search page

# Select websites to scrape posts from
scrape_indeed = False
scrape_monster = True

# only does one or the other (ie csv || db export)
export_to_csv = True  # as opposed to printing data in the console
export_to_db = False

use_custom_locations = False  # option to enter your own search locations instead of picking n top locations

# DB parameters
table_name_jobs = "JobPost"

# variables
master_job_list = []
master_monster_job_list = []

# specify the url
if not only_do_one:
    for term in search_terms:
        print('Scraping...' + term)
        if use_custom_locations:
            for locale in custom_search_locations:
                print('        ...' + locale[0] + ' ' + locale[1])
                for page in range(0, pages):
                    target_url = IndeedScrapeHelper.get_indeed_url(term, page, locale[0], locale[1])
                    master_job_list.append(IndeedScrapeHelper.get_indeed_job_posts(target_url, term))
                    print('                 pg ' + str(page + 1))
        else:  # using Census data for cities, sorted by population
            for city in range(0, num_cities):
                print('        ...' + search_locations_usa.loc[city, 'city'] + ' ' + search_locations_usa.loc[
                    city, 'state_id'])
                for page in range(0, pages):
                    target_url = IndeedScrapeHelper.get_indeed_url(term, page, search_locations_usa.loc[city, 'city'],
                                                                   search_locations_usa.loc[city, 'state_id'])
                    master_job_list.append(IndeedScrapeHelper.get_indeed_job_posts(target_url, term))
                    print('                 pg ' + str(page + 1))
else:
    if scrape_indeed:
        target_url = IndeedScrapeHelper.get_indeed_url(search_terms[0], 1, search_locations_usa.loc[0, 'city'],
                                                       search_locations_usa.loc[0, 'state_id'])
        master_job_list.append(IndeedScrapeHelper.get_indeed_job_posts(target_url, search_terms[0]))
    if scrape_monster:
        target_monster_url = MonsterScrapeHelper.get_monster_url(search_terms[0], 1, search_locations_usa.loc[0, 'city'],
                                                       search_locations_usa.loc[0, 'state_id'])
        master_monster_job_list.append(IndeedScrapeHelper.get_indeed_job_posts(target_monster_url, search_terms[0]))

if export_to_csv:
    now = datetime.datetime.now()
    new_csv_file = open(
        "IndeedJobPostExport-" + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + ".csv", "w",
        newline='')
    writer = csv.writer(new_csv_file)
    fields = ['Name', 'Company', 'Location', 'Indeed Company Rating', 'Salary', 'Commitment', 'URL', 'Description',
              'Search Term', 'Date of Scrape', 'Source']
    writer.writerow(fields)
elif export_to_db:
    # Creating the DynamoDB Client
    dynamodb_client = boto3.client('dynamodb')
    # Creating the DynamoDB Table Resource
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name_jobs)

# how many did we find

print('Scrape complete.  Beginning to write data.')

job_found_count = 0
csv_file_count: int = 0

for x in master_job_list:
    try:
        job_found_count = job_found_count + len(x)
        print('Jobs Found: ' + str(len(x)) + ', Net: ' + str(job_found_count))
        print('csv files generated: ' + str(csv_file_count))
        if job_found_count > next_file_save_count:
            new_csv_file.close()
            csv_file_count += 1
            next_file_save_count += jobs_per_csv
            now = datetime.datetime.now()
            new_csv_file = open(
                "IndeedJobPostExport-" + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + "-" + str(csv_file_count) + ".csv", "w",
                newline='')
            writer = csv.writer(new_csv_file)
            writer.writerow(fields)
    except:
        print(' oops  ')
    for y in x:
        try:
            IndeedScrapeHelper.complete_job_profile(y)
        except:
            print(IndeedScrapeHelper.print_error_string(
                'Error completing Job Profile. URL: ' + y.url))
        else:
            if export_to_csv:
                try:
                    new_row = [y.job_title, y.company, y.location, y.company_rating, y.salary, y.commitment_level,
                               y.url,
                               y.description.encode('unicode_escape', errors='replace'), y.search_term,
                               str(y.last_update),
                               y.source]
                    writer.writerow(new_row)
                    print('Writing: ' + y.job_title)
                except Exception as e:
                    print(IndeedScrapeHelper.print_error_string(
                        'csv error: ' + y.job_title + ' ' + y.search_term + ' ' + y.location))
            elif export_to_db:
                try:
                    with table.batch_writer() as batch:
                        batch.put_item(
                            Item={
                                "JobTitle": y.job_title,
                                "CompanyID": 0,
                                "company": y.company,
                                "location": y.location,
                                "rating": y.company_rating,
                                "salary": y.salary,
                                "commitment": y.commitment_level,
                                "url": y.url,
                                "search_term": y.search_term,
                                "source": y.source,
                                "description": y.description.encode('unicode_escape', errors='replace')
                            }
                        )

                except Exception as e:
                    print(IndeedScrapeHelper.print_error_string(
                        'database error: ' + y.job_title + ' ' + y.search_term + ' ' + y.location + '\n' + str(e)))
            else:
                print(str(y))

if export_to_csv:
    new_csv_file.close()

