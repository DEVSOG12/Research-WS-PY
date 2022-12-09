# Research-WS-PY 
[![Python application](https://github.com/DEVSOG12/Research-WS-PY/actions/workflows/python-app.yml/badge.svg)](https://github.com/DEVSOG12/Research-WS-PY/actions/workflows/python-app.yml)
## Python Implentation Web Scraping Algorithm. BS4.

## Introduction
This project is a research project to scrape data from a website. The project is built using Python and the following libraries are used:
* BeautifulSoup4
* Requests
* urllib
* pdfkit
* PyPDF2


## Installation
Run the following command to install the required libraries:
```bash
pip install -r requirements.txt
```

## Usage
The project is divided into two parts:
* Scraping data
* Analyzing data
* Creating PDF
* Creating TXT

### Scraping data
The data is scraped using the following steps:
* Within the `./src/scraper.py` file, the URL is defined to scrape data from and the data is stored in the `./data` folder as a .csv file
* Run the `main.py` file
* The data is scraped and stored in the ./outputs folder

### Analyzing data
The data is analyzed using the following steps:
