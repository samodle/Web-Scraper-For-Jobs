class JobPost:
    def __init__(self, job_title, url=""):
        self.job_title = job_title
        self.url = url

    def __str__(self):
        return self.job_title + ": " + self.url
