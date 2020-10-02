import multiprocessing
from Classes.JobPostModule import JobPost
from WebScraper import Indeed
from WebScraper import Monster
from WebScraper import ScrapeHelper
from WebScraper import CareerBuilder
from CensusData import CityData
from pymongo import MongoClient
from time import time  # To time our operations
import ForkConfig as Fork
import database as ForkDB
from concurrent.futures import ProcessPoolExecutor, as_completed

if __name__ == '__main__':
    # freeze_support()  # include this if packaging as stand alone app/freezing
    # set up mechanism for timing how long the program takes to execute
    t = time()

    # initialize in process variables
    master_job_list = []
    jobs_found = 0
    cores = multiprocessing.cpu_count()  # Count the number of cores in a computer
    job_list = []

    if Fork.use_professions_as_search_terms:
        df = ForkDB.get_all_professions()
        if Fork.use_only_target_occupations:
            df = df.loc[df['Name'].isin(Fork.target_occupations)]
        if Fork.query_alternate_titles:
            df = df[['AlternateNames']]
            search_terms = []
            for item in df['AlternateNames'].values:
                search_terms.extend(item)
        else:
            search_terms = df['Name']
    else:
        search_terms = Fork.search_terms

    print('Initialization Complete. Beginning Job URL Scrape. Time: {} min'.format(round((time() - t) / 60, 2)))

    # first, perform location agnostic search
    if Fork.scrape_indeed:
        for i in range(0, Fork.pages):
            with ProcessPoolExecutor(max_workers=cores - 1) as executor:
                futures = [executor.submit(Indeed.get_job_list, term, i) for term in search_terms]
                for result in as_completed(futures):
                    master_job_list.append(result.result())
            print('Indeed URLs Scraped pg ' + str(i) + ': {} min'.format(round((time() - t) / 60, 2)))

    if Fork.scrape_monster:
        with ProcessPoolExecutor(max_workers=cores - 1) as executor:
            futures = [executor.submit(Monster.get_job_list, term) for term in search_terms]
            for result in as_completed(futures):
                master_job_list.append(result.result())
        print('Monster URLs Scraped: {} min'.format(round((time() - t) / 60, 2)))

    if Fork.scrape_career_builder:
        with ProcessPoolExecutor(max_workers=cores - 1) as executor:
            futures = [executor.submit(CareerBuilder.get_job_list, term) for term in search_terms]
            for result in as_completed(futures):
                master_job_list.append(result.result())
        print('CareerBuilder URLs Scraped: {} min'.format(round((time() - t) / 60, 2)))

    # specific locations
    if Fork.use_custom_locations:
        for locale in Fork.custom_search_locations:
            print('        ...' + locale[0] + ' ' + locale[1])
            if Fork.scrape_indeed:
                for i in range(0, Fork.pages):
                    with ProcessPoolExecutor(max_workers=cores - 1) as executor:
                        futures = [executor.submit(Indeed.get_job_list, term, i, locale[0], locale[1]) for term in
                                   search_terms]
                        for result in as_completed(futures):
                            master_job_list.append(result.result())
                    print('           ' + 'Indeed URLs pg ' + str(i) + ': {} min'.format(round((time() - t) / 60, 2)))

            if Fork.scrape_monster:
                with ProcessPoolExecutor(max_workers=cores - 1) as executor:
                    futures = [executor.submit(Monster.get_job_list, term, locale[0], locale[1]) for term in
                               search_terms]
                    for result in as_completed(futures):
                        master_job_list.append(result.result())
                print('           ' + 'Monster URLs: {} min'.format(round((time() - t) / 60, 2)))

            if Fork.scrape_career_builder:
                with ProcessPoolExecutor(max_workers=cores - 1) as executor:
                    futures = [executor.submit(CareerBuilder.get_job_list, term, locale[0], locale[1]) for term in
                               search_terms]
                    for result in as_completed(futures):
                        master_job_list.append(result.result())
                print('           ' + 'CareerBuilder URLs: {} min'.format(round((time() - t) / 60, 2)))

    if Fork.scrape_census_locations:  # using Census data for cities, sorted by population

        locations = CityData.import_city_data()

        for city in range(0, Fork.num_cities):
            print('        ...' + locations.loc[city, 'city'] + ' ' + locations.loc[
                city, 'state_id'] + ', ' + str(city + 1) + '/' + str(Fork.num_cities))

            if Fork.scrape_indeed:
                for i in range(0, Fork.pages):
                    with ProcessPoolExecutor(max_workers=cores - 1) as executor:
                        futures = [executor.submit(Indeed.get_job_list, term, i, locations.loc[city, 'city'],
                                                   locations.loc[city, 'state_id']) for term in search_terms]
                        for result in as_completed(futures):
                            master_job_list.append(result.result())
                    print('           ' + 'Indeed URLs pg ' + str(i) + ': {} min'.format(round((time() - t) / 60, 2)))

            if Fork.scrape_monster:
                with ProcessPoolExecutor(max_workers=cores - 1) as executor:
                    futures = [executor.submit(Monster.get_job_list, term, locations.loc[city, 'city'],
                                               locations.loc[city, 'state_id']) for term in search_terms]
                    for result in as_completed(futures):
                        master_job_list.append(result.result())
                print('           ' + 'Monster URLs: {} min'.format(round((time() - t) / 60, 2)))

            if Fork.scrape_career_builder:
                with ProcessPoolExecutor(max_workers=cores - 1) as executor:
                    futures = [executor.submit(CareerBuilder.get_job_list, term, locations.loc[city, 'city'],
                                               locations.loc[city, 'state_id']) for term in search_terms]
                    for result in as_completed(futures):
                        master_job_list.append(result.result())
                print('           ' + 'CareerBuilder URLs: {} min'.format(round((time() - t) / 60, 2)))

    # how many total jobs did we find?
    for listx in master_job_list:
        jobs_found += len(listx)

    # if saving the database, open db connection
    if Fork.export_to_mongo:
        client = MongoClient(Fork.MONGO_HOST, Fork.MONGO_PORT, username=Fork.MONGO_USERNAME,
                             password=Fork.MONGO_PASSWORD)
        db = client.jobs
        collection = db.jds  # db.job_descriptions

    print('Scrape complete. Jobs Found: ' + str(jobs_found) + ', Time to scrape: {} min'.format(
        round((time() - t) / 60, 2)))

    job_found_count = 0
    unsaved_job_count = 0

    # STEP 2: SCRAPE COMPLETE JOB DESCRIPTIONS, EXPORT THE SCRAPED JOB DESCRIPTIONS
    for x in master_job_list:
        if isinstance(x, JobPost):
            unsaved_job_count += 1
            print('Unsaved Job: #' + str(unsaved_job_count))
        elif len(x) > 0:

            # status update
            job_found_count += len(x)
            pct_complete = round(job_found_count * 100 / jobs_found, 2)
            print(str(pct_complete) + '% Complete. Jobs: ' + str(len(x)) + ', Net: ' + str(job_found_count) + '/' + str(jobs_found) + ', Time: {} min'.format(round((time() - t) / 60, 2)))

            doc_collection = []

            temp = x[0]

            # iterate through each list of JDs
            if temp.source == ScrapeHelper.INDEED:
                with ProcessPoolExecutor(max_workers=cores - 1) as executor:
                    futures = [executor.submit(Indeed.get_document, y) for y in x]
                    for result in as_completed(futures):
                        doc_collection.append(result.result())
            elif temp.source == ScrapeHelper.MONSTER:
                with ProcessPoolExecutor(max_workers=cores - 1) as executor:
                    futures = [executor.submit(Monster.get_document, y) for y in x]
                    for result in as_completed(futures):
                        doc_collection.append(result.result())
            elif temp.source == ScrapeHelper.CAREERBUILDER:
                with ProcessPoolExecutor(max_workers=cores - 1) as executor:
                    futures = [executor.submit(CareerBuilder.get_document, y) for y in x]
                    for result in as_completed(futures):
                        doc_collection.append(result.result())

            if len(doc_collection) > 0:
                doc_collection = list(filter(None, doc_collection))

                # save to db
                if Fork.export_to_mongo:
                    try:
                        collection.insert_many(doc_collection)
                    except Exception as e:
                        ScrapeHelper.print_error_string('Mongo Write Error: ' + str(e))

    print('Fork Data Export - 100% Complete.  Execution Time: {} min'.format(round((time() - t) / 60, 2)))
