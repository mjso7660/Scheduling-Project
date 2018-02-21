![Alt text](feed_parser.jpg?raw=true "Title")
# Scheduling Project
Automates assigning hours for employees of an organization

## Getting Started

cucc.py: file includes the algorithm for matching hours with candidates
spreadsheet.py: helper file for accessing Google spreadsheet

### Prerequisites

#### gspread & oauth2client
```
pip install gspread oauth2client
```
#### Google API and Service Accounts
Need to create a service account and OAuth2 credentials from the Google API console.
Follow the steps mentioned here: (https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)

This will give you client_secret.json. Additionally, you will need an access to the spreadsheet.

## Running the tests

No tests for the current version

## Algorithm
Algorithm for stable marriage, hospital/resident problem. For more, see (https://en.wikipedia.org/wiki/Stable_marriage_problem)

## Authors

* **Min Joon So** - *Initial work* - [mjso7660](https://github.com/mjso7660)
