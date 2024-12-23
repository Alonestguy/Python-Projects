import requests
from bs4 import BeautifulSoup
import mysql.connector

# MySQL connection details
db_config = {
    'user': 'Host Name',
    'password': 'Pass',
    'host': 'IP ',
    'database': 'Name Created'
}

# Function to save data to MySQL database
def save_to_database(countries):
    # Connect to MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insert countries data into the table
    insert_query = '''
        INSERT INTO countries (name, capital, population, area) 
        VALUES (%s, %s, %s, %s)
    '''
    cursor.executemany(insert_query, countries)

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()

# Function to retrieve data from MySQL database
def retrieve_from_database():
    # Connect to MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Fetch data from the table
    cursor.execute('SELECT name, capital, population, area FROM countries')
    result = cursor.fetchall()

    # Print the fetched data
    for row in result:
        print(f"Name: {row[0]}, Capital: {row[1]}, Population: {row[2]}, Area: {row[3]}")

    # Close connection
    cursor.close()
    conn.close()

# Fetch data from Scrapethissite
url = 'https://scrapethissite.com/pages/simple/'
response = requests.get(url)
if response.status_code != 200:
    print("Failed to retrieve the webpage")
    exit()

# Parse HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract countries data
country_list = soup.find_all('div', class_='col-md-4 country')
countries = []

for country in country_list[:20]:  # Select the first 20 countries
    name = country.find('h3', class_='country-name').text.strip()
    capital = country.find('span', class_='country-capital').text.strip()
    population = int(country.find('span', class_='country-population').text.strip().replace(',', ''))
    area = float(country.find('span', class_='country-area').text.strip().replace(',', ''))

    countries.append((name, capital, population, area))

# Save data to MySQL database
save_to_database(countries)
print("Data saved successfully!")

# Retrieve and print stored data
retrieve_from_database()
