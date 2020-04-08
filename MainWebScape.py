import ScrapeHelper
from JobPostModule import JobPost

search_term = 'data science'
master_job_list = []

# specify the url
target_url = ScrapeHelper.get_indeed_url(search_term, 1, 'Washington', 'DC')

master_job_list.append(ScrapeHelper.get_indeed_urls(target_url))

for x in master_job_list:
    for y in x:
        print(str(y))

# export to excel
# with open('index.csv', 'a') as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow([name, price, datetime.now()])
