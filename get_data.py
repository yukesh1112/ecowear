import pandas as pd
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# Set the correct path for chromedriver
DRIVER_PATH = 'D:\mini_project\HACKATHON\GreenStyle-main\chromedriver.exe'

# Initialize ChromeDriver
service = Service(DRIVER_PATH)
wd = webdriver.Chrome(service=service)

# Read the previously scraped data
df = pd.read_csv('D:\mini_project\HACKATHON\GreenStyle-main\tops.csv')
brand_link = df['brand link']

# Helper function to assign numeric ratings
def rate_change(t):
    if t == 'We avoid':
        return 1
    elif t == 'Not good enough':
        return 2
    elif t == "It's a start":
        return 3
    elif t == 'Good':
        return 4
    elif t == 'Great':
        return 5
    else:
        return 0

# Initialize empty lists for data
brand_site = []
brand_name = []
brand_rate = []
brand_price = []
brand_rec = [] 
brand_r1 = []
brand_r2 = []
brand_r3 = []
brand_store = []

base = 'https://directory.goodonyou.eco'

# Loop through each brand link and scrape data
for i, l in enumerate(brand_link):
    brand_url = base + l
    store_name = l.split('/')[2]
    
    # Open brand page
    wd.get(brand_url)
    time.sleep(7.5)
    
    # Parse the page
    soup = bs(wd.page_source, "lxml")
    span = soup.find_all("span", class_='StyledText-sc-1sadyjn-0 bBUTWf')
    
    # Handle cases where rating and price might not be present
    if len(span) >= 2:
        try:
            rating = span[0].text.split(': ')[1]
            rate_num = rate_change(rating)
            price = span[1].text.split(': ')[1]
        except IndexError:
            rate_num = 0
            price = 0
    else:
        rate_num = 0
        price = 0
    
    brand_rate.append(rate_num)
    brand_price.append(price)
    
    # Scrape brand recommendations
    brand_rec = ["", "", ""]
    brand_div2 = soup.find_all('div', class_="StyledBox-sc-13pk1d4-0 hkSFzT")
    
    for j, element in enumerate(brand_div2):
        if j == 3:
            break
        brand_rec[j] = element.h5.text
    
    # Append recommendations
    brand_r1.append(brand_rec[0])
    brand_r2.append(brand_rec[1])
    brand_r3.append(brand_rec[2])
    brand_store.append(store_name)

# Create DataFrame and save as CSV
df2 = pd.DataFrame({
    'store name': brand_store,
    'rating': brand_rate,
    'price': brand_price,
    'r1': brand_r1,
    'r2': brand_r2,
    'r3': brand_r3
})

# Save to CSV
df2.to_csv('D:\mini_project\HACKATHON\GreenStyle-main\db.csv', index=False)

# Close the browser
wd.quit()
