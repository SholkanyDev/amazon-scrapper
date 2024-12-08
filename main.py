import requests
import csv
from bs4 import BeautifulSoup

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0',
            'Accept-Language': 'en-US, en;q=0.5'})
page = 1
query = input("Product: ")
url= f"https://www.amazon.com/s?k={query}&page={page}"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")
total_page = int(soup.find_all(attrs={"tabindex":"0"})[-3].text)
file = [["ASIN", "url", "listing name", "price", "rating"]]

while True:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    results = []
    c = 1
    while True:
        result = soup.find(attrs={"data-csa-c-pos":c})
        if result == None:
            break
        else:
            results.append(result)
            c+=1

    for e in results:
        review_block = str(e.find(attrs={"data-cy":"reviews-block"}))
        file.append([e.get("data-csa-c-item-id").split(".")[-1],
                     f"https://www.amazon.com{e.find("a").get("href")}",
                     e.find("h2").text,
                     str(e.find(attrs={"class":"a-offscreen"})).split("$")[-1].replace("</span>",""),
                     review_block[review_block.find("span")+163:review_block.find("span")+166]])
    page += 1
    if page > total_page:
        break
with open(f"{query}.csv", mode="w", newline="", encoding="utf-8") as fp:
    writer = csv.writer(fp)
    writer.writerows(file)
print("\033[92m"+"Done!\nPlz hire me i am good LOLz")