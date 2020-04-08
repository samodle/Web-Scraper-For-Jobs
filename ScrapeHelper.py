import requests
from bs4 import BeautifulSoup
from JobPostModule import JobPost


def get_indeed_url(search_term, search_page_number=0, search_city='', search_state=''):
    """Returns URL that queries Indeed for the given search term at the given location.
    search_page_number counts from 0! """

    base_url = 'https://www.indeed.com/jobs?q='

    search_term = search_term.replace(' ', '+')

    search_city = search_city.replace(' ', '+')

    if len(search_state) > 0:
        search_state = '%2C+' + search_state

    if search_page_number > 0:
        return base_url + search_term + '&l=' + search_city + search_state + '&start=' + str(search_page_number * 10)
    else:
        return base_url + search_term + '&l=' + search_city + search_state


def get_indeed_urls(target_url):
    """Given a url, returns a list of tuples: (Job Name, Url)"""

    url_list = []

    page = requests.get(target_url)

    # Create a BeautifulSoup object
    big_soup = BeautifulSoup(page.text, 'html.parser')

    # Let's clean this mess up
    for script in big_soup(["script", "style"]):  # remove all javascript and stylesheet code
        script.decompose()

    for div in big_soup.find_all("div", {'class': 'jobsearch-SerpJobCard-footer'}):
        div.decompose()

    for table in big_soup.find_all("table", {'class': 'jobCardShelfContainer'}):
        table.decompose()

    for div2 in big_soup.find_all("div", {'class': 'tab-container'}):
        div2.decompose()

    # Ok ok I think we're ready...
    jesus_take_the_wheel = big_soup.find_all('a', class_='jobtitle turnstileLink')

    for x0 in jesus_take_the_wheel:
        links = 'https://www.indeed.com' + x0.get('href')
        names = x0.get_text().strip('\n')
        url_list.append(JobPost(names, links))

    return url_list


