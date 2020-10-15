import requests
import csv
from requests_html import HTMLSession
from bs4 import BeautifulSoup
session = HTMLSession()

def get_otc_tickers():
    l = "http://otcmarkets.com/research/stock-screener/api/downloadCSV"
    r = requests.get(l)
    decoded_content = r.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    tickers = [x[0] for x in list(cr)]
    return tickers

ticker_list = get_otc_tickers()
print (ticker_list)

#with open("otctickerlist.txt", "w") as output:
    #output.write(str(ticker_list))

for i in ticker_list:
    url = "https://www.otcmarkets.com/stock/"+i+"/security"
    r_loop = session.get(url)
    r_loop.html.render(sleep=1)
    soup = BeautifulSoup(r_loop.html.raw_html, "html.parser")
    a = soup.find("div", class_="_33MgosRhnB sc-htpNat pyeRb sc-bdVaJa bVTGsP") #title
    for i in a:
        #os = b.find("div", {"class": "sc-bdVaJa ensNgD"})
        #for i in os:
        blah = (i.text)
        print(blah)
    #scrapes outstanding share counts
    b = soup.find("div", class_="_8AXJn4ourf qiMJzfQpgv sc-htpNat jtWIOA sc-bdVaJa gRrvFh") #title
    for i in b:
        #os = b.find("div", {"class": "sc-bdVaJa ensNgD"})
        #for i in os:
        blah2 = (i.text)
        print(blah2)

    #print(soup.prettify())
    #scrape restricted os
    c = soup.find("div", class_="_8AXJn4ourf _3piM0unCuM qiMJzfQpgv sc-htpNat jtWIOA sc-bdVaJa gRrvFh") #title

    for i in c:
        #os = b.find("div", {"class": "sc-bdVaJa ensNgD"})
        #for i in os:
        blah3 = (i.text)
        print(blah3)

    #scrape unrestricted os
    d = soup.find("div", class_="_8AXJn4ourf _3piM0unCuM sc-htpNat jtWIOA sc-bdVaJa gRrvFh") #title

    for i in d:
        #os = b.find("div", {"class": "sc-bdVaJa ensNgD"})
        #for i in os:
        blah4 = (i.text)
        print(blah4)
