# import libraries
import requests
from bs4 import BeautifulSoup

# indeed search term - DO NOT INCLUDE SPACES RN
search_term = 'data'
show_me_the_money = False

# specify the url
target_url = 'https://www.indeed.com/jobs?q=' + search_term + '&l=Washington%2C+DC'
page = requests.get(target_url)

# Create a BeautifulSoup object
bigSoup = BeautifulSoup(page.text, 'html.parser')

# Let's clean this mess up
for script in bigSoup(["script", "style"]):  # remove all javascript and stylesheet code
    script.decompose()

for div in bigSoup.find_all("div", {'class': 'jobsearch-SerpJobCard-footer'}):
    div.decompose()

for table in bigSoup.find_all("table", {'class': 'jobCardShelfContainer'}):
    table.decompose()

for div2 in bigSoup.find_all("div", {'class': 'tab-container'}):
    div2.decompose()

# utilities go here, right?
separator = " "

# if not show_me_the_money:
# Ok ok I think we're ready...
jesus_take_the_wheel = bigSoup.find_all('a', class_='jobtitle turnstileLink')  # class_='jobsearch-SerpJobCard unifiedRow row result')
# Create for loop to print out all artists' names
for x1 in jesus_take_the_wheel:
    print('---------------------')
    print('                    ')
    print('---------------------')
    print(x1.prettify())
# else:
# Ok ok I think we're ready...
jesus_take_the_wheel = bigSoup.find_all('a', class_='jobtitle turnstileLink')
for x0 in jesus_take_the_wheel:
    # names = x0.contents[0]

    links = 'https://www.indeed.com' + x0.get('href')
    # print(names)
    print(x0.string)
    print(links)
    print('---------------------')

# export to excel
# with open('index.csv', 'a') as csv_file:
#    writer = csv.writer(csv_file)
#    writer.writerow([name, price, datetime.now()])
