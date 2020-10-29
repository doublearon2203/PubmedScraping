#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
from network_graph import Networkgraph

networkgraph = Networkgraph()

total_layers = 4

PATH = 'C:\sdk\chromedriver\chromedriver.exe'
driver = webdriver.Chrome(PATH)

# 49Quellen:
# startArticle = 'https://pubmed.ncbi.nlm.nih.gov/32141569/'

# 5 Quellen:
startArticle = 'https://pubmed.ncbi.nlm.nih.gov/31811279/'

# 21 Cites:
# startArticle = 'https://pubmed.ncbi.nlm.nih.gov/21098570/'

driver.get(startArticle)
database = {}

def get_startArticle():

    try:
        articleDetails = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "article-details")))
    
    except:
        print('No Starting Article Found')

    heading = articleDetails.find_element_by_id('full-view-heading')
    
    cit = heading.find_element_by_class_name('cit')
    year = cit.text[:4]

    heading_title = heading.find_element_by_class_name('heading-title')
    print(heading_title.text)
    ID = startArticle[-10:]

    database[ID] = {
                'Title': heading_title.text,
                'Year': year,
                'Link': startArticle,
                'Appearance': 1,
                'Referencing': [],
                'Layer': 0
            }


    

def check_show_more_button():

    noMore = False
    while noMore == False:
        try: 
            articleDetails = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "article-details")))
            citedby = articleDetails.find_element_by_id('citedby')
            button = citedby.find_element_by_class_name('show-more')
            button.click()

            # print('Button Found')
            time.sleep(3)

        except Exception:
            # print(e)
            noMore = True


def open_new_links(layer):

    startDatabase = database
    entryList = []

    for entry in startDatabase:
        if startDatabase[entry]['Layer'] == layer-1:
            entryList.append(entry)

    for article in entryList:

        link = startDatabase[article]['Link']
        child_sourceID = link[-10:]

        driver.execute_script(f'''window.open("{link}","_blank");''')
        driver.switch_to.window(driver.window_handles[1])
        # articleDetails = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "article-details")))
        # time.sleep(2)


        scrape_citedby_articles(child_sourceID, layer)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])


def scrape_citedby_articles(sourceID, layer):

    try:
        articleDetails = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "article-details")))

        # Get year of source article
        heading = articleDetails.find_element_by_id('full-view-heading')
        cit = heading.find_element_by_class_name('cit')
        year = cit.text[:4]

        database[sourceID]['Year'] = year

        citedby = articleDetails.find_element_by_id('citedby')

    except:
        print('No CitedBy Articles')
        app_count = 0
        return

    check_show_more_button()

    citedbyList = citedby.find_element_by_id('citedby-articles-list')
    citedbyList = citedby.find_element_by_id('citedby-articles-list')
    articles = citedbyList.find_elements_by_class_name('full-docsum')

    for article in articles:

        title = article.find_element_by_class_name('docsum-title')
        link = title.get_attribute('href')
        ID = link[-10:]

        print(link)
        print(ID)
        print(title.text + '\n')

        app_count = 0

        if ID not in database:
            database[ID] = {
                'Title': title.text,
                'Year': " ",
                'Link': link,
                'Appearance': 1,
                'Referencing': [sourceID],
                'Layer': layer
            }
        
        else:
            database[ID]['Appearance'] = database[ID]['Appearance'] + 1
            print('Appearance count of article increased and citedby added')
            app_count += 1
            database[ID]['Referencing'].append(sourceID)

    with open('database.json', 'w') as f:
        json.dump(database, f, indent=4)

    print(f'{len(database)} articles in database')


try:
    # print('eskalation')
    get_startArticle()

    startID = startArticle[-10:]
    population = 1
    scrape_citedby_articles(startID, population)

    for i in range(total_layers-2):
        # print('open new links')
        open_new_links(i+2)
        

except Exception as e:
    print(e)

finally:
    time.sleep(5)
    driver.quit()
    # networkgraph.display()
# %%
