meds-tracker backend
====================

This is an API server which returns the data in REST+JSON format and provides 
a GraphQL interface (TO DO).

It relies on:
* echo
* gorm
* postgres+postgis
* gogeos

It does three things:
1. Query for medication reports in your area (geolocation / by postcode)
2. Handle submission of medication reports
3. Handle submission of new medication type / new pharmacy branch type
   * This data will be 