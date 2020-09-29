import datetime


class JobPost:
    def __init__(self, job_title, url=None, company=None, location=None, search_term=None, source=None, salary='',
                 commitment_level='', post_date=''):
        self.job_title = job_title
        self.url = url
        self.company = company
        self.location = location
        self.dates_found = [datetime.datetime.now()]
        self.search_terms = [search_term]
        self.source = source
        # initialize other fields
        self.company_rating = ''  # None
        self.salary = salary  # None
        self.commitment_level = commitment_level  # None
        self.description = ''
        self.post_date = post_date

    def __str__(self):
        return self.job_title + ', ' + self.company + ', ' + self.location + '\n' + self.company_rating + ', ' + self.salary + ', ' + self.commitment_level + '\n' + self.url
