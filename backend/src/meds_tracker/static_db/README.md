meds-tracker source data
========================

The Python scripts in this directory are responsible for downloading and
processing of source data:

* Known medication products: Scraped from https://bnf.nice.org.uk/drugs/
* UK postal code areas: https://www.getthedata.com/open-postcode-geo 
* Pharmacy branches: https://opendata.nhsbsa.net/dataset/consolidated-pharmaceutical-list

We will not store the original source data in this directory - only the
scripts for downloading it from publicly available sources, and the scripts
for converting that data into an SQLite+SpatiaLite database consumable by
the backend service.

The source data from official sources may in some circumstances require
additions or modification; any corrections or additions we make will be done
here in code and overlay data files.