import csv
from random import randrange
import sqlite3
import logging

# creating data for table from OPENFDA file
def create_data():
    drug_storage = []
    with open('database/Products.txt', newline ='') as drugs:
        drug_reader = csv.reader(drugs, delimiter='\t')
        for idx, drug in enumerate(drug_reader):
            if '' not in drug:
                drug_name = drug[5] + ' ' + drug[2]
                drug_data = [drug_name, drug[3], randrange(1000),]
                drug_storage.append(drug_data)
    
    print("Successfully created data")

    return drug_storage

# create table from schema file
def create_table():
    conn = None
    try:
        conn = sqlite3.connect('database/medication_table.db')
        cursor = conn.cursor()
    except sqlite3.Error as err:
        logging.error(err.message)

    # create table for medication uses
    with open('database/schema.sql') as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()
    print("Successfully created medication table and database")

# insert data from OPENFDA into Table
def populate_table(drug_storage):
    conn = None
    try:
        conn = sqlite3.connect('database/medication_table.db')
        cursor = conn.cursor()
    except sqlite3.Error as err:
        logging.error(err.message)
    
    for drug in drug_storage:
        cursor.execute("INSERT INTO medication_table (name, dose, number_of_items) VALUES (?,?,?)", (drug[0], drug[1], drug[2]))

    conn.commit()
    conn.close()
    print("Successfully inserted into medication table")

# Generic function to insert into table
def insert_into_db(name, dose, number_of_items):

    if type(name) is str and type(dose) is str and type(number_of_items) is int:
        conn = None
        try:
            conn = sqlite3.connect('database/medication_table.db')
            cursor = conn.cursor()
        except sqlite3.Error as err:
            logging.error(err.message)
        
        cursor.execute("INSERT INTO medication (name, dose, number_of_items) VALUES (?,?,?)", (name, dose, number_of_items))
        conn.commit()
        print("Successfully inserted into medication table")
        conn.close()
    else:
        print("Unsuccessful insertion. Data type of input is incorrect")

# autocomplete search database result
def search_database(user_input):

    try:
        conn = sqlite3.connect('database/medication_table.db')
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT name FROM medication_table WHERE name LIKE ? LIMIT 10", (f'%{user_input}%',))
        search_results = cursor.fetchall()
        conn.close()
    except sqlite3.Error as err:
        logging.error(err.message)

    return search_results

# chosen medication results
def chosen_medication_results(chosen_medication):
    try:
        conn = sqlite3.connect('database/medication_table.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medication_table WHERE name = ?", (chosen_medication,))
        medication_results = cursor.fetchall()
        conn.close()
    except sqlite3.Error as err:
        logging.error(err.message)

    return medication_results

    
# initialise once to create database and table
def init_db():
    create_table()
    drug_data = create_data()
    populate_table(drug_data)
    print("Finished initialising database and table")