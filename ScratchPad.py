import IndeedScrapeHelper
from JobPostModule import JobPost
import requests
from bs4 import BeautifulSoup

target_url = 'https://www.indeed.com/viewjob?cmp=Sanametrix&t=Program+Manager&jk=813f1c04aba43a31&sjdu' \
             '=QwrRXKrqZ3CNX5W-O9jEvboqH3KsCi-ZpW0p65RLM2UrrmEy0vlZZHoowQB8WdRNfaZ845MRlV50p5w6RC5d1w&adid=307171116' \
             '&pub=4a1b367933fd867b19b072952f68dceb&vjs=3 '

target_url2 = 'https://www.indeed.com/viewjob?jk=47ddb70095540843&tk=1e5l2d681p70n800&from=serp&vjs=3'

page = requests.get(target_url2)

# Create a BeautifulSoup object
big_soup = BeautifulSoup(page.text, 'html.parser')



# Let's clean this mess up
for script in big_soup(["script", "style"]):  # remove all javascript and stylesheet code
    script.decompose()

#for div in big_soup.find_all("div", {'class': 'jobsearch-SerpJobCard-footer'}):
 #   div.decompose()

#for table in big_soup.find_all("table", {'class': 'jobCardShelfContainer'}):
 #   table.decompose()

#for div2 in big_soup.find_all("div", {'class': 'tab-container'}):
#    div2.decompose()

print(big_soup.prettify())

# Ok ok I think we're ready...
jesus_take_the_wheel = big_soup.find("div", class_='jobsearch-jobDescriptionText')
#print(jesus_take_the_wheel.text)

print('xxxxxxxxxxxxxxxxx')

rating_section = big_soup.find("meta", itemprop='ratingValue')
print('Employer Rating:' + rating_section.get('content'))

print('xxxxxxxxxxxxxxxxx')

salary_section = big_soup.find("span", class_='icl-u-xs-mr--xs')
print('Salary:' + salary_section.text)

print('xxxxxxxxxxxxxxxxx')

time_section = big_soup.find("span", class_='jobsearch-JobMetadataHeader-item icl-u-xs-mt--xs')
print('Commitment Level:' + time_section.text)

print('xxxxxxxxxxxxxxxxx')

#print(big_soup.prettify())

"""
███████╗ ██████╗ ██████╗ ██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██║ ██╔╝
█████╗  ██║   ██║██████╔╝█████╔╝
██╔══╝  ██║   ██║██╔══██╗██╔═██╗
██║     ╚██████╔╝██║  ██║██║  ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝                 
"""