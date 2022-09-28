# adata-nbs

## Installation

On Windows you can use the "windows_scripts" folder after pulling the repo.

There you can find a .cmd file which is called "install_requirements" if you have <a href="https://pip.pypa.io/en/stable/installation/">pip</a> installed just run it and all the requirements will be installed for you.

On other platforms you will need to run this command in the main folder for the requirements to be installed.

```bash
pip install -r requirements.txt
```

## Usage
If you are using Windows you can find the scripts for running the scraper and the api inside "windows_scripts" folder.

"start_scrapper.cmd" will initiate the spyder.

"start_rest.cmd" will start the REST endpoint.

on other platforms:

```
# STARTING THE SCRAPER
scrapy crawl nbs_article

# STARTING THE API 
uvicorn api:app --reload
```
