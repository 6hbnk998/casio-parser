import requests
from bs4 import BeautifulSoup
import time
import os
import json

def get_all_pages():
    headers = {
        'user-agent': 'your user_agent',
        'Accept': 'text/html, */*; q=0.01'
    }
    
    r = requests.get(url="https://de.casio-shop.eu/g-shock/?sort=release-date&view_type=matrix&",headers=headers)

    if not os.path.exists("data"):
        os.mkdir("data")

    with open("casio.html", 'w') as file:
        file.write(r.text)
    with open("name of the folder html") as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    pages_count = int(soup.find("div", class_="c-controlbar__item c-controlbar__item--pager").find_all("a")[-3].text)

    for i in range(1, pages_count+1):
        url = f"https://de.casio-shop.eu/g-shock/?sort=release-date&view_type=matrix&page_number={i}"
        
        r = requests.get(url=url,headers=headers)
        
        with open(f"casio/casio_num_{i}.html","w") as file:
            file.write(r.text)

        time.sleep(2)

    return pages_count +1


def collecting_data(pages_count):

    data_casio = []
    for page in range(1,2):
        with open(f"/casio/casio_num_{page}.html") as file:
            src = file.read()
            
        soup = BeautifulSoup(src,'lxml')
        item_cards = soup.find_all("li", class_="o-grid__item c-product-matrix__item")
        for item in item_cards:
            item_name = item.find("h2",class_="c-product-name__title c-product-name__title--level2").text
            item_price = item.find("span",class_="c-product-pricing__price").strip()
            item_href = "https://de.casio-shop.eu"+ item.find("a",class_="c-product-name__anchor").get("href")
            print(item_price)


            data_casio.append(
            {
                "product_name": item_name,
                "product_price": item_price,
                "product_href": item_href
            }
        )

    with open("casio_casio.json", "a") as file:
        json.dump(data_casio,file, indent=4, ensure_ascii=False)



def main():
    pages_count= get_all_pages()
    collecting_data(pages_count=pages_count)

if __name__=="__main__":
    main()