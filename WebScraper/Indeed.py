import requests
from WebScraper import ScrapeHelper
from bs4 import BeautifulSoup
from Classes.JobPostModule import JobPost
import ForkConfig as Fork


def get_job_list(search_term, search_city='', search_state=''):
    job_list = []

    for search_page_number in range(0, Fork.pages):
        url = get_url(search_term, search_page_number, search_city, search_state)
        job_list.append(get_job_posts(url, search_term))

    return job_list


def get_url(search_term, search_page_number=0, search_city='', search_state=''):
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


def get_job_posts(target_url, search_term):
    """Given a url, returns a list of objects of instance JobPost"""

    # custom parameters
    unknown_string = 'UNKNOWN'
    unwanted_company_string = 'Seen by Indeed'

    # variables
    url_list = []
    seen_by_indeed_count = 0

    page = requests.get(target_url)

    # Create a BeautifulSoup object
    big_soup = BeautifulSoup(page.text, 'html.parser')

    # Let's clean this up
    for script in big_soup(["script", "style"]):  # remove all javascript and stylesheet code
        script.decompose()

    for div in big_soup.find_all("div", {'class': 'jobsearch-SerpJobCard-footer'}):
        div.decompose()

    for table in big_soup.find_all("table", {'class': 'jobCardShelfContainer'}):
        table.decompose()

    for div2 in big_soup.find_all("div", {'class': 'tab-container'}):
        div2.decompose()

    parent_search_section = big_soup.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result')

    if parent_search_section is None:
        ScrapeHelper.print_error_string(big_soup.prettify())
    else:
        for x02 in parent_search_section:
            # print(x02.prettify())
            try:
                x1 = x02.find('span', class_='company')
                if not x1 is None:
                    company = x1.text.strip('\n')
                else:
                    company = unknown_string

                if not company == unwanted_company_string:
                    x0 = x02.find('a', class_='jobtitle turnstileLink')
                    links = 'https://www.indeed.com' + x0.get('href')
                    names = x0.get_text().strip('\n')

                    x4 = x02.find('div', class_='recJobLoc')
                    if not x4 is None:
                        location = x4.get('data-rc-loc')
                    else:
                        location = unknown_string

                    url_list.append(
                        JobPost(job_title=names, url=links, company=company, location=location, search_term=search_term,
                                source=ScrapeHelper.INDEED))
                    # print(names + ' -- ' + location + ' -- ' + company + ' -- ' + links)
                else:
                    seen_by_indeed_count += 1
            except:
                ScrapeHelper.print_error_string(x02.prettify())

    # print('Seen By Indeed: ' + str(seen_by_indeed_count))
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

    # Ok ok I think we're ready...
    primary_description = big_soup.find("div", class_='jobsearch-jobDescriptionText')
    if not primary_description is None:
        job_post.description = primary_description.get_text().replace('\n', ' ')

    rating_section = big_soup.find("meta", itemprop='ratingValue')
    if not rating_section is None:
        job_post.company_rating = rating_section.get('content')

    salary_section = big_soup.find("span", class_='icl-u-xs-mr--xs')
    if not salary_section is None:
        job_post.salary = salary_section.text

    time_section = big_soup.find("span", class_='jobsearch-JobMetadataHeader-item icl-u-xs-mt--xs')
    if not time_section is None:
        job_post.commitment_level = time_section.text

    return





