from backEnd import *

def display_results():
    sql = MySQLite()
    sql.build_SQLite_table()
    sql.scrape_webpage()
    sql.build_pie_chart()
    sql.close_SQLite_table()

display_results()