import datetime
from Database import Database

from Table.CongresTable import CongresTable
from Table.ActivitesTable import ActivitesTable
from Table.ThematiquesTable import ThematiquesTable
from Table.ParticipantsTable import ParticipantsTable
from Table.StatutsTable import StatutsTable
from Table.InscrireTable import InscrireTable
from Table.ChoixActivitesTable import ChoixActivitesTable
from Table.ChoixThematiquesTable import ChoixThematiquesTable

from Validator.CongresAddValidator import CongresAddValidator
from Validator.ParticipantAddValidator import ParticipantAddValidator
from Validator.ConnectionValidator import ConnectionValidator
from Validator.ParticipantUpdateValidator import ParticipantUpdateValidator

from utils import *
from flask import Flask, request, session, redirect, url_for
from flask import render_template

app = Flask(__name__)

@app.route("/index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def index():

    user = None
    errors = []
    list_congres = []
    user_congres = []

    table = ParticipantsTable(Database.get_instance())
    if (request.method == 'POST'):
        v = ConnectionValidator(request.form, table)
        errors = v.validate()
        if (len(errors) <= 0):
            user = table.find_by_email(request.form.get('email'))[0]
            session['user_id'] = user['CODPARTICIPANT']
            return redirect(url_for('index'))

    elif (auth()):
        user = table.find_by_code(session.get('user_id'))[0]
        table = CongresTable(Database.get_instance())

        user_id = int(user.get('CODPARTICIPANT'))
        
        user_congres = table.find_by_participant_email(user.get('EMAILPART'))
        
        list_congres = table.find_where_participant_unregistered(user_id)
    
    return render_template('home/index.html', \
        errors=errors, user=user, \
        list_congres=list_congres, \
        user_congres=user_congres)

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('user_id')
    return redirect(url_for('index'))

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

    v = CongresAddValidator(request.form)
    errors = v.validate()

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

        values = []
        values.append(request.form.get('TITRECONGRES'))
        values.append(request.form.get('NUMEDITIONCONGRES'))
        values.append(request.form.get('DTDEBUTCONGRES'))
        values.append(request.form.get('DTFINCONGRES'))
        values.append(request.form.get('URLSITEWEBCONGRES'))

        congresTable = CongresTable(Database.get_instance())
        inserted_id = congresTable.insert_line(values)

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
    participant = dict()
    statutsTable = StatutsTable(Database.get_instance())

    list_statuts = statutsTable.all()

    form_url = url_for("participants_new")
    return render_template('participants/add.html', participant=participant, form_url=form_url, list_statuts=list_statuts)
 
@app.route("/participants/new", methods=["POST"])
def participants_new():
    v = ParticipantAddValidator(request.form)

    errors = v.validate()

    is_valid = len(errors) == 0

    is_already_registered = find_participant_by_email(request.form.get('EMAILPART'))
    if (len(is_already_registered) > 0):
        is_valid = False
        errors.append("L'utilisateur ayant pour email {} est déjà inscrit. Veuillez réessayer".format(request.form.get('EMAILPART')))

    if (is_valid):
        
        x = datetime.datetime.now()
        now_date = x.strftime("%Y-%m-%d")

        values = []
        values.append(request.form.get('CODESTATUT'))
        values.append(request.form.get('NOMPART'))
        values.append(request.form.get('PRENOMPART'))
        values.append(request.form.get('ORGANISMEPART'))
        values.append(request.form.get('CPPART'))
        values.append(request.form.get('ADRPART'))
        values.append(request.form.get('VILLEPART'))
        values.append(request.form.get('PAYSPART'))
        values.append(request.form.get('EMAILPART'))
        values.append(now_date)

        participantsTable = ParticipantsTable(Database.get_instance())

        participantsTable.insert_line(values)

    return render_template('participants/new.html', errors=errors, is_valid=is_valid)

@app.route("/login", methods=['GET', 'POST'])
def login():
    user = None
    errors = []

    table = ParticipantsTable(Database.get_instance())
    if (request.method == 'POST'):
        v = ConnectionValidator(request.form, table)
        errors = v.validate()
        if (len(errors) <= 0):
            user = table.find_by_email(request.form.get('email'))[0]
            session['user_id'] = user['CODPARTICIPANT']
            return redirect(url_for('index'))

    return render_template('login/signin.html', errors=errors)

@app.route("/register", methods=['GET', 'POST'])
def register():
    errors = []
    participant = dict()
    if (request.method == 'POST'):
        v = ParticipantAddValidator(request.form)

        errors = v.validate()

        is_valid = len(errors) == 0

        is_already_registered = find_participant_by_email(request.form.get('EMAILPART'))
        if (len(is_already_registered) > 0):
            is_valid = False
            errors.append("L'utilisateur ayant pour email {} est déjà inscrit. Veuillez réessayer".format(request.form.get('EMAILPART')))

        if (is_valid):
            
            x = datetime.datetime.now()
            now_date = x.strftime("%Y-%m-%d")

            values = []
            values.append(request.form.get('CODESTATUT'))
            values.append(request.form.get('NOMPART'))
            values.append(request.form.get('PRENOMPART'))
            values.append(request.form.get('ORGANISMEPART'))
            values.append(request.form.get('CPPART'))
            values.append(request.form.get('ADRPART'))
            values.append(request.form.get('VILLEPART'))
            values.append(request.form.get('PAYSPART'))
            values.append(request.form.get('EMAILPART'))
            values.append(now_date)

            participantsTable = ParticipantsTable(Database.get_instance())

            participantsTable.insert_line(values)

            return redirect(url_for('login'))

    statutsTable = StatutsTable(Database.get_instance())

    list_statuts = statutsTable.all()

    form_url = url_for("register")
    return render_template('login/register.html', participant=participant, form_url=form_url, list_statuts=list_statuts, errors=errors)
   
@app.route('/manage_account', methods=['GET', 'POST'])
def manage_account():
    if (not auth()):
        return redirect(url_for('login'))
    
    errors = []
    participantsTable = ParticipantsTable(Database.get_instance())
    participant = participantsTable.find_by_code(session.get('user_id'))[0]

    if (request.method == 'POST'):
        v = ParticipantUpdateValidator(request.form)

        errors = v.validate()

        is_valid = len(errors) == 0

        if (is_valid):
            values = []
            values.append(request.form.get('CODESTATUT'))
            values.append(request.form.get('NOMPART'))
            values.append(request.form.get('PRENOMPART'))
            values.append(request.form.get('ORGANISMEPART'))
            values.append(request.form.get('CPPART'))
            values.append(request.form.get('ADRPART'))
            values.append(request.form.get('VILLEPART'))
            values.append(request.form.get('PAYSPART'))
            values.append(request.form.get('EMAILPART'))

            participantsTable.update(participant.get('CODPARTICIPANT'), values)

            return redirect(url_for('manage_account'))


    statutsTable = StatutsTable(Database.get_instance())

    list_statuts = statutsTable.all()

    return render_template('account/edit.html', \
        participant=participant, \
        list_statuts=list_statuts, \
        errors=errors)

@app.route("/inscriptions/search")
def inscriptions_search():
    return render_template('inscriptions/search.html')

@app.route("/inscriptions/list", methods=["POST"])
def inscriptions_list():
    email = request.form.get('email')

    congresTable = CongresTable(Database.get_instance())

    list_congres = congresTable.find_by_participant_email(email)
    
    for congres in list_congres:
        thematiquesTable = ThematiquesTable(Database.get_instance())
        temp_list_thematiques = thematiquesTable.find_by_congres_participants(int(congres['CODCONGRES']), email)

        list_thematiques = []
        for thematique in temp_list_thematiques:
            list_thematiques.append(thematique['NOMTHEMATIQUE'])
        congres['THEMATIQUES'] = list_thematiques


    return render_template('inscriptions/list.html', email=email, list_congres=list_congres)

@app.route("/inscriptions/add/<congres_id>")
def inscriptions_add(congres_id):
    db = Database.get_instance()

    if (not auth()):
        return redirect(url_for('login'))

    thematiquesTable = ThematiquesTable(db)
    activitesTable = ActivitesTable(db)
    congresTable = CongresTable(db)

    list_thematiques = thematiquesTable.find_for_congres(congres_id)
    list_activites = activitesTable.find_for_congres(congres_id)
    congres = congresTable.find_by_code(congres_id)[0]
    
    return render_template('inscriptions/add.html', congres=congres, list_thematiques=list_thematiques, list_activites=list_activites)

@app.route("/inscriptions/confirm", methods=['POST'])
def inscriptions_confirm():
    db = Database.get_instance()
    
    if (not auth()):
        return redirect(url_for('login'))

    congresTable = CongresTable(db)
    
    thematiques_ids = request.form.getlist('CODESTHEMATIQUES')
    activities_ids = request.form.getlist('CODESACTIVITES')

    congres_id = request.form.get('CODCONGRES')
    user_id = session.get('user_id')

    list_activites = find_activites(activities_ids)
    list_thematiques = find_thematiques(thematiques_ids)
    congres = congresTable.find_by_code(congres_id)[0]
    tarif = congresTable.find_participant_tarif(congres_id, user_id)[0].get('MONTANTTARIF')

    total = float(tarif)

    for activite in list_activites:
        total += float(activite['PRIXACTIVITE'])

    return render_template('inscriptions/confirm.html', total=total, congres=congres, tarif=tarif, list_thematiques=list_thematiques, list_activites=list_activites)

@app.route("/inscriptions/new", methods=['POST'])
def inscriptions_new():
    thematiques_ids = request.form.getlist('CODESTHEMATIQUES[]')
    activities_ids = request.form.getlist('CODESACTIVITES[]')
    congres_id = request.form.get('CODCONGRES')

    user_id = session.get('user_id')

    inscrireTable = InscrireTable(Database.get_instance())
    choixActivitesTable = ChoixActivitesTable(Database.get_instance())
    choixThematiquesTable = ChoixThematiquesTable(Database.get_instance())

    inscrireTable.insert_line(user_id, congres_id)
    choixActivitesTable.insert_lines(user_id, congres_id, activities_ids)
    choixThematiquesTable.insert_lines(user_id, congres_id, thematiques_ids)

    return redirect(url_for('index', add_success = 1))

if (__name__ == '__main__'):

    host = '127.0.0.1'
    port = 5000
    debug = True

    app.secret_key = __name__

    app.run(host, port, debug)
