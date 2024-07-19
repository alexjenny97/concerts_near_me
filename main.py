
import requests
from bs4 import BeautifulSoup
import logging
import logging.config
import json
import urllib.request, json 
from requests_html import HTMLSession
import time 
import pandas as pd 
from selenium import webdriver
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By 
from datetime import datetime

# Define the Chrome webdriver options
options = webdriver.ChromeOptions() 
options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability
# By default, Selenium waits for all resources to download before taking actions.
# don't need it as the page is populated with dynamically generated JavaScript code.
options.page_load_strategy = "none"
driver = Chrome(options=options) 
# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)


# set up logging
with open('logging_config.json', 'r') as file:
    config = json.load(file)
    logging.config.dictConfig(config)

# Get the logger specified in the file
logger = logging.getLogger('my_logger')

url_mapping = {'fiddlers green': 'https://www.fiddlersgreenamp.com/calendar/'
    }

schema_mapping = {'fiddlers green': {'div': 'c-axs-event-card__wrapper', 'album_cover': 'c-axs-event-card__image', 
                                     'extra_info': 'c-axs-event-card__supporting-text', 'Artist_or_event_name': 'c-axs-event-card__title',
                                     'date': 'c-axs-event-card__date', 'link_for_tickets': 'c-axs-event-card__info'}}

def connectToSite(venue, venue_url):
     # try to connect to venue website
    try:
        logger.info(f'Getting event data for {venue}')
        url = venue_url
        driver.get(url)
        content = driver.find_elements(By.CSS_SELECTOR, f"div[class*='{schema_mapping[venue]['div']}']")
        return content

    except Exception as e:
        logger.error(f'Error getting event data for {venue} due to {e}')


def getEventDetails(event, venue):
    try:
        details = {}
        details['artist']  = event.split("\n")[0] + event.split("\n")[1]
        details['date'] = event.split("\n")[2]
        details['price'] = ''
        details['show_time'] = event.split("\n")[3]
        details['ticket_link'] = ''
        details['tour_poster'] = ''
        return details
    except Exception as e:
        logger.error(f"Failed getting event details due to {e}")

def getUpcommingEvents():
    # events is a list of dictionaries
    # events[x] = {'artist': artist, 'venue': venue, 'date': date, 'show_time' : show_time, 'price' : price, 'ticket_link': ticket_link,
                                #   'tour_poster': tour_poster, 'new': is_new}
    events = []
    for venue, venue_url in url_mapping.items():
       try:
        venue_events = connectToSite(venue=venue, venue_url=venue_url)
        for event in venue_events:
            event = event.text
            events.append(getEventDetails(event=event, venue=venue))

       except Exception as e:
        logger.error(f'Error connecting to site due to {e}')

    if events:
        logger.info(f'Successfully got events for : {len(events)}')
        return events
    else:
        logger.info(f"No results")
        

def removeDupes(events):
    old_events = []
    input_format = '%a %b %d %Y'
    output_format = '%d-%m-%Y'
    new_events = []
    try:
        with open('previous_events.json') as file:
            # old_events should be a list of dictionaries
            old_events = json.load(file)
            old_events = old_events['old_events'] 
            logger.info(f"Successfully opened old events file.")
    except Exception as e:
        logger.error(f"Error opening old event file due to {e}")
    
    try:
        # keeps list of old events small
        for old_event in old_events:
            old_event['date'] = datetime.strptime( \
            old_event['date'], \
            input_format)
            if old_event['date'].date() < datetime.today().date(): #event has passed
                del old_event
        
        for new_event in events:
            for old_event in old_events:
                if new_event['artist'] == old_event['artist'] and new_event['date'] == old_event['date']:
                    continue
                else:
                    new_events.append(new_event)
            # commented out for testing/dev
            # old_events.append(new_event)
            print(new_events)
    except Exception as e:
        logger.error(f"Error removing duplicates due to {e}")
    
    try:
        with open('previous_events.json', 'w') as file:
            json.dump(old_events, file, default=str, indent=4)
        with open('new_events.json', 'w') as file:
            json.dump(new_events, file, default=str, indent=4)
    except Exception as e:
        logger.error(f"Error writing final events to files due to {e}")
    logger.info(f"Successfully removed old events fom new list")
    return new_events


def main():
    events = getUpcommingEvents()
    if events:
        # check if the events have already been discovered
        events = removeDupes(events=events)

    # send email if any updates

# in case this becomes a module
if __name__ == "__main__":
    main()
