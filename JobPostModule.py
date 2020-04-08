import datetime


class JobPost:
    def __init__(self, job_title, url=""):
        self.job_title = job_title
        self.url = url
        self.last_update = datetime.datetime.now()

    def __str__(self):
        return self.job_title + ": " + self.url
