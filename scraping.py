#%%
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json

class Scraping():

    def __init__(self):

        # self.total_layers = 3

        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        with open("config.json") as f:
            data = json.load(f)
        PATH = data["path"]

        # PATH = "C:\sdk\chromedriver\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH, chrome_options=options)

        # 49Quellen:
        # startArticle = 'https://pubmed.ncbi.nlm.nih.gov/32141569/'

        # 5 Quellen:
        # self.startArticle = 'https://pubmed.ncbi.nlm.nih.gov/31811279/'

        # 21 Cites:
        # startArticle = 'https://pubmed.ncbi.nlm.nih.gov/21098570/'

        self.database = {}


    def runScraping(self, total_layers, startArticle):
        
        self.total_layers = int(total_layers)
        self.startArticle = startArticle
        self.driver.get(self.startArticle)

        try:
            self.get_startArticle()

            startID = self.startArticle[-10:]
            self.population = 1
            self.scrape_citedby_articles(startID, self.population)

            for i in range(self.total_layers-2):
                # print('open new links')
                self.open_new_links(i+2)
                

        except Exception as e:
            print(e)

        finally:
            time.sleep(5)
            self.driver.quit()

            return self.database

    def get_startArticle(self):
        try:
            articleDetails = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "article-details")))
        
        except:
            print('No Starting Article Found')

        heading = articleDetails.find_element_by_id('full-view-heading')
        
        cit = heading.find_element_by_class_name('cit')
        year = cit.text[:4]

        heading_title = heading.find_element_by_class_name('heading-title')
        print(heading_title.text)
        ID = self.startArticle[-10:]

        self.database[ID] = {
                    'Title': heading_title.text,
                    'Year': year,
                    'Link': self.startArticle,
                    'Appearance': 1,
                    'Referencing': [],
                    'Layer': 0
                }

    def check_show_more_button(self):

        noMore = False
        while noMore == False:
            try: 
                articleDetails = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "article-details")))
                citedby = articleDetails.find_element_by_id('citedby')
                button = citedby.find_element_by_class_name('show-more')
                button.click()

                # print('Button Found')
                time.sleep(3)

            except Exception:
                # print(e)
                noMore = True


    def open_new_links(self, layer):

        self.layer = layer

        self.startDatabase = self.database
        entryList = []

        for entry in self.startDatabase:
            if self.startDatabase[entry]['Layer'] == layer-1:
                entryList.append(entry)

        for article in entryList:

            link = self.startDatabase[article]['Link']
            child_sourceID = link[-10:]

            self.driver.execute_script(f'''window.open("{link}","_blank");''')
            self.driver.switch_to.window(self.driver.window_handles[1])
            # articleDetails = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "article-details")))
            # time.sleep(2)


            self.scrape_citedby_articles(child_sourceID, layer)
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])


    def scrape_citedby_articles(self, sourceID, layer):

        try:
            articleDetails = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "article-details")))

            # Get year of source article
            heading = articleDetails.find_element_by_id('full-view-heading')
            cit = heading.find_element_by_class_name('cit')
            year = cit.text[:4]

            self.database[sourceID]['Year'] = year

            citedby = articleDetails.find_element_by_id('citedby')

        except:
            print('No CitedBy Articles')
            app_count = 0
            return

        self.check_show_more_button()

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

            if ID not in self.database:
                self.database[ID] = {
                    'Title': title.text,
                    'Year': " ",
                    'Link': link,
                    'Appearance': 1,
                    'Referencing': [sourceID],
                    'Layer': layer
                }
            
            else:
                self.database[ID]['Appearance'] = self.database[ID]['Appearance'] + 1
                print('Appearance count of article increased and citedby added')
                app_count += 1
                self.database[ID]['Referencing'].append(sourceID)

        print(f'{len(self.database)} articles in database')
# %%
