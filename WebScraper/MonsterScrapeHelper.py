import requests
from bs4 import BeautifulSoup
from Classes.JobPostModule import JobPost


def get_monster_url(search_term, search_page_number=0, search_city='', search_state=''):
    """Returns URL that queries Monster for the given search term at the given location.
    search_page_number counts from 0! """

    #https://www.monster.com/jobs/search/?q=data-science&where=New-Orleans__2C-LA
    base_url = 'https://www.monster.com/jobs/search/?q='

    search_term = search_term.replace(' ', '-')

    search_city = search_city.replace(' ', '-')

    if len(search_state) > 0:
        search_state = '__2C-' + search_state

    if search_page_number > 0:
        return base_url + search_term + '&where=' + search_city + search_state + '&start=' + str(search_page_number * 10)
    else:
        return base_url + search_term + '&where=' + search_city + search_state