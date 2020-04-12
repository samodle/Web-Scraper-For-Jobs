import IndeedScrapeHelper
import csv
import datetime
from JobPostModule import JobPost

# USER INPUT GOES HERE!
search_terms = ('data science', 'data center', 'IT')
search_locales = (('Washington', 'DC'), ('New York', 'NY'), ('Chicago', 'IL'), ('San Jose', 'CA'))
pages = 5
only_do_one = False
export_to_csv = True  # as opposed to printing data in the console

# variables
master_job_list = []

# specify the url
if not only_do_one:
    for term in search_terms:
        for locale in search_locales:
            for page in range(0, pages):
                target_url = IndeedScrapeHelper.get_indeed_url(term, page, locale[0], locale[1])
                master_job_list.append(IndeedScrapeHelper.get_indeed_urls(target_url))
else:
    target_url = IndeedScrapeHelper.get_indeed_url(search_terms[0], 1, search_locales[0][0], search_locales[0][1])
    master_job_list.append(IndeedScrapeHelper.get_indeed_urls(target_url))

if export_to_csv:
    now = datetime.datetime.now()
    new_csv_file = open("JobPostExport-" + str(now.day) + str(now.hour) + str(now.minute) + str(now.second) + ".csv", "w", newline='')
    writer = csv.writer(new_csv_file)
    fields = ['Name', 'Company', 'Location', 'Indeed Company Rating', 'Salary', 'Commitment', 'URL', 'Description']
    writer.writerow(fields)

for x in master_job_list:
    for y in x:
        IndeedScrapeHelper.complete_job_profile(y)
        if export_to_csv:
            new_row = [y.job_title, y.company, y.location, y.company_rating, y.salary, y.commitment_level, y.url, y.description.encode('utf-8', errors='replace')]
            writer.writerow(new_row)
        else:
            print(str(y))

if export_to_csv:
    new_csv_file.close()



