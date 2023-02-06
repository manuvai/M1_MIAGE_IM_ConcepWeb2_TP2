import datetime
import sqlite3
from Database import Database
from CongresTable import CongresTable
from ActivitesTable import ActivitesTable
from ThematiquesTable import ThematiquesTable
from ParticipantsTable import ParticipantsTable
from StatutsTable import StatutsTable
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
    db = Database.get_instance()
    congresTable = CongresTable(db)

    list_congres = congresTable.all()

    column_names = []
    if (not list_congres is None and len(list_congres) > 0):
        column_names = list_congres[0].keys()
    else:
        list_congres = []

    return render_template('congres/list.html', column_names=column_names, list_elements=list_congres)

@app.route("/congres/add")
def congres_add():
    list_thematiques = []
    list_activites = []

    activitesTable = ActivitesTable(Database.get_instance())
    list_activites = activitesTable.all()

    thematiquesTable = ThematiquesTable(Database.get_instance())
    list_thematiques = thematiquesTable.all()

    return render_template('congres/add.html', list_thematiques=list_thematiques, list_activites=list_activites)

@app.route("/congres/new", methods = ['POST'])
def congres_new():

    keys_validation = {
        'TITRECONGRES': ['required'],
        'NUMEDITIONCONGRES': ['required'],
        'DTDEBUTCONGRES': ['required'],
        'DTFINCONGRES': ['required'],
        'URLSITEWEBCONGRES': ['required'],
    }
    errors = form_validate(request.form, keys_validation)

    form_data = {
        'TITRECONGRES': request.form.get('TITRECONGRES'),
        'NUMEDITIONCONGRES': request.form.get('NUMEDITIONCONGRES'),
        'DTDEBUTCONGRES': request.form.get('DTDEBUTCONGRES'),
        'DTFINCONGRES': request.form.get('DTFINCONGRES'),
        'URLSITEWEBCONGRES': request.form.get('URLSITEWEBCONGRES'),
    }

    activities_ids = []
    thematiques_ids = []

    if (len(errors) == 0):   

        activities_ids = request.form.getlist('CODESACTIVITES')
        thematiques_ids = request.form.getlist('CODESTHEMATIQUES')

        column_names = fetch_column_names(keys_validation)
        columns = ', '.join(column_names)

        values = []
        values.append("'{}'".format(request.form.get('TITRECONGRES')))
        values.append("'{}'".format(request.form.get('NUMEDITIONCONGRES')))
        values.append("'{}'".format(request.form.get('DTDEBUTCONGRES')))
        values.append("'{}'".format(request.form.get('DTFINCONGRES')))
        values.append("'{}'".format(request.form.get('URLSITEWEBCONGRES')))

        values_str = ', '.join(values)
        query = f"INSERT INTO congres ({columns}) VALUES ({values_str})"

        inserted_id = execute_query(get_connection(), query)

        add_traiter_line(thematiques_ids, inserted_id)
        add_proposer_line(activities_ids, inserted_id)

    form_data['ACTIVITES'] = find_activites(activities_ids)
    form_data['THEMATIQUES'] = find_thematiques(thematiques_ids)

    return render_template('congres/new_success.html', errors=errors, form_data=form_data)

@app.route("/participants")
def participants_list():

    participantsTable = ParticipantsTable(Database.get_instance())

    list_participants = participantsTable.all()

    column_names = []
    if (len(list_participants) > 0):
        column_names = list_participants[0].keys()

    return render_template('participants/list.html', column_names=column_names, list_elements=list_participants)

@app.route("/participants/add")
def participants_add():
    statutsTable = StatutsTable(Database.get_instance())

    list_statuts = statutsTable.all()

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

    is_already_registered = find_participant_by_email(request.form.get('EMAILPART'))
    if (len(is_already_registered) > 0):
        is_valid = False
        errors.append("L'utilisateur ayant pour email {} est déjà inscrit. Veuillez réessayer".format(request.form.get('EMAILPART')))

    if (is_valid):
        
        
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

@app.route("/inscriptions/search")
def inscriptions_search():
    return render_template('inscriptions/search.html')

@app.route("/inscriptions/list", methods=["POST"])
def inscriptions_list():
    email = request.form.get('email')

    query = """
    SELECT c.*
    FROM congres c, inscrire i, participants p
    WHERE c.codCongres = i.codCongres
        AND i.codParticipant = p.codParticipant
        AND p.EMAILPART = '{}'
    """

    connection = get_connection()
    list_congres = execute_read_query(connection, query.format(email))
    
    for congres in list_congres:
        
        query = """
        SELECT t.*
        FROM congres c, choix_thematiques ct, participants p, thematiques t
        WHERE c.codCongres = ct.codCongres
            AND ct.codParticipant = p.codParticipant
            AND t.codeThematique = ct.codeThematique
            AND p.EMAILPART = '{}'
            AND c.codCongres = {}
        """
        query = query.format(email, congres['CODCONGRES'])
        temp_list_thematiques = execute_read_query(connection, query)

        list_thematiques = []
        for thematique in temp_list_thematiques:
            list_thematiques.append(thematique['NOMTHEMATIQUE'])
        congres['THEMATIQUES'] = list_thematiques


    return render_template('inscriptions/list.html', email=email, list_congres=list_congres)

def fetch_column_names(keys_validation: dict) -> list:
    response = []
    for key in keys_validation.keys():
        response.append(key)

    return response

def find_activites(ids: list) -> list:
    query = '''
    SELECT *
    FROM activites
    WHERE codeActivite IN ({ids_str})
    '''

    ids_str = ', '.join(ids)
    result = execute_read_query(get_connection(), query.format(ids_str = ids_str))
    if not result:
        return []
    return result

def find_thematiques(ids) -> list:
    query = '''
    SELECT *
    FROM thematiques
    WHERE codeThematique IN ({ids_str})
    '''

    ids_str = ', '.join(ids)
    result = execute_read_query(get_connection(), query.format(ids_str = ids_str))
    if not result:
        return []
    return result

def add_traiter_line(thematiques_ids: list, congres_id: int):
    query = 'INSERT INTO traiter (codCongres, codeThematique) VALUES '

    temp_sql = []
    for them_id in thematiques_ids:
        temp_sql.append('({}, {})'.format(congres_id, them_id))

    query = query + ', '.join(temp_sql)

    execute_query(get_connection(), query)

def add_proposer_line(activites_ids: list, congres_id: int):
    query = 'INSERT INTO proposer (codCongres, codeActivite) VALUES '

    temp_sql = []
    for act_id in activites_ids:
        temp_sql.append('({}, {})'.format(congres_id, act_id))

    query = query + ', '.join(temp_sql)

    execute_query(get_connection(), query)


def get_connection() -> sqlite3.Connection:
    """Implémentation de la récupération de la BD commune

    Returns:
        sqlite3.Connection: La connection à la BD
    """
    db_path = './db/bd_congres.db'
    connection = create_connection(db_path)

    return connection

def find_participant_by_email(email: str) -> dict|None:
    participantsTable = ParticipantsTable(Database.get_instance())
    
    return participantsTable.find_by_email(email)
    

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
