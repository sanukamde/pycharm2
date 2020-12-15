import sqlite3
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


class MySQLite:
    def __init__(self):
        self.page_name = "https://en.wikipedia.org/wiki/List_of_countries_by_carbon_dioxide_emissions"
        self.table_connect = sqlite3.connect('co2_table.db')
        self.country = []
        self.emissions = []

    def build_SQLite_table(self):
        temp_table_create_query = '''CREATE TABLE IF NOT EXISTS Database (id INTEGER PRIMARY KEY, country STRING,
        emissions REAL); '''
        self.table_connect.execute(temp_table_create_query)

    def close_SQLite_table(self):
        self.table_connect.close()

    def sort_SQLite_table(self):
        sort_data_query = "SELECT country,emissions  FROM Database ORDER BY emissions DESC"
        cursor = self.table_connect.execute(sort_data_query)
        myresult = cursor.fetchall()
        counter = 0
        for x in myresult:
            if counter >= 10:
                break
            self.country.append(x[0])
            self.emissions.append(x[1])
            counter += 1

    def graph_builder(self):
        cursor = self.table_connect.execute("SELECT id, country, emissions from Database")
        counter = 0
        for row in cursor:
            if counter >= 10:
                break
            self.country.append(row[1])
            self.emissions.append(row[2])
            counter += 1

    def scrape_webpage(self):
        page = requests.get(self.page_name)
        soup = BeautifulSoup(page.content, 'html.parser')
        insert_data_query = '''INSERT OR IGNORE INTO Database (id, country, emissions) VALUES (?,?,?) '''
        id_count = 0
        table = soup.find("table", {"class": "wikitable sortable"})
        rows = table.find_all('tr')
        for row in rows:
            data = row.find_all('td')
            data = [x.text.strip() for x in data]
            if len(data) <= 0:
                continue
            if "World" in data[0]:
                continue
            data_tuple = (id_count, str(data[0]), float(data[4][:-1]))
            id_count += 1
            self.table_connect.execute(insert_data_query, data_tuple)
        self.sort_SQLite_table()
        self.table_connect.commit()

    def build_pie_chart(self):
        plt.pie(self.emissions, labels=self.country, labeldistance=1.1, startangle=95, textprops={'fontsize': 7})
        plt.axis('equal')
        plt.show()
