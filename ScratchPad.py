import ScrapeHelper
from JobPostModule import JobPost
import requests
from bs4 import BeautifulSoup

target_url = 'https://www.indeed.com/viewjob?cmp=Sanametrix&t=Program+Manager&jk=813f1c04aba43a31&sjdu' \
             '=QwrRXKrqZ3CNX5W-O9jEvboqH3KsCi-ZpW0p65RLM2UrrmEy0vlZZHoowQB8WdRNfaZ845MRlV50p5w6RC5d1w&adid=307171116' \
             '&pub=4a1b367933fd867b19b072952f68dceb&vjs=3 '
page = requests.get(target_url)

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

# Ok ok I think we're ready...
jesus_take_the_wheel = big_soup.find_all("div", class_='jobsearch-jobDescriptionText')

for x0 in jesus_take_the_wheel:
    print(x0.prettify())

#print(big_soup.prettify())