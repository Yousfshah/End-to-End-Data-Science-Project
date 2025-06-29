import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List of countries and their URLs
countries = {
    'in': 'India', 'us': 'USA', 'br': 'Brazil', 'id': 'Indonesia',
    'mx': 'Mexico', 'jp': 'Japan', 'de': 'Germany', 'vn': 'Vietnam',
    'ph': 'Philippines', 'tr': 'Turkey', 'pk': 'Pakistan', 'gb': 'UK',
    'eg': 'Egypt', 'fr': 'France', 'th': 'Thailand', 'bd': 'Bangladesh',
    'kr': 'ROK', 'it': 'Italy', 'es': 'Spain', 'ar': 'Argentina',
    'au': 'Australia', 'ca': 'Canada'
}

all_data = []

# Loop through each country
for country_code, country_name in countries.items():
    url = f'https://vidiq.com/youtube-stats/top/country/{country_code}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        table_data = soup.find(class_='w-full min-w-[600px] lg:min-w-0')
        
        if table_data:
            rows = table_data.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                if cols:
                    row_data = {
                        'Rank': cols[0].text.strip(),
                        'Channel': cols[1].text.strip(),
                        'Videos': cols[2].text.strip(),
                        'Subscribers': cols[3].text.strip(),
                        'Views': cols[4].text.strip(),
                        'Country': country_name
                    }
                    all_data.append(row_data)
        
        # Add a small delay to be respectful to the server
        time.sleep(5)
        
    except Exception as e:
        print(f"Error scraping {country_name}: {str(e)}")

# Create DataFrame with all data
df = pd.DataFrame(all_data)

# save into excel file
df.to_excel('./Data/YouTube_Channels_Data.xlsx', index=False)