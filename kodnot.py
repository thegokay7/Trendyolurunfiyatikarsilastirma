import requests
from bs4 import BeautifulSoup 


url="https://www.trendyol.com/karpefingo/erkek-reglan-kol-oversize-siyah-sisme-mont-p-144971092?boutiqueId=61&merchantId=106453"


headers={
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
}

page = requests.get(url, headers=headers)

sayfa = BeautifulSoup(page.content,'html.parser')

productTitle = sayfa.find("h1", class_="pr-new-br").getText()

price = sayfa.find("span", class_="prc-slg").getText()

image = sayfa.find("img",class_="js-image-zoom__zoomed-area")

convertedPrice = float(price.replace(",",".").replace("TL",""))

