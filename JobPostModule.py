import datetime


class JobPost:
    def __init__(self, job_title, url="", company="", location=""):
        self.job_title = job_title
        self.url = url
        self.company = company
        self.location = location
        self.last_update = datetime.datetime.now()
        # initialize other fields
        self.company_rating = ""
        self.salary = ""
        self.commitment_level = ""
        self.description = ""

    def __str__(self):
        return self.job_title + ', ' + self.company + ', ' + self.location + '\n' + self.company_rating + ', ' + self.salary + ', ' + self.commitment_level + '\n' + self.url

    def get_csv_string(self):
        return '[[' + self.job_title + ', ' + self.company + ', ' + self.location + ',' + self.company_rating + ', ' + self.salary + ', ' + self.commitment_level + ',' + self.url + ']]' #  ',' + self.description + ']'