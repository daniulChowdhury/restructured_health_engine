from flask import Blueprint, render_template, jsonify, request
from app.medication_db_functions import chosen_medication_results, search_database
from app.db import get_db
import logging

bp = Blueprint('search', __name__)

@bp.route('/')
def index():
    return render_template("search/index.html")


@bp.route('/result', methods=["POST"])
def result():
    db_conn = get_db()
    medication_name = request.form.get("search_medication")
    if not medication_name:
        return render_template("search/index.html")
    else :
        database_results = chosen_medication_results(db_conn, medication_name)
        return render_template("search/result.html", results=database_results)


@bp.route('/autocomplete', methods=['POST', 'GET'])
def autocomplete():
    db_conn = get_db()
    search_input = request.form.get('user_input')
    autocomplete_results = search_database(db_conn, search_input)
    return jsonify(autocomplete_results)