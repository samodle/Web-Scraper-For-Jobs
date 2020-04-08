import ScrapeHelper
from JobPostModule import JobPost

# USER INPUT GOES HERE!
search_terms = ('data science', 'data center', 'IT')
search_locales = (('Washington', 'DC'), ('New York', 'NY'), ('Chicago', 'IL'))
pages = 3

# variables
master_job_list = []

# specify the url
for term in search_terms:
    for locale in search_locales:
        for page in range(0, pages):
            target_url = ScrapeHelper.get_indeed_url(term, page, locale[0], locale[1])
            master_job_list.append(ScrapeHelper.get_indeed_urls(target_url))

for x in master_job_list:
    for y in x:
        print(str(y))

# export to excel
# with open('index.csv', 'a') as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow([name, price, datetime.now()])
