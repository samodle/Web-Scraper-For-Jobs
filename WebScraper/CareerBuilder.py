import requests
from bs4 import BeautifulSoup
from Classes.JobPostModule import JobPost
from WebScraper import ScrapeHelper


def get_job_list(search_term, search_page_number=0, search_city='', search_state=''):
    url = get_url(search_term, search_page_number, search_city, search_state)
    return get_job_posts(url, search_term)


def get_url(search_term, search_page_number=0, search_city='', search_state=''):
    """Returns URL that queries CareerBuilder for the given search term at the given location.
    search_page_number counts from 0! """

    # https://www.careerbuilder.com/jobs?keywords=data&location=&page_number=2
    base_url = 'https://www.careerbuilder.com/jobs?keywords='

    search_term = search_term.replace(' ', '+')

    search_city = search_city.replace(' ', '+')

    if len(search_state) > 0:
        search_state = '%2C+' + search_state

    if search_page_number > 0:
        return base_url + search_term + '&location=' + search_city + search_state + '&page_number=' + str(
            search_page_number)
    else:
        return base_url + search_term + '&location=' + search_city + search_state


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

    parent_search_section = big_soup.find_all('div', class_='data-results-content-parent relative')

    if parent_search_section is None:
        ScrapeHelper.print_error_string(big_soup.prettify())
    else:
        try:
            for card in parent_search_section:
                try:
                    # print(card.prettify())

                    main_div = card.find_all('a')
                    # main_div2 = card.find_all('a', _class='data-results-content block job-listing-item')
                    links = 'https://www.careerbuilder.com' + main_div[1].get('href')

                    name_div = card.find('div', {"class": "data-results-title"})
                    names = name_div.get_text().strip('\n')
                    names = names.replace('\r', '')

                    pub_time = card.find('div', {"class": "data-results-publish-time"})

                    if not pub_time is None:
                        publish_time = pub_time.get_text().strip('\n')
                    else:
                        publish_time = unknown_string

                    # salary_div = card.find('div', {"class": "data-snapshot"})

                    salary_divA = card.find(
                        lambda tag: tag.name == 'div' and tag.get('class') == ['data-snapshot'])

                    salary_div = salary_divA.find(
                        lambda tag: tag.name == 'div' and tag.get('class') == ['block'])

                    if not salary_div is None:
                        salary = salary_div.text.strip('\n')

                    company_div = card.find('div', {"class": "data-details"})
                    spans = company_div.find_all('span')

                    if not spans[0] is None:
                        company = spans[0].text.strip('\n')
                    else:
                        company = unknown_string

                    if not spans[1] is None:
                        location = spans[1].text.strip('\n')
                    else:
                        location = unknown_string

                    if not spans[2] is None:
                        commitment = spans[2].text.strip('\n')
                    else:
                        commitment = unknown_string

                    # print(names + ' -- ' + location + ' -- ' + company + ' -- ' + links + ' -- ' + salary + ' -- '
                    # + commitment + ' -- ' + publish_time)
                    url_list.append(
                        JobPost(job_title=names, url=links, company=company, location=location, search_term=search_term,
                                source=ScrapeHelper.CAREERBUILDER, salary=salary, commitment_level=commitment,
                                post_date=publish_time))
                except Exception as e:
                    ScrapeHelper.print_error_string(str(e) + " Career Builder Job Unavailable/Not Found")
        except Exception as e:
            ScrapeHelper.print_error_string(str(e) + " Career Builder Job Cards Not Found")

    return url_list


def complete_job_profile(job_post: JobPost):
    page = requests.get(job_post.url)

    # Create a BeautifulSoup object
    big_soup = BeautifulSoup(page.text, 'html.parser')

    # Let's clean this mess up
    for script in big_soup(["script", "style"]):  # remove all javascript and stylesheet code
        script.decompose()

    # print(big_soup.prettify())

    parent_search_section = big_soup.find_all('div', class_='seperate-bottom tab bloc jdp-description-details')

    x1 = parent_search_section[0].find_all('div', class_='col big col-mobile-full')
    x0 = x1[0]

    # print(x0.prettify())

    if x0 is not None:
        job_post.description = x0.get_text().replace('\n', ' ')

    return
