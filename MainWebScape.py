from WebScraper import Indeed
from WebScraper import Monster
from WebScraper import ScrapeHelper
import csv
import datetime
from CensusData import CityData as city
from pymongo import MongoClient
import time

start_time = time.time()

# CUSTOMIZE YOUR SCRAPING BY EDITING THESE VARIABLES
master_list_of_search_terms2 = ['unilever']
master_list_of_search_terms3 = ['customer support', 'customer experience', 'data center', 'help desk', 'technician',
                                'retail', 'sales']
search_terms = [
    'supervisor', 'manager', 'project', 'developer', 'customer support', 'customer experience', 'data center', 'help desk', 'technician',
    'slack', 'server', 'recruiter', 'computer', 'product', 'assistant', 'genius', 'retail', 'sales']

custom_search_locations = (('Washington', 'DC'), ('New York', 'NY'), ('Chicago', 'IL'), ('San Jose', 'CA'))
pages = 5
num_cities = 30
jobs_per_csv = 10000
next_file_save_count = jobs_per_csv

search_locations_usa = city.import_city_data()
# These parameters affect how the scrape will run
only_do_one = True  # if only_do_one is true, the scrape will query 1 search page

# Select websites to scrape posts from
scrape_indeed = True
scrape_monster = True
scrape_career_builder = False

# only does one or the other (ie csv || db export)
export_to_csv = False  # as opposed to printing data in the console
export_to_mongo = True

use_custom_locations = False  # option to enter your own search locations instead of picking n top locations

monster_pages = 10  # min(10, pages)  # monster can't handle more than 10 pages

# DB parameters
# table_name_jobs = "JobPost"

# variables
master_job_list = []
jobs_found = 0

# specify the url
for term in search_terms:
    # location agnostic
    if scrape_indeed:
        for page in range(0, pages):
            target_url = Indeed.get_url(term, page)
            temp_list = Indeed.get_job_posts(target_url, term)
            jobs_found = jobs_found + len(temp_list)
            master_job_list.append(temp_list)
            print('Indeed No Location pg ' + str(page + 1) + ', Jobs: ' + str(len(temp_list)))
    if scrape_monster:
        target_url = Monster.get_url(term, monster_pages)
        temp_list = Monster.get_job_posts(target_url, term)
        jobs_found = jobs_found + temp_list.count
        master_job_list.append(temp_list)
        print('Monster No Location Page' + ', Jobs: ' + str(len(temp_list)))
    # specific locations
    print('Scraping...' + term)
    if use_custom_locations:
        for locale in custom_search_locations:
            print('        ...' + locale[0] + ' ' + locale[1])
            if scrape_indeed:
                for page in range(0, pages):
                    target_url = Indeed.get_url(term, page, locale[0], locale[1])
                    temp_list = Indeed.get_job_posts(target_url, term)
                    jobs_found = jobs_found + len(temp_list)
                    master_job_list.append(temp_list)
                    print('Indeed             pg ' + str(page + 1) + ', Jobs: ' + str(len(temp_list)))
            if scrape_monster:
                target_url = Monster.get_url(term, monster_pages, locale[0], locale[1])
                temp_list = Monster.get_job_posts(target_url, term)
                jobs_found = jobs_found + len(temp_list)
                master_job_list.append(Monster.get_job_posts(temp_list))
                print('Monster' + ', Jobs: ' + str(len(temp_list)))
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

if export_to_csv:
    now = datetime.datetime.now()
    new_csv_file = open(
        "ForkJobExport-" + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + ".csv", "w",
        newline='')
    writer = csv.writer(new_csv_file)
    fields = ['Name', 'Company', 'Location', 'Indeed Company Rating', 'Salary', 'Commitment', 'URL', 'Description',
              'Search Term', 'Date Scraped', 'Source']
    writer.writerow(fields)

if export_to_mongo:
    client = MongoClient('localhost', 27017, username='forkAdmin', password='ForkAdmin123')
    db = client.jobs
    collection = db.job_descriptions

runtime_in_seconds = round(time.time() - start_time, 1)
print('Scrape complete.  Beginning to write data. Scraping time: ' + str(runtime_in_seconds) + ' secs')

job_found_count = 0
csv_file_count: int = 0

for x in master_job_list:
    try:
        runtime_in_seconds = round(time.time() - start_time, 1)
        runtime_in_minutes = runtime_in_seconds / 60
        job_found_count = job_found_count + len(x)
        pct_complete = round(job_found_count / jobs_found, 3)*100
        print(str(pct_complete) + '% Complete. ' + str(runtime_in_minutes) + ' Minutes. Jobs Saved: ' + str(len(x)) + ', Net: ' + str(job_found_count))
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
    except Exception as e:
        print(str(e))
    for y in x:
        try:
            if y.source is ScrapeHelper.INDEED:
                Indeed.complete_job_profile(y)
            elif y.source is ScrapeHelper.MONSTER:
                Monster.complete_job_profile(y)
        except Exception as e:
            print(ScrapeHelper.print_error_string(
                'Error completing Job Profile. URL: ' + y.url))
        else:
            if export_to_csv:
                try:
                    new_row = [y.job_title, y.company, y.location, y.company_rating, y.salary, y.commitment_level,
                               y.url,
                               y.description, y.search_term,
                               str(y.last_update),
                               y.source]
                    writer.writerow(new_row)
                    print('Writing: ' + y.job_title)
                except Exception as e:
                    print(ScrapeHelper.print_error_string(
                        'csv error: ' + y.job_title + ' ' + y.search_term + ' ' + y.location + str(e)))
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
                try:
                    collection.insert_one(new_jd)
                except Exception as e:
                    ScrapeHelper.print_error_string(str(e))

print('Fork Data Export - 100% Complete')
if export_to_csv:
    new_csv_file.close()
