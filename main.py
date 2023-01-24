import datetime
import sqlite3
from connection_db import create_connection, execute_query, execute_read_query
from flask import Flask, request
from flask import render_template
import re

app = Flask(__name__)


@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/congres")
def congres_list():
    connection = get_connection()

    query = """
    SELECT *
    FROM congres
    """

    list_congres = execute_read_query(connection, query)

    column_names = []
    if (len(list_congres) > 0):
        column_names = list_congres[0].keys()

    return render_template('congres/list.html', column_names=column_names, list_elements=list_congres)


@app.route("/participants")
def participants_list():
    connection = get_connection()

    query = """
    SELECT *
    FROM participants
    """

    list_participants = execute_read_query(connection, query)

    column_names = []
    if (len(list_participants) > 0):
        column_names = list_participants[0].keys()

    return render_template('participants/list.html', column_names=column_names, list_elements=list_participants)

@app.route("/participants/add")
def participants_add():
    connection = get_connection()

    query = """
    SELECT *
    FROM statuts
    """

    list_statuts = execute_read_query(connection, query)

    return render_template('participants/add.html', list_statuts=list_statuts)
    
@app.route("/participants/new", methods=["POST"])
def participants_new():

    keys_validation = {
        'CODESTATUT': ['required'], 
        'NOMPART': ['required'], 
        'PRENOMPART': ['required'], 
        'ORGANISMEPART': ['required'], 
        'CPPART': ['required'], 
        'ADRPART': ['required'], 
        'VILLEPART': ['required'], 
        'PAYSPART': ['required'], 
        'EMAILPART': ['required', 'email'], 
    }

    errors = form_validate(request.form, keys_validation)

    is_valid = len(errors) == 0

    connection = get_connection()
    
    column_names = fetch_column_names(keys_validation)
    column_names.append('DTINSCRIPTION')
    columns = ', '.join(column_names)

    x = datetime.datetime.now()
    now_date = x.strftime("%Y-%m-%d")

    values = []
    values.append(request.form.get('CODESTATUT'))
    values.append("'{}'".format(request.form.get('NOMPART')))
    values.append("'{}'".format(request.form.get('PRENOMPART')))
    values.append("'{}'".format(request.form.get('ORGANISMEPART')))
    values.append("'{}'".format(request.form.get('CPPART')))
    values.append("'{}'".format(request.form.get('ADRPART')))
    values.append("'{}'".format(request.form.get('VILLEPART')))
    values.append("'{}'".format(request.form.get('PAYSPART')))
    values.append("'{}'".format(request.form.get('EMAILPART')))
    values.append("'{}'".format(now_date))

    values_str = ', '.join(values)

    query = f"INSERT INTO participants ({columns}) VALUES ({values_str})"

    execute_query(connection, query)

    return render_template('participants/new.html', errors=errors, is_valid=is_valid)

def fetch_column_names(keys_validation: dict) -> list:
    response = []
    for key in keys_validation.keys():
        response.append(key)

    return response

def get_connection() -> sqlite3.Connection:
    """Implémentation de la récupération de la BD commune

    Returns:
        sqlite3.Connection: La connection à la BD
    """
    db_path = './db/bd_congres.db'
    connection = create_connection(db_path)

    return connection

def form_validate(form: any, keys_validation: dict) -> list:
    error_messages = []
    for key, values in keys_validation.items():
        if ('required' in values):
            if (form.get(key) is None):
                error_messages.append(f"Le champs {key} n'est pas présent dans le formulaire, veuillez renseigner une donnée")
            elif (form.get(key) == ''):
                error_messages.append(f"Le champs {key} est vide, veuillez renseigner une valeur")
        if ('email' in values):
            pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            est_email = re.match(pat, form.get(key))
            if (not est_email):
                error_messages.append(f"Le champs {key} doit être un email valide (ex : nom.prenom@example.com). Veuillez réessayer")
    return error_messages

if (__name__ == '__main__'):

    host = '127.0.0.1'
    port = 5000
    debug = True

    app.run(host, port, debug)
