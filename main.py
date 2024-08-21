from __future__ import print_function
import requests
# from bs4 import BeautifulSoup
import logging
import logging.config
import json
import urllib.request, json 
# from requests_html import HTMLSession
import time 
# import pandas as pd 
from selenium import webdriver
from selenium.webdriver import Chrome 
from selenium.webdriver.common.by import By 
from datetime import datetime
from googleapiclient.discovery import build
from apiclient import errors
import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from requests import HTTPError
import html
from email.message import EmailMessage
from email.utils import make_msgid
from PIL import Image

import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from apiclient.discovery import build
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


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

schema_mapping = {'fiddlers green': {'main_div': 'c-axs-event-card__wrapper','ticket_div': 'BUY TICKETS', 'poster_div': 'u-img-respond'}}

def connectToSite(venue, venue_url):
     # try to connect to venue website
    try:
        logger.info(f'Getting event data for {venue}')
        url = venue_url
        driver.get(url)
        content = driver.find_elements(By.CSS_SELECTOR, f"div[class*='{schema_mapping[venue]['main_div']}']")
        # ticket_links = content.find_elements(By.PARTIAL_LINK_TEXT, schema_mapping[venue]['ticket_div'])
        # print(f"TEST TEST: {ticket_links[0]}")
        # if content:
        #     print(content[0].find_element(By.PARTIAL_LINK_TEXT, schema_mapping[venue]['ticket_div']).get_attribute('href'))
     

    except Exception as e:
        logger.error(f'Error getting event data for {venue} due to {e}')

    return content


def getEventDetails(event, venue):
    try:
            event_text = event.text.split("\n")
            
            details = {}
            details['artist']  = event_text[0] + event_text[1]
            details['date'] = event_text[2]
            # details['price'] = ''
            details['show_time'] = event_text[3]
            details['ticket_link'] = event.find_element(By.PARTIAL_LINK_TEXT, schema_mapping[venue]['ticket_div']).get_attribute('href')
            details['tour_poster'] = event.find_element(By.CSS_SELECTOR, f"img[class*='{schema_mapping[venue]['poster_div']}']").get_attribute('src')
            details['venue'] = venue


            return details
    except Exception as e:
        logger.error(f"Failed getting event details due to {e}")

def getUpcommingEvents():
    # events is a list of dictionaries
    # events[x] = {'artist': artist, 'venue': venue, 'date': date, 'show_time' : show_time, 'price' : price (future update),
                #  'ticket_link': ticket_link, 'tour_poster': tour_poster}
    events = []
    for venue, venue_url in url_mapping.items():
       try:
        venue_events  = connectToSite(venue=venue, venue_url=venue_url)
        for event in venue_events:
            if event.text: 
                events.append(getEventDetails(event=event, venue=venue))
            else: 
                del event

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
            if old_events:
                old_events = old_events['old_events'] 
                logger.info(f"Successfully opened old events file.")
            else: 
                logger.info(f"No old events.")
    except Exception as e:
        logger.error(f"Error opening old event file due to {e}")
    
    if old_events:
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
        except Exception as e:
            logger.error(f"Error removing duplicates due to {e}")
    else: 
        new_events = events
    
    try:
        with open('previous_events.json', 'w') as file:
            json.dump(old_events, file, default=str, indent=4)
        with open('new_events.json', 'w') as file:
            json.dump(new_events, file, default=str, indent=4)
    except Exception as e:
        logger.error(f"Error writing final events to files due to {e}")
    logger.info(f"Successfully removed old events fom new list")
    return new_events

def build_service(SCOPES):
    # """Build a Gmail service object.

    # Args:
    #     credentials: OAuth 2.0 credentials.

    # Returns:
    #     Gmail service object.
    # """
    from google.oauth2 import service_account

    SERVICE_ACCOUNT_FILE = 'gmail_creds.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    http = httplib2.Http()
    http = credentials.authorize(http)
    return build('gmail', 'v1', http=http)

def formatMessage(events):
    try:
        message = f"Hello! There are some new events you might be inrerested in!\n"
        for event in events:
            message = message + f"\n{event['artist']} is playing at {event['venue']} on {event['date']} at {event['show_time']}. \n{event['tour_poster']} \n{event['ticket_link']}\n \n "
        return message

    except Exception as e:
        logger.error(f"Failed formatting the email messsage due to {e}")

def sendEmail(events):
    if events[0]:
        message = formatMessage(events)
        logger.info(message)
        try:
            SCOPES = [
                    "https://www.googleapis.com/auth/gmail.send"
                ]
            # flow = InstalledAppFlow.from_client_secrets_file(
            #             'gmail_creds.json', SCOPES)
            # creds = flow.run_local_server(port=0)
            # service = build_service(SCOPES=SCOPES)
            creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "gmail_creds.json", SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                    with open("token.json", "w") as token:
                        token.write(creds.to_json())
            service = build("gmail", "v1", credentials=creds)
            message = MIMEText(message)
            message['to'] = 'alexjenny97@gmail.com'
            message['subject'] = 'Email Subject'
            create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
            try:
                message = (service.users().messages().send(userId="me", body=create_message).execute())
                print(F'sent message to {message} Message Id: {message["id"]}')
            except HTTPError as error:
                print(F'An error occurred: {error}')
                message = None
        except Exception as e:
            logger.error(f"Error sending email due to {e}")

    


def main():
    events = getUpcommingEvents()
    if events:
        # check if the events have already been discovered
        try:
            events = removeDupes(events=events)
            sendEmail(events=events)
        except Exception as e:
            logger.error(f"Error due to {e}")


    # send email if any updates

# in case this becomes a module
if __name__ == "__main__":
    main()
