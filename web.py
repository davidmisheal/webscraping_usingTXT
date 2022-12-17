import requests
import csv
from bs4 import BeautifulSoup
from itertools import zip_longest
import re

page = 1  # first page number.
jobTitle__ = []  # variable for job names.
price__ = []  # variable for price of each job.
delivery__ = []  # variable for delivery date.
links__ = []  # variable containing links using in scraping from multiple pages.
desc__ = []  # variable for job description.
likes__ = []  # variable for number of likes.
wholeDiv = []  # variable containing the whole div of the job to get links from
names__ = []  # employee names
counterWh = 1  # counter for print number of job
counterFor = 1  # counter for print number of job looping


# looping to scrape all the 9 pages.
while True:
    result = requests.get(f"https://www.peopleperhour.com/services/python?page={page}&ref=search")
    src = result.content
    soup = BeautifulSoup(src, "html.parser")

    jobTitle = soup.find_all("h2", {"class": "title-nano card__title⤍HourlieTile⤚5LQtW"})
    price = soup.find_all("span", {"class": "title-nano"})
    deliveryDate = soup.find_all("span", {"class": "nano card__shipment⤍HourlieTile⤚AjgW3"})
    div = soup.find_all("div", {"class": "card⤍HourlieTile⤚3DrJs"})

    for i in range(len(jobTitle)):
        jobTitle__.append(str(counterWh)+"- "+jobTitle[i].text.replace("\n", ""))
        links__.append(div[i].find("a").attrs['href'])
        price__.append(price[i].text.replace("\n", ""))
        delivery__.append(deliveryDate[i].text.replace("\n", "").replace("delivered in", ""))
        counterWh += 1

    print(f"page number {page} switched")
    page += 1
    if page > 9:
        break

# scraping data from inner pages(each job).
for link in links__:
    result = requests.get(link)
    src = result.content
    soup = BeautifulSoup(src, "html.parser")
    likes = soup.find("span", {"class": "count-stars"})
    if likes is None:
        likes__.append("------")
    else:
        likes__.append(likes.text)
    desc = soup.find("div", {"class": "content-text clearfix"})
    if desc is None:
        desc__.append("------")
    else:
        desc__.append(re.sub(r'[^a-zA-Z0-9,.-]', ' ', desc.text.strip()))
    names = soup.find("h5")
    names__.append(names.text.strip())
    print(f"looping job {counterFor}")
    counterFor += 1

# printing number of jobs.
num = len(jobTitle__)
print(f"number of jobs:{num}")

# inserting data in a csv file.
listOfItems = [jobTitle__, names__, price__, delivery__, likes__, desc__]
exported = zip_longest(*listOfItems)
with open("PeoplePerHourFinal.csv", "w", encoding="utf-8") as myFile:
    wr = csv.writer(myFile)
    wr.writerow(["Job Title", "Name", "Price", "Delivery Date", "Likes", "Job Description"])
    wr.writerows(exported)


