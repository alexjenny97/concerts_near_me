# Project: Concerts Near Me

## Problem Summary: 
Many venues and shows happening around Denver make it difficult to easily find relevent event data such as:
- who is playing
- when the show is
- where the show is
- the tour poster
- a link for tickets

Getting this data via scrolling multiple sites & emails takes much more time than reading one personalized email.

## Solution Summary: 
Build a process that scrapes relevent show data (listed above & more), cleans & formats the data, then if new events have been found, emails me just the new shows.

## Expected Set Up:
1. Configure credentials file (not made)
1. Configure local machine to run script every day
2. Run program (python main.py) in the virtual enviornment
3. Recieve first email, save sender

## Expected Workflow:
1. First email will be large with all current events from all venues in the credentials package

2. Script runs every day at a set time & compiles an email

3. Subsequent emails with be sent on a basis set in the credentials file with new events

#### Note: If no new events, no email will be sent

## Current Status:
Program curently gets info from Fiddler's Green Ampitheater and puts what would be the email data into "new_events.json".

## Next Steps:
1. Make credentials file
1. Configure email connection
1. Add Mission Ballroom as next venue

## Additional Details:
1. Venues must be manually added to script

    - More research is required to see if sites are similar enough to make adding a new vennue more streamlined.

    - Not in the project's initial scope to make adding new venues easy

## Possible Improvements:
- Connect with Spotify for further data gathering
    - Such as new artists to highlight


