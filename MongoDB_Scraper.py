import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from pathlib import Path

global level
global browser


reset_spot = "#fas-nav-world"
membership_spot = " > div > div.stat-line.w-graph > div:nth-child(1) > div.key-box.key-box-a > h4"
congregation_spot = " > div > div.stat-line.w-graph > div:nth-child(1) > div.key-box.key-box-b > h4"
mission_spot = " > div > div.stat-line.w-graph > div:nth-child(2) > h4.weird-label > span:nth-child(1)"
temple_spot = " > div > div.stat-line.w-graph > div.stat-block.weird-label-holder.continent-temples-block > h4.weird-label > span:nth-child(1)"
family_spot = " > div > div.stat-line.w-graph > div.stat-block.fh-stat-block > div > div.gen-one > div.box > span"

id = []
continents = ("north-america", "south-america", "europe", "asia", "oceania", "africa")
membership = []   
congregation = []
mission = []   
temple = []
family = []

new_collection = [{
        "key_id": 0,
        "continent": "test",
        "total_membership": 0,
        "congregations": 0,
        "missions": 0,
        "temples": 0,
        "family_history_centers": 0
    },
    {
        "key_id": 0,
        "continent": "test",
        "total_membership": 0,
        "congregations": 0,
        "missions": 0,
        "temples": 0,
        "family_history_centers": 0
    },
    {
        "key_id": 0,
        "continent": "test",
        "total_membership": 0,
        "congregations": 0,
        "missions": 0,
        "temples": 0,
        "family_history_centers": 0
    },
    {
        "key_id": 0,
        "continent": "test",
        "total_membership": 0,
        "congregations": 0,
        "missions": 0,
        "temples": 0,
        "family_history_centers": 0
    },
    {
        "key_id": 0,
        "continent": "test",
        "total_membership": 0,
        "congregations": 0,
        "missions": 0,
        "temples": 0,
        "family_history_centers": 0
    },
    {
        "key_id": 0,
        "continent": "test",
        "total_membership": 0,
        "congregations": 0,
        "missions": 0,
        "temples": 0,
        "family_history_centers": 0
    }
    ]

#starts program
def main():  
    set_up_site()      
    get_values()
    insert_data(id,
                continents,
                membership,  
                congregation,
                mission, 
                temple,
                family)
    update_database()
    end_program()

    




#gets Address and Zip Code and runs those through get_owner_name() until all rows are updated
def get_values():
    
    global level
    level = 0
    regions = ("#fas-continents > li:nth-child(1) > a", "#fas-continents > li:nth-child(2) > a", "#fas-continents > li:nth-child(3) > a", "#fas-continents > li:nth-child(4) > a", "#fas-continents > li:nth-child(5) > a", "#fas-continents > li:nth-child(6) > a")
    
    while level != 6:
        current_spot = browser.find_element(By.CSS_SELECTOR, regions[level])
        current_spot.click()
        scrape_page(level)        
        current_spot = browser.find_element(By.CSS_SELECTOR, reset_spot)
        current_spot.click()  
        level += 1    
   

#opens up the website needed to scrape data from
def set_up_site():
    global browser
    browser = webdriver.Chrome(str(Path.cwd()) + "\\chromedriver")
    browser.get('https://newsroom.churchofjesuschrist.org/facts-and-statistics#')
    

#gets data from each page given and stores it in lists
def scrape_page(level):
    global browser
    data_value = 0

    id.append(level + 1)
    data_value = browser.find_element(By.CSS_SELECTOR, combiner(continents[level], membership_spot)).text
    membership.append(int(data_value.replace(',',"")))
    data_value = browser.find_element(By.CSS_SELECTOR, combiner(continents[level], congregation_spot)).text
    congregation.append(int(data_value.replace(',',"")))
    data_value = browser.find_element(By.CSS_SELECTOR, combiner(continents[level], mission_spot)).text
    mission.append(int(data_value.replace(',',"")))
    data_value = browser.find_element(By.CSS_SELECTOR, combiner(continents[level], temple_spot)).text
    temple.append(int(data_value.replace(',',"")))
    data_value = browser.find_element(By.CSS_SELECTOR, combiner(continents[level], family_spot)).text
    family.append(int(data_value.replace(',',"")))
   

#function forms the exact css selector needed
def combiner(continent, spot):
    return str("#fas-continent-stats-" + continent + spot)


   
#Insert data values scraped from website into newly created postgres tables
def insert_data(id,
                continents,
                membership,  
                congregation,
                mission, 
                temple,
                family):

    row = 0

    while row != 6:
            new_collection[row].update({"key_id":id[row], "continent":continents[row], "total_membership":membership[row], "congregations":congregation[row], "missions":mission[row], "temples":temple[row], "family_history_centers":family[row]})
            row += 1

    # Commented outlines create a JSON file
    # final = json.dumps(new_collection, indent=7)

    # with open("sample.json", "w") as outfile:
    #     outfile.write(final)
        
    
    

#Connects to MongoDB Server and creates Database
def get_database():
   CONNECTION_STRING = "mongodb+srv://Askels0n:Askels0n@sandbox.eaeyl.mongodb.net/test"
   client = MongoClient(CONNECTION_STRING)
   return client['LDS_Records']
  

#Updates Database with new collection
def update_database():
    dbname = get_database()
    collection_name = dbname["Membership_Records"]
    collection_name.insert_many([new_collection[0],new_collection[1],new_collection[2],new_collection[3],new_collection[4],new_collection[5]])



#Finishes up and ends program
def end_program():
    browser.quit()
    #test to check proper table values
    """ print(id)
    print(continents)
    print(membership)
    print(congregation)
    print(mission)
    print(temple)
    print(family) 
    xval = ""
    xval = input("Looks Good?")"""
    #connect()
    sys.exit()



main()

 

 

