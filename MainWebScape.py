from WebScraper import Indeed
from WebScraper import Monster
from WebScraper import ScrapeHelper
import csv
import datetime
from CensusData import CityData as city
from pymongo import MongoClient
import logging  # Setting up the loggings to monitor execution time
from time import time  # To time our operations
import ForkConfig as Fork

# set up mechanism for timing how long the program takes to execute
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt='%H:%M:%S', level=logging.INFO)
t = time()

# initialize in process variables
next_file_save_count = Fork.jobs_per_csv
search_locations_usa = city.import_city_data()
master_job_list = []
jobs_found = 0
monster_pages = 10  # monster can't handle more than 10 'pages'

# STEP 1: IDENTIFY AND SCRAPE THE URLS TO PREPARE FOR STEP 2
for term in Fork.search_terms:  # for each term specific above, go through the following steps

    # always start with a generic, location agnostic search
    if Fork.scrape_indeed:
        for page in range(0, Fork.pages):  # iterate through each page
            # determine the URL for the desired query
            target_url = Indeed.get_url(term, page)

            # scrape the JDs from that query
            temp_list = Indeed.get_job_posts(target_url, term)
            jobs_found = jobs_found + len(temp_list)

            # add the JDs to our list
            master_job_list.append(temp_list)
            print('Indeed No Location pg ' + str(page + 1) + ', Jobs: ' + str(len(temp_list)))
    if Fork.scrape_monster:
        # determine the URL for the desired query
        target_url = Monster.get_url(term, monster_pages)

        # scrape the JDs from that query
        temp_list = Monster.get_job_posts(target_url, term)
        jobs_found = jobs_found + len(temp_list)

        # add the JDs to our list of lists
        master_job_list.append(temp_list)
        print('Monster No Location Page' + ', Jobs: ' + str(len(temp_list)))
    # specific locations
    print('Scraping...' + term)
    if Fork.use_custom_locations:
        for locale in Fork.custom_search_locations:
            print('        ...' + locale[0] + ' ' + locale[1])

            if Fork.scrape_indeed:
                for page in range(0, Fork.pages):  # iterate through each page
                    # determine the URL for the desired query
                    target_url = Indeed.get_url(term, page, locale[0], locale[1])

                    # scrape the JDs from that query
                    temp_list = Indeed.get_job_posts(target_url, term)
                    jobs_found = jobs_found + len(temp_list)

                    # add the JDs to our list of lists
                    master_job_list.append(temp_list)
                    print('Indeed             pg ' + str(page + 1) + ', Jobs: ' + str(len(temp_list)))

            if Fork.scrape_monster:
                # determine the URL for the desired query
                target_url = Monster.get_url(term, monster_pages, locale[0], locale[1])

                # scrape the JDs from that query
                temp_list = Monster.get_job_posts(target_url, term)
                jobs_found = jobs_found + len(temp_list)

                # add the JDs to our list of lists
                master_job_list.append(temp_list)
                print('Monster' + ', Jobs: ' + str(len(temp_list)))

    else:  # using Census data for cities, sorted by population

        for city in range(0, Fork.num_cities):
            print('        ...' + search_locations_usa.loc[city, 'city'] + ' ' + search_locations_usa.loc[
                city, 'state_id'])

            if Fork.scrape_indeed:
                for page in range(0, Fork.pages):
                    # determine the URL for the desired query
                    target_url = Indeed.get_url(term, page, search_locations_usa.loc[city, 'city'],
                                                search_locations_usa.loc[city, 'state_id'])

                    # scrape the JDs from that query
                    temp_list = Indeed.get_job_posts(target_url, term)
                    jobs_found = jobs_found + len(temp_list)
                    master_job_list.append(temp_list)
                    print('Indeed            pg ' + str(page + 1) + ', Jobs: ' + str(len(temp_list)))

            if Fork.scrape_monster:
                # determine the URL for the desired query
                target_url = Monster.get_url(term, monster_pages, search_locations_usa.loc[city, 'city'],
                                             search_locations_usa.loc[city, 'state_id'])

                # scrape the JDs from that query
                temp_list = Monster.get_job_posts(target_url, term)
                jobs_found = jobs_found + len(temp_list)

                # add the JDs to our list of lists
                master_job_list.append(temp_list)
                print('Monster Page' + ', Jobs: ' + str(len(temp_list)))

# if saving the data as a .csv, initialize the .csv writing
if Fork.export_to_csv:
    now = datetime.datetime.now()
    new_csv_file = open(
        "ForkJobExport-" + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + ".csv", "w",
        newline='')
    writer = csv.writer(new_csv_file)
    fields = ['Name', 'Company', 'Location', 'Indeed Company Rating', 'Salary', 'Commitment', 'URL', 'Description',
              'Search Term', 'Date Scraped', 'Source']
    writer.writerow(fields)

# if saving the database, open db connection
if Fork.export_to_mongo:
    client = MongoClient(Fork.MONGO_HOST, Fork.MONGO_PORT, Fork.MONGO_USERNAME, Fork.MONGO_PASSWORD)
    db = client.jobs
    collection = db.job_descriptions

# status update
print('Scrape complete. Jobs Found: ' + str(jobs_found))
print('Time to scrape: {} min'.format(round((time() - t) / 60, 2)))

job_found_count = 0
csv_file_count: int = 0

# STEP 2: SCRAPE COMPLETE JOB DESCRIPTIONS, EXPORT THE SCRAPED JOB DESCRIPTIONS
for x in master_job_list:
    try:
        # status update
        job_found_count = job_found_count + len(x)
        pct_complete = round(job_found_count / jobs_found, 3)*100
        print(str(pct_complete) + '% Complete. ' + ' Jobs Saved: ' + str(len(x)) + ', Net: ' + str(job_found_count) + ' / ' + str(jobs_found))
        print('Execution Time: {} min'.format(round((time() - t) / 60, 2)))

        if Fork.export_to_csv:
            print('csv files generated: ' + str(csv_file_count))  # status update

            # check if the current csv file has exceeded it's capacity, if so create a new one
            if job_found_count > next_file_save_count:
                new_csv_file.close()  # this csv file is complete
                csv_file_count += 1
                next_file_save_count += Fork.jobs_per_csv

                # start a new csv file
                now = datetime.datetime.now()
                new_csv_file = open(
                    "ForkJobExport-" + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + "-" + str(
                        csv_file_count) + ".csv", "w",
                    newline='')
                writer = csv.writer(new_csv_file)
                writer.writerow(fields)
    except Exception as e:
        ScrapeHelper.print_error_string(str(e))  # print the error, try the next one

    # iterate through each list of JDs
    for y in x:
        try:
            # scrape the JD based on the URL from the list
            if y.source is ScrapeHelper.INDEED:
                Indeed.complete_job_profile(y)
            elif y.source is ScrapeHelper.MONSTER:
                Monster.complete_job_profile(y)
        except Exception as e:
            print(ScrapeHelper.print_error_string(
                'Error completing Job Profile. URL: ' + y.url + ' // ' + str(e)))
        else:
            # save to csv
            if Fork.export_to_csv:
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

            # save to db
            if Fork.export_to_mongo:
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

if Fork.export_to_csv:
    new_csv_file.close()

print('Fork Data Export - 100% Complete.  Execution Time: {} min'.format(round((time() - t) / 60, 2)))
