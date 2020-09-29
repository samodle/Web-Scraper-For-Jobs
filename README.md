# forkwebscraper

Please contact @samodle to ensure read.me is up to date. spoiler alert - as of 9/28/2020, its not

Fork Web Scraper requires a ForkConfig.py file with the following parameters:

```python
# Application Settings
# 'search_terms' will be iterated through to query various job boards
search_terms = [
    'supervisor', 'manager', 'project', 'developer', 'customer support', 'customer experience', 'data center', 'help desk', 'technician',
    'slack', 'server', 'recruiter', 'computer', 'product', 'assistant', 'genius', 'retail', 'sales']

# option to define custom locations not included in the census data
custom_search_locations = (('Washington', 'DC'), ('New York', 'NY'), ('Chicago', 'IL'), ('San Jose', 'CA'))

# query params
pages = 3  # if a job board uses pages, number of pages to pull
num_cities = 10  # number of cities to query
jobs_per_csv = 10000  # how many jds per csv files (if outputting to csv)

# feature toggles
only_do_one = False  # if only_do_one is true, the scrape will query 1 search page

# Select websites to scrape posts from
scrape_indeed = True
scrape_monster = True
scrape_career_builder = True

# choose how to save the data
export_to_csv = False
export_to_mongo = True

# input parameter sources
scrape_census_locations = False
use_custom_locations = False  # option to enter your own search locations instead of picking n top locations
use_professions_as_search_terms = False

  # Database Params
  MONGO_USERNAME = ''
  MONGO_PASSWORD = ''
  MONGO_PORT = 
  MONGO_HOST = ''
  MONGO_JOB_DB = ''
  MONGO_JOB_COLLECTION = ''
```