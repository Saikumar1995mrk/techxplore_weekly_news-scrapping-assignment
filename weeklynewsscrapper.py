import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# File path to save the CSV
file_path = "techxplore_weekly_news_10.csv"

# Create an empty DataFrame with the desired columns
df = pd.DataFrame(columns=["URL", "Title", "Description", "Base_url"])

# Save the empty DataFrame to create the file with headers if it doesn't exist
if not os.path.isfile(file_path):
    df.to_csv(file_path, index=False)

for i in range(1, 11):
    base_url = f"https://techxplore.com/weekly-news/page{i}.html"

    # Define the headers
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": "deviceType=desktop_f1f6b29a6cc1f79a0fea05b885aa33d0m; _ga=GA1.1.842814392.1720689934; __qca=P0-1903064963-1720689933609; __gads=ID=a41dbcc2d94be6ab:T=1720689978:RT=1720689978:S=ALNI_MZrFeQSEYY1Uz5kNdawwsSWhom7Rg; __eoi=ID=c03e8b782bd2c465:T=1720689978:RT=1720689978:S=AA-Afja6bZTzpvMS7T_F7jKk3Brj; FCNEC=%5B%5B%22AKsRol-Uw_UBRxBQ3obTlUNhqNxzxfN2TvRyJ9xOI3TZQ3H4LywDKFL7UEN1SpbYQPPS8FFH5ENppv9K4B0V5eHAqn-M5-_AzyG6MpmVGBp7XyUsavMHcJMjrKqEJxG7rSzP-vdqlvxUsI15YzP3Li5N7qn4CJHTiw%3D%3D%22%5D%5D; _ga_XXEZ1QMTTS=GS1.1.1720689933.1.1.1720691052.0.0.0; mediavine_session={%22depth%22:18%2C%22referrer%22:%22https://teams.microsoft.com/%22}",
        "Priority": "u=0, i",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\", \"Google Chrome\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }

    # Make the HTTP request
    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all <div> tags with class "sorted-article-content d-flex flex-column"
        div_tags = soup.find_all("div", class_="sorted-article-content d-flex flex-column")

        # List to store the extracted data
        data = []

        # Extract and append the data to the list
        for div in div_tags:
            h2_tag = div.find("h2", class_="text-middle mb-3")
            if h2_tag:
                a_tag = h2_tag.find("a")
                if a_tag and 'href' in a_tag.attrs:
                    url = a_tag['href']
                    title = a_tag.text.strip()

            p_tag = div.find("p", class_="mb-4")
            if p_tag:
                description = p_tag.text.strip()

            # Append data to the list
            data.append({"URL": url, "Title": title, "Description": description, "Base_url": base_url})

        # Convert the list to a DataFrame
        df = pd.DataFrame(data)

        # Append the DataFrame to the CSV file
        df.to_csv(file_path, mode='a', header=False, index=False)

        print(f"Data from {base_url} saved to {file_path}")

    else:
        print(f"Failed to retrieve the webpage at {base_url}. Status code: {response.status_code}")
