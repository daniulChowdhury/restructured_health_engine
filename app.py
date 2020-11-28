from flask import Flask, render_template, request, jsonify
from medication_db_functions import search_database, chosen_medication_results, create_table, create_data, populate_table
import sqlite3
import logging

app = Flask(__name__)

@app.before_first_request
def init_db():
    create_table()
    drug_data = create_data()
    populate_table(drug_data)
    print("Finished initialising database and table")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/result', methods=["POST"])
def result():
        medication_name = request.form.get("search_medication")
        if not medication_name:
            return render_template("index.html")
        else :
            database_results = chosen_medication_results(medication_name)
            return render_template("result.html", results=database_results)


@app.route('/autocomplete', methods=['POST', 'GET'])
def autocomplete():
    search_input = request.form.get('user_input')
    autocomplete_results = search_database(search_input)
    return jsonify(autocomplete_results)


if __name__ == "__main__":
    app.run(debug=True)
