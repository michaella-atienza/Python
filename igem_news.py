#importing packages and setting up our base
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import requests 

root = "https://www.google.com"

# Plug in the link of your topic of interest after your first google search. In this case, biomanufacturing.
link = "https://www.google.com/search?q=biomanufacturing&sxsrf=ALiCzsZEO68fLKUdO3xlwBvpjKMyAEMSCg:1670813767551&source=lnms&tbm=nws&sa=X&ved=2ahUKEwiF3eaoivP7AhUFSN8KHWKeBK4Q_AUoAXoECAEQAw&biw=1413&bih=1123&dpr=0.8"

def extract_news(link):     
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read() # print(webpage)

    with requests.Session() as c: 
        soup = BeautifulSoup(webpage, 'html5lib')
        print(soup)

        for item in soup.find_all('div', attrs={'class': 'Gx5Zad fP1Qef xpd EtOod pkphOe'}):
            raw_link = (item.find('a', href=True)['href']) # this will print all the links within the class. 

            link = (raw_link.split("/url?q=")[1]).split('&sa=U')[0] # clean up link and only print the URL, and not a page not found after remove '&sa=U'
            #print(link) 

            title = (item.find('div', attrs={'class': 'egMi0 kCrYT'}).get_text()) #get_text() removes the html elements
            title = title.split(" ...")[0]
            title = title.replace(",", "")
            #print(title)

            raw_description = item.find('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'}).get_text()

            description = raw_description.split(".")[0]
            description = description.replace(",", "")
            #print(description)

            publisher = (item.find('div', attrs={'class': 'BNeawe UPmit AP7Wnd lRVwie'})).get_text()
            #print(publisher)

            document = open("1biomanufacturing_recent_dec112022.csv", "a")
            document.write("{}, {}, {}, {} \n".format(title, description, publisher, link))
            document.close()

        next_page = soup.find('a', attrs={'aria-label':'Next page'})
        #print(next_page['href']) # look at what to add to the root to go to next page
        next_page = (next_page['href'])
        link = root + next_page # add next to root 
        extract_news(link)

extract_news(link)
