# Project: Concerts Near Me

## Problem Summary: 
Many venues and shows happening around Denver make it difficult to easily find relevent event data such as:
- who is playing
- when the show is
- where the show is
- the tour poster
- a link for tickets

Getting this data via scrolling multiple sites & emails takes much more time than reading one personalized email. There should be a script to run that will send the formatted details as an email. 

## Solution MVP: 
1. One venue's data will be a proof of concept.
     - This will set up Selenium, webscraping and connecting to the Gmail API.
       
3. Data must include date, time, venue and artist.
     - Other attributes are acceptable, this is the bare minimum.
     - **Final MVP includes: date, time, venue, artist, ticket link and a link to the tour poster**
       
4. The email must not send duplicate events for consecuitive emails.
      - Repeating events is not a scaleable solution as the number of venues increases.
#### Note: If no new events, no email will be sent


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





## Current Status:
- Program curently gets info from Fiddler's Green Ampitheater and **if not commented out** adds the events to the "previous_events.json" file, then emails the events. Below is a snapshot of an email sent.
  <img width="722" alt="image" src="https://github.com/user-attachments/assets/f654d4a1-2ec5-40ef-9078-cd7fddaa0af6">

- Program stores Gmail credentials and uses them in subsequent runs so the user does not need to allow the program access every run. 

## Possible Next Steps:
1. Next venue: Mission Ballroom.
2. Add price of general admission ticket into the email.
3. Connect to Spotify API to bold small artists that are known and might be missed. 



