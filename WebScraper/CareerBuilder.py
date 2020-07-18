import requests
from bs4 import BeautifulSoup
from Classes.JobPostModule import JobPost
from WebScraper import ScrapeHelper


def get_url(search_term, search_page_number=0, search_city='', search_state=''):
    """Returns URL that queries Monster for the given search term at the given location.
    search_page_number counts from 0! """

    # https://www.careerbuilder.com/jobs?keywords=data&location=&page_number=2
    base_url = 'https://www.careerbuilder.com/jobs?keywords='

    search_term = search_term.replace(' ', '+')

    search_city = search_city.replace(' ', '+')

    if len(search_state) > 0:
        search_state = '%2C+' + search_state

    if search_page_number > 0:
        return base_url + search_term + '&location=' + search_city + search_state + '&stpage=1&page=' + str(
            search_page_number)
    else:
        return base_url + search_term + '&location=' + search_city + search_state