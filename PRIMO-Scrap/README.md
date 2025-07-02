# Google Play Store Scraping Automation

PRIMO-Scrap enables the automation of search queries on the Google Play Store platform using **SerpApi** and **google_play_scraper**. The input is a tree structure describing all the queries to be performed. The output is a folder containing JSON files with the details of the executed searches and scraped applications.


## Dataset extraction

### Prerequisites

Scraping is performed using **SerpApi**, which enables the retrieval of application data from the Google Play Store platform, and the **google_play_scraper** library to obtain additional app details.

#### Using SerpApi
1. Create an account at [SerpApi](https://serpapi.com/).
2. Retrieve your personal API key.
3. Replace the API key in the **`.env`** file or directly inside your code functions (see **search_google_play(query)**) to authenticate your requests.

#### Install Required Libraries

Use the following commands to install the required dependencies:

```bash
pip install serpapi
pip install google-play-scraper
``` 

### Main Functions

#### `info_app(idapp)`
Retrieves detailed information about an application using its unique Google Play Store identifier (`idapp`).

#### `search_google_play(query)`
Performs a search on Google Play Store based on the keyword `query` and returns the associated results.

### Final function

#### `arbo_taxonomie`
The **`arbo_taxonomie`** function is the core of the program. It traverses the query tree and performs the necessary searches. It takes a node from the tree as input and executes searches for each node and its synonyms.

Main steps:

1. **Folder Creation**: Creates a directory for each node of the tree where the results will be stored.
2. **App Search**: Performs searches on Google Play Store via **SerpApi** for each node and its synonyms.
3. **Result Collection**: Collects application IDs and fetches their detailed information using google_play_scraper.
4. **Data Saving**: Saves the search results in JSON files.

### Running the Program
To run the program, simply execute the bigtree_scraper.py file.



## Post-processing

**File:** `Extraction.py`

**Description:**
Once the applications are scraped, a second program will browse the local database of created files. It will create a folder named "applications". For each scraped application, this program will create a subfolder named after the application's ID. This subfolder will contain the HTML page of the terms and conditions as well as the app's permissions.

**Function:** `create_folders_app() `

