import time
from random import randint
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
import random
import time
import numpy as np
from datetime import date
import random
import time
import pandas as pd


def scrape_hotel_urls():
    """
    Scrapes the URLs of hotels from a website and saves them to a Feather file.

    The function iterates through a range of pages, extracts the hotel URLs
    from each page, and saves the URLs to a DataFrame. The URLs are then
    updated with the full URL format and saved to a Feather file.

    Returns:
        None
    """
    

    base_url = 'https://www.hotelleriesuisse.ch/de/branche-und-politik/branchenverzeichnis/hotel-page-'
    total_pages = 3
    data = []

    for page in range(1, total_pages + 1):
        url = f"{base_url}{page}"
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')

        # Find all list items with class 'CardGrid--grid-item'
        items = soup.find_all('li', class_='CardGrid--grid-item')

        # Iterate over each item and extract href
        for item in items:
            link = item.find('a')['href']
            data.append({'Link': link})

        # Random sleep timer between 1 and 3 seconds
        sleep_time = randint(1, 3)
        time.sleep(sleep_time)

    # Create a DataFrame from the scraped data
    df = pd.DataFrame(data)

    # Update link column with full URL
    df['Link'] = df['Link'].apply(lambda x: 'https://www.hotelleriesuisse.ch' + x)

    # Save DataFrame to a Feather file
    df.to_feather('hotel_urls.feather')

    # Export the scraped Data
    current_date = date.today().strftime("%Y%m%d")
    filename = f"data/{current_date}_Scraped_Data_Urls.feather"
    df.to_feather(filename)


def scrape_hotel_data(url):
    """
    Scrapes information from a single URL of a hotel and returns the extracted information.

    Args:
        url (str): The URL of the hotel page to scrape.

    Returns:
        dict: A dictionary containing the extracted information from the hotel page.
    """
    # Set a list of user-agent headers to rotate between
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]

    # Set a random user-agent header
    user_agent = random.choice(user_agents)

    # Set headers with the user-agent
    headers = {
        "User-Agent": user_agent
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return None

    try:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract the desired information from the HTML using BeautifulSoup selectors
        hotel_name = soup.find('title').get_text(strip=True) if soup.find('title') else None
        hotel_summary = soup.select_one(".Text--copy.richtext").get_text(strip=True) if soup.select_one(".Text--copy.richtext") else None
        #contact_name = soup.select_one(".Avatar--name").get_text(strip=True) if soup.select_one(".Avatar--name") else None
        address_element = soup.select_one(".Button--label p")
        address_lines = []

        if address_element:
            for content in address_element.contents:
                if isinstance(content, NavigableString):
                    line = content.strip()
                    if line:
                        address_lines.append(line)

        if len(address_lines) >= 2:
            hotelname = address_lines[0]
            strasse = address_lines[1]
            plz_ort = address_lines[2].split(" ")
            plz = plz_ort[0] if len(plz_ort) > 0 else None
            ort = " ".join(plz_ort[1:]) if len(plz_ort) > 1 else None
            adresse_not_mapped = None
        else:
            hotelname = None
            strasse = None
            plz = None
            ort = None
            adresse_not_mapped = address_element



        hotel_features = [tag.get_text(strip=True) for tag in soup.select(".TagList--list--item .BlockLink.active")]

        # Additional Hotel information
        richtext_div = soup.select('div.richtext:not(.Text--copy)')
        richtext_div_html = str(richtext_div)
        soup_richtext_div = BeautifulSoup(richtext_div_html, 'html.parser')
        variables = {strong_tag.previous_sibling.strip(): strong_tag.text.strip() for strong_tag in soup_richtext_div.find_all('strong')}

        check_in = variables.get('Check-In')
        check_out = variables.get('Check-Out')
        zimmer_apartments = variables.get('Zimmer/Apartments')
        betten = variables.get('Betten')
        seminare_bis = variables.get('Seminare bis')
        bankette_bis = variables.get('Bankette bis')

        # Create a dictionary with all the extracted information
        hotel_info = {
            "Hotel": hotel_name,
            "Summary": hotel_summary,
            #"Contact Name": contact_name,
            "Hotelname": hotelname,
            "Strasse": strasse,
            "PLZ": plz,
            "Ort": ort,
            "Adresse_Not_Mapped":adresse_not_mapped,
            "Hotel_Features": hotel_features,
            "Anzahl_Zimmer_Apartments": zimmer_apartments,
            "Anzahl_Betten": betten,
            "Check_In": check_in,
            "Check_Out": check_out,
            "Maximale_Seminargrösse": seminare_bis,
            "Maximale_Bankettgrösse": bankette_bis,
            "url":url
        }

        return hotel_info
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None
    

def scrape_and_export_data():
    """
    Scrape data from a list of URLs, filter relevant columns, convert data types,
    and export the scraped data to a feather file.

    Requires:
        - 'scrape_hotel_data(url)' function to be defined elsewhere for scraping individual URLs.
        - 'scraped_data.feather' file to exist and contain a DataFrame with a 'Link' column.

    Returns:
        None
    """

    # Import urls dataframe
    current_date = date.today().strftime("%Y%m%d")
    df = pd.read_feather(f"data/{current_date}_Scraped_Data_Urls.feather")
    links_to_scrape = df.Link

    # Set a delay range between requests (in seconds)
    min_delay = 0  # Minimum delay
    max_delay = 0.3  # Maximum delay
    delay = random.uniform(min_delay, max_delay)  # Randomize the delay between requests

    # Scrape information from each URL in the list
    scraped_data = []
    for url in links_to_scrape:
        try:
            data = scrape_hotel_data(url)  # Assuming scrape_url() is defined elsewhere
            if data is not None:
                scraped_data.append(data)
            time.sleep(delay)
        except Exception as e:
            print(f"Error occurred while scraping {url}: {str(e)}")

    # Create a DataFrame from the scraped data
    df_hotels = pd.DataFrame(scraped_data)

    # Filter on relevant columns
    df_hotels = df_hotels[
        [
            'Hotel',
            'Summary',
            'Strasse',
            'PLZ',
            'Ort',
            'Hotel_Features',
            'Anzahl_Zimmer_Apartments',
            'Anzahl_Betten',
            'Maximale_Seminargrösse',
            'Maximale_Bankettgrösse',
            'url'
        ]
    ]

    # Replace empty values with NaN
    df_hotels[['Anzahl_Betten', 'Anzahl_Zimmer_Apartments', 'Maximale_Seminargrösse', 'Maximale_Bankettgrösse']] = df_hotels[['Anzahl_Betten', 'Anzahl_Zimmer_Apartments', 'Maximale_Seminargrösse', 'Maximale_Bankettgrösse']].replace('', np.nan)

    # Convert columns to integers
    df_hotels[['Anzahl_Betten', 'Anzahl_Zimmer_Apartments', 'Maximale_Seminargrösse', 'Maximale_Bankettgrösse']] = df_hotels[['Anzahl_Betten', 'Anzahl_Zimmer_Apartments', 'Maximale_Seminargrösse', 'Maximale_Bankettgrösse']].astype(float).astype(pd.Int64Dtype())

    # Export the scraped Data
    current_date = date.today().strftime("%Y%m%d")
    filename = f"data/{current_date}_Scraped_Data_Hotels.feather"
    df_hotels.to_feather(filename)
    



#######
# Run #
#######

##############
# Scrape_URLS #
##############
print("Starting scraping urls...")
scrape_hotel_urls()
print("Scraping urls finished")

######################
# Scrape Hotelsdata #####
######################

print("Starting scraping hoteldata...")
scrape_and_export_data()
print("finished scraping hoteldata")



