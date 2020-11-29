import csv
from random import randrange
import sqlite3
import logging

# Generic function to insert into table
def insert_into_db(db_connection, name, dose, number_of_items):
    print("Starting insert medication table")

    if type(name) is str and type(dose) is str and type(number_of_items) is int:
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO medication_table (name, dose, number_of_items) VALUES (?,?,?)", (name, dose, number_of_items))
        
        print("Successfully inserted into medication table")
    else:
        print("Unsuccessful insertion. Data type of input is incorrect")

# autocomplete search database result
def search_database(db_connection, user_input):
    print("Starting search for user's medication choice")

    cursor = db_connection.cursor()
    cursor.execute("SELECT DISTINCT name FROM medication_table WHERE name LIKE ? LIMIT 10", (f'%{user_input}%',))
    search_results = cursor.fetchall()

    print("Finished search for user's medication choice")

    return search_results

# chosen medication results
def chosen_medication_results(db_connection, chosen_medication):
    print("Starting autocomplete search")

    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM medication_table WHERE name = ?", (chosen_medication,))
    medication_results = cursor.fetchall()

    print("Finished autocomplete search")
    
    return medication_results
