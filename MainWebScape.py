from WebScraper import Indeed
from WebScraper import Monster
from WebScraper import ScrapeHelper
import csv
import datetime
from CensusData import CityData as city
from pymongo import MongoClient

# import boto3

# CUSTOMIZE YOUR SCRAPING BY EDITING THESE VARIABLES
master_list_of_search_terms = ('unilever')
master_list_of_search_terms3 = ('customer support', 'customer experience', 'data center', 'help desk', 'technician', 'retail', 'sales')
master_list_of_search_terms2 = (
    'unilever', 'customer support', 'customer experience', 'data center', 'help desk', 'technician',
    'slack', 'server', 'recruiter', 'computer', 'product', 'assistant', 'genius', 'retail', 'sales')

search_terms = master_list_of_search_terms[0:10]
custom_search_locations = (('Washington', 'DC'), ('New York', 'NY'), ('Chicago', 'IL'), ('San Jose', 'CA'))
pages = 4
num_cities = 10
jobs_per_csv = 10000
next_file_save_count = jobs_per_csv

search_locations_usa = city.import_city_data()
# These parameters affect how the scrape will run
only_do_one = True  # if only_do_one is true, the scrape will query 1 search page

# Select websites to scrape posts from
scrape_indeed = True
scrape_monster = True

# only does one or the other (ie csv || db export)
export_to_csv = True  # as opposed to printing data in the console
# export_to_db = False # AWS
export_to_mongo = False

use_custom_locations = False  # option to enter your own search locations instead of picking n top locations

monster_pages = 10  # min(10, pages)  # monster can't handle more than 10 pages
# DB parameters
# table_name_jobs = "JobPost"

# variables
master_job_list = []

# specify the url
if not only_do_one:
    for term in search_terms:
        print('Scraping...' + term)
        if use_custom_locations:
            for locale in custom_search_locations:
                print('        ...' + locale[0] + ' ' + locale[1])
                if scrape_indeed:
                    for page in range(0, pages):
                        target_url = Indeed.get_url(term, page, locale[0], locale[1])
                        master_job_list.append(Indeed.get_job_posts(target_url, term))
                        print('Indeed             pg ' + str(page + 1))
                if scrape_monster:
                    target_url = Monster.get_url(term, monster_pages, locale[0], locale[1])
                    master_job_list.append(Monster.get_job_posts(target_url, term))
                    print('Monster Page')
        else:  # using Census data for cities, sorted by population
            for city in range(0, num_cities):
                print('        ...' + search_locations_usa.loc[city, 'city'] + ' ' + search_locations_usa.loc[
                    city, 'state_id'])
                if scrape_indeed:
                    for page in range(0, pages):
                        target_url = Indeed.get_url(term, page, search_locations_usa.loc[city, 'city'],
                                                    search_locations_usa.loc[city, 'state_id'])
                        master_job_list.append(Indeed.get_job_posts(target_url, term))
                        print('Indeed            pg ' + str(page + 1))
                if scrape_monster:
                    target_url = Monster.get_url(term, monster_pages, search_locations_usa.loc[city, 'city'],
                                                 search_locations_usa.loc[city, 'state_id'])
                    master_job_list.append(Monster.get_job_posts(target_url, term))
                    print('Monster Page')
else:
    if scrape_indeed:
        target_url = Indeed.get_url(search_terms[0], 1, search_locations_usa.loc[0, 'city'],
                                    search_locations_usa.loc[0, 'state_id'])
        master_job_list.append(Indeed.get_job_posts(target_url, search_terms[0]))
    if scrape_monster:
        target_url = Monster.get_url(search_terms[0], 1, search_locations_usa.loc[0, 'city'],
                                     search_locations_usa.loc[0, 'state_id'])
        master_job_list.append(Monster.get_job_posts(target_url, search_terms[0]))

if export_to_csv:
    now = datetime.datetime.now()
    new_csv_file = open(
        "ForkJobExport-" + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + ".csv", "w",
        newline='')
    writer = csv.writer(new_csv_file)
    fields = ['Name', 'Company', 'Location', 'Indeed Company Rating', 'Salary', 'Commitment', 'URL', 'Description',
              'Search Term', 'Date Scraped', 'Source']
    writer.writerow(fields)
# elif export_to_db:
# Creating the DynamoDB Client
# dynamodb_client = boto3.client('dynamodb')
# Creating the DynamoDB Table Resource
# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table(table_name_jobs)
if export_to_mongo:
    client = MongoClient('localhost', 27017, username='forkAdmin', password='ForkAdmin123')
    db = client.jobs
    collection = db.job_descriptions

print('Scrape complete.  Beginning to write data.')

job_found_count = 0
csv_file_count: int = 0

for x in master_job_list:
    try:
        job_found_count = job_found_count + len(x)
        print('Jobs Found: ' + str(len(x)) + ', Net: ' + str(job_found_count))
        if export_to_csv:
            print('csv files generated: ' + str(csv_file_count))
            if job_found_count > next_file_save_count:
                new_csv_file.close()
                csv_file_count += 1
                next_file_save_count += jobs_per_csv
                now = datetime.datetime.now()
                new_csv_file = open(
                    "ForkJobExport-" + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + "-" + str(
                        csv_file_count) + ".csv", "w",
                    newline='')
                writer = csv.writer(new_csv_file)
                writer.writerow(fields)
    except:
        print(' oops  ')
    for y in x:
        try:
            if y.source is ScrapeHelper.INDEED:
                Indeed.complete_job_profile(y)
            elif y.source is ScrapeHelper.MONSTER:
                Monster.complete_job_profile(y)
        except:
            print(Indeed.print_error_string(
                'Error completing Job Profile. URL: ' + y.url))
        else:
            if export_to_csv:
                try:
                    new_row = [y.job_title, y.company, y.location, y.company_rating, y.salary, y.commitment_level,
                               y.url,
                               y.description.encode('UTF-8', errors='ignore'), y.search_term,
                               str(y.last_update),
                               y.source]
                    writer.writerow(new_row)
                    print('Writing: ' + y.job_title)
                except Exception as e:
                    print(ScrapeHelper.print_error_string(
                        'csv error: ' + y.job_title + ' ' + y.search_term + ' ' + y.location))

            if export_to_mongo:
                new_jd = {
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
                    "description": y.description
                }
                collection.insert_one(new_jd)
            # elif export_to_db:
            #    try:
            #        with table.batch_writer() as batch:
            #            batch.put_item(
            #                Item={
            #                    "JobTitle": y.job_title,
            #                    "CompanyID": 0,
            #                    "company": y.company,
            #                    "location": y.location,
            #                    "rating": y.company_rating,
            #                    "salary": y.salary,
            #                    "commitment": y.commitment_level,
            #                    "url": y.url,
            #                    "search_term": y.search_term,
            #                    "source": y.source,
            #                    "description": y.description.encode('UTF-8', errors='ignore')
            #                }
            #            )
            #    except Exception as e:
            #        print(Indeed.print_error_string(
            #            'database error: ' + y.job_title + ' ' + y.search_term + ' ' + y.location + '\n' + str(e)))
            # else:
            #    print(str(y))

print('Fork Data Export - 100% Complete')
if export_to_csv:
    new_csv_file.close()
