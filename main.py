from connection_db import create_connection, execute_query, execute_read_query
from flask import Flask
from flask import render_template

app =  Flask(__name__)
 
@app.route("/index")
@app.route("/")
def index():
  return render_template('index.html')

@app.route("/congres")
def congres_list():

    db_path = './db/bd_congres.db'
    connection = create_connection(db_path)
  
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

  db_path = './db/bd_congres.db'
  connection = create_connection(db_path)

  query = """
  SELECT *
  FROM participants
  """

  list_participants = execute_read_query(connection, query)

  column_names = []
  if (len(list_participants) > 0):
    column_names = list_participants[0].keys()

  return render_template('participants/list.html', column_names=column_names, list_elements=list_participants)

if (__name__ == '__main__'):

    host = '127.0.0.1'
    port = 5000
    debug = True

    app.run(host, port, debug)
  