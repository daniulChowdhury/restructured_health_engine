import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import csv
from random import randrange

# connect to database
def connect_db():
    rv = sqlite3.connect(current_app.config['DATABASE'])
    print("Connecting to database specified in app.config")

    return rv

# open database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    
    print("Opening database for use")

    return g.sqlite_db

# close database connection
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
    print('connection is closed')

# create the database
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# creating data for table from OPENFDA file
def create_data():
    drug_storage = []
    print("Creating data for database with OPENFDA information")

    with open('app/table_information/Products.txt', newline ='') as drugs:
        drug_reader = csv.reader(drugs, delimiter='\t')
        for idx, drug in enumerate(drug_reader):
            if '' not in drug:
                drug_name = drug[5] + ' ' + drug[2]
                drug_data = [drug_name, drug[3], randrange(1000),]
                drug_storage.append(drug_data)
    
    print("Successfully created data")

    return drug_storage

# insert data from OPENFDA into Table
def populate_table(drug_storage = create_data()):
    print("Populating database with data from OPENFDA information")

    db = get_db()
    cursor = db.cursor()
    for drug in drug_storage:
        cursor.execute("INSERT INTO medication_table (name, dose, number_of_items) VALUES (?,?,?)", (drug[0], drug[1], drug[2]))

    db.commit()
    print("Successfully inserted into medication table")

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    populate_table()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)