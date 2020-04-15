import IndeedScrapeHelper
from JobPostModule import JobPost
import requests
from bs4 import BeautifulSoup
import pandas as pd

raw_city_data = pd.read_csv("IndeedJobPostExport-1592231.csv", encoding='unicode_escape')
print(' ')

"""
███████╗ ██████╗ ██████╗ ██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██║ ██╔╝
█████╗  ██║   ██║██████╔╝█████╔╝
██╔══╝  ██║   ██║██╔══██╗██╔═██╗
██║     ╚██████╔╝██║  ██║██║  ██╗
╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝                 
"""
