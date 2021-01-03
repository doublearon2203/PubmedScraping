import sys
import click
import os
import json
from scraping import Scraping
from network_graph import Networkgraph


def scrape():

    scraping = Scraping()
    link = input("Input Link of Article: ")
    iterations = input("Input number of layers: ")
    
    database = scraping.runScraping(iterations, link)

    return database

def display(db_path):
    network = Networkgraph()
    network.display(db_path)

def save(database, db_path):

    with open(db_path, 'w') as f:
        json.dump(database, f, indent=4)

def let_user_pick(options):
    print("Please choose:")
    for idx, element in enumerate(options):
        print("{}) {}".format(idx+1,element))
    print("\n")
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i)
    except:
        pass
    return None

if __name__ == "__main__":
    print("-----------------------------------------------------")
    print("------------ PubMed Web Scraping Starting -----------")
    print("-----------------------------------------------------\n")

    options = ["Run Webscraping and Display Network Graph", 
                "Display Network Graph from previous Search",
                "Set Chromium Webbrowser Path",
                "Exit Application"]

    while True:

        pick = let_user_pick(options)
        print("\n")

        if pick == 1:
            print("-----------------------------------------------------")
            db_name = input("Input name for database (No spaces): ")
            db_path = f"Results/{db_name}.json"
            database = scrape()

            save(database, db_path)
            display(db_path)

        if pick == 2:
            print("-----------------------------------------------------")
            dirlist = os.listdir("Results")
            dirlist = [elem[:-5] for elem in dirlist]
            ID = let_user_pick(dirlist)
            db_path = f"Results\{dirlist[ID-1]}.json" 
            # print(db_path)
            display(db_path)
        
        if pick == 3:
            print("-----------------------------------------------------")
            webpath = input("Input chromium Webbrowser path: ")
            webpath = webpath + "\chromedriver.exe"

            with open("config.json", 'w') as f:
                json.dump({"path": webpath}, f, indent=4)

        if pick == 4:
            print("-----------------------------------------------------")
            print('Closing')
            break

        else:
            print("Invalid Pick\n")

    