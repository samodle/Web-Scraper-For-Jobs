import datetime


class JobPost:
    def __init__(self, job_title, company="", url=""):
        self.job_title = job_title
        self.url = url
        self.company = company
        self.last_update = datetime.datetime.now()
        # initialize other fields
        self.company_rating = -1
        self.salary = ""

    def __str__(self):
        return self.job_title + ": " + self.url
