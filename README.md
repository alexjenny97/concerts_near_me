# Project: Concerts Near Me
# This project is currently on hold. Priotities have shifted and the main goal (create a working web scraper that connects to a free API to keep skills sharp) has been accomplished. 

## Project Summary: 
Denver is full of fun events! Mac & cheese celebrations, concerts, local festivals, parades, and more happen all over Denver and the surrounding cities. To make the process of finding and comparing events more effiecnt, I created a process to web scrape certain sites (starting with Fiddler's Green for scope management), that emails the events to my personal gmail email. This is done by using Selenium & Python to get the web data and Gmail API to send the email. With the foundataion set, the next step is to gather and format data from the Denver city website to add diversity to the events given. 

The data is given in the form:

ARTIST is playing at VENUE at SHOW_TIME on SHOW_DATE
LINK TO POSTER
LINK TO EVENT

## Files:
previous_events.json
- This tracks the previous events obtained from earlier runs of the process. 
- This could become enough data to analyze later for things like: favorite venue, cheapest venue, if prices are cheaper during some part of the year, most active areas, ect.
    
getting_price.md
- This is a plan on how to get the price of the tickets. 
- This was not part of the MVP but may be a later update.
    
gmail_creds.json
- This is the gmail credentials to run the process. 
- The format neede is:
- 
        {"installed":
              {
              "client_id":"stuff",
              "project_id":"stuff",
              "auth_uri":"stuff",
              "token_uri":"stuff",
              "auth_provider_x509_cert_url":"stuff",
              "client_secret":"stuff",
              "redirect_uris":["stuff"]
              }
        }

## Example of current email. 
  <img width="722" alt="image" src="https://github.com/user-attachments/assets/f654d4a1-2ec5-40ef-9078-cd7fddaa0af6">

## Possible Next Steps:
1. Next site: Denver city website.
2. Add price of general admission ticket into the email.
3. Connect to Spotify API to bold small artists that are known and might be missed.
4. Analyze the venues to see if prices rise closer to the event date.



