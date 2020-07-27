import requests
from bs4 import BeautifulSoup
from Classes.JobPostModule import JobPost
from WebScraper import ScrapeHelper
import ForkConfig as Fork


def get_job_list(search_term, search_city='', search_state=''):
    url = get_url(search_term, Fork.monster_pages, search_city, search_state)
    return get_job_posts(url, search_term)


def get_url(search_term, search_page_number=0, search_city='', search_state=''):
    """Returns URL that queries Monster for the given search term at the given location.
    search_page_number counts from 0! """

    # https://www.monster.com/jobs/search/?q=data-science&where=New-Orleans__2C-LA
    base_url = 'https://www.monster.com/jobs/search/?q='

    search_term = search_term.replace(' ', '-')

    search_city = search_city.replace(' ', '-')

    if len(search_state) > 0:
        search_state = '__2C-' + search_state

    if search_page_number > 0:
        return base_url + search_term + '&where=' + search_city + search_state + '&stpage=1&page=' + str(
            search_page_number)
    else:
        return base_url + search_term + '&where=' + search_city + search_state


def get_job_posts(target_url, search_term):
    """Given a url, returns a list of objects of instance JobPost"""

    # custom parameters
    unknown_string = 'UNKNOWN'

    # variables
    url_list = []
    page = requests.get(target_url)

    # Create a BeautifulSoup object
    big_soup = BeautifulSoup(page.text, 'html.parser')

    # Let's clean this mess up
    for script in big_soup(["script", "style"]):  # remove all javascript and stylesheet code
        script.decompose()

    parent_search_section = big_soup.find_all('div', class_='mux-card mux-job-card')

    if parent_search_section is None:
        ScrapeHelper.print_error_string(big_soup.prettify())
    else:
        try:
            job_cards_master = parent_search_section[0]
            # job_cards = job_cards_master.find_all('section', class_='card-content')
            job_cards = job_cards_master.find_all(
                lambda tag: tag.name == 'section' and tag.get('class') == ['card-content'])
            for card in job_cards:
                try:
                    company_div = card.find('div', class_='company')
                    x1 = company_div.find('span', class_='name')
                    if not x1 is None:
                        company = x1.text.strip('\n')
                    else:
                        company = unknown_string

                    loc_div = card.find('div', class_='location')
                    x2 = loc_div.find('span', class_='name')
                    if not x2 is None:
                        location = x2.text.strip('\n')
                        location = location.replace('\r', '')
                        location = location.replace('\n', '')
                    else:
                        location = unknown_string

                    sum_div = card.find('div', class_='summary')
                    x3 = sum_div.find('header', class_='card-header')
                    x0 = x3.find('a')
                    links = x0.get('href')
                    names = x0.get_text().strip('\n')
                    names = names.replace('\r', '')

                    # print(names + ' -- ' + location + ' -- ' + company + ' -- ' + links)
                    url_list.append(
                        JobPost(job_title=names, url=links, company=company, location=location, search_term=search_term,
                                source=ScrapeHelper.MONSTER))
                except Exception as e:
                    ScrapeHelper.print_error_string(str(e) + " Monster Job Unavailable/Not Found: " + search_term)
        except Exception as e:
            ScrapeHelper.print_error_string(str(e) + " Monster Job Cards Not Found: " + search_term)

    return url_list


def get_document(y: JobPost):
    try:
        complete_job_profile(y)
        new_jd = {
            "JobTitle": y.job_title,
            "CompanyID": 0,
            "company": y.company,
            "location": y.location,
            "rating": y.company_rating,
            "salary": y.salary,
            "commitment": y.commitment_level,
            "url": y.url,
            "search_term": y.search_term,
            "source": y.source,
            "description": y.description,
            "date_found": y.date_found,
            "post_date": y.post_date
        }
        return new_jd
    except Exception as e:
        ScrapeHelper.print_error_string('Complete Job Post Error ' + y.source + ' ' + y.url + ' : ' + str(e))
        return None


def complete_job_profile(job_post: JobPost):
    page = requests.get(job_post.url)

    # Create a BeautifulSoup object
    big_soup = BeautifulSoup(page.text, 'html.parser')

    # Let's clean this mess up
    for script in big_soup(["script", "style"]):  # remove all javascript and stylesheet code
        script.decompose()

    x0 = big_soup.find('div', class_='job-description')

    if not x0 is None:
        for h2 in x0.find_all("h2"):
            h2.decompose()
        job_post.description = x0.get_text().replace('\n', ' ')

    return
