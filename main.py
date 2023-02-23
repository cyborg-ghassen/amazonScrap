from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.amazon.com"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(BASE_URL + "/s?rh=n%3A16225007011&fs=true&ref=lp_16225007011_sar")

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

container = soup.find("div", {'class': 's-main-slot s-result-list s-search-results sg-row'})

links = []
titles = []
prices = []

for i in container.find_all("div", {"class": "sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 "
                                             "sg-col s-widget-spacing-small sg-col-4-of-20"}):
    title = i.find("h2", {"class": "a-size-mini a-spacing-none a-color-base s-line-clamp-4"})
    titles.append(title.text.replace("\n", ""))

    link = title.findNext("a")
    links.append(BASE_URL + link["href"])

    try:
        price_section = i.find("div", {"class": "a-section a-spacing-none a-spacing-top-small "
                                                "s-price-instructions-style"})
        price = price_section.find("span", {"class": "a-price"}).findNext("span", {"class": "a-offscreen"}).text
        prices.append(price)
    except AttributeError as a:
        prices.append("NAN")


df = pd.DataFrame({
    "Title": titles,
    "Price": prices,
    "Link": links
})

df.to_excel("data.xlsx")
