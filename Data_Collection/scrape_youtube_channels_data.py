import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# List of countries and their URLs
countries = {
    'in': 'India', 'us': 'USA', 'br': 'Brazil', 'id': 'Indonesia',
    'mx': 'Mexico', 'jp': 'Japan', 'de': 'Germany', 'vn': 'Vietnam',
    'ph': 'Philippines', 'tr': 'Turkey', 'pk': 'Pakistan', 'gb': 'UK',
    'eg': 'Egypt', 'fr': 'France', 'th': 'Thailand', 'bd': 'Bangladesh',
    'kr': 'ROK', 'it': 'Italy', 'es': 'Spain', 'ar': 'Argentina',
    'au': 'Australia', 'ca': 'Canada'
}

output_dir = 'Data'
os.makedirs(output_dir, exist_ok=True)

excel_files = []

# Loop through each country
for country_code, country_name in countries.items():
    url = f'https://vidiq.com/youtube-stats/top/country/{country_code}/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    all_data = []
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
        # Save country-wise data to Excel
        df = pd.DataFrame(all_data)
        country_file = os.path.join(output_dir, f'YouTube_Channels_Stats_{country_name}.xlsx')
        df.to_excel(country_file, index=False)
        excel_files.append(country_file)
        print(f"Saved data for {country_name} to {country_file}")
        time.sleep(5)
    except Exception as e:
        print(f"Error scraping {country_name}: {str(e)}")

# Merge all country files into one final Excel file
final_df = pd.concat([pd.read_excel(f) for f in excel_files], ignore_index=True)
final_file = os.path.join(output_dir, 'Final_Merged_Youtube_Channels_Stats.xlsx')
final_df.to_excel(final_file, index=False)
print(f"All data merged and saved to {final_file}")