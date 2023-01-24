import sqlite3
import os

def create_connection(chemin_vers_BD: str) -> sqlite3.Connection:
  """Implémentation de la récupération des données

  Args:
      chemin_vers_BD (str): Chemin vers la DB

  Returns:
      sqlite3.Connection: La connection créée
  """
  connection = None

  if not os.path.exists(chemin_vers_BD):
      print(f"Le fichier {chemin_vers_BD} n'existe pas")
  else:         
      try:
        connection = sqlite3.connect(chemin_vers_BD)

      except sqlite3.Error as e:
        print(f"The error {e} occured")

  return connection

def execute_read_query(connection: sqlite3.Connection, query: str) -> list:
  """Implémentation de la récupération de données à partir d'une requête

  Args:
      connection (sqlite3.Connection): La connection à la DB
      query (str): La requête

  Returns:
      list: La liste de retour
  """
  data = None

  try:
    cursor = connection.cursor()
    exec_data = cursor.execute(query)

    data = []

    column_names = []
    for column in exec_data.description:
      column_names.append(column[0])

    temp_data = cursor.fetchall()
    for row in temp_data:
      query_data = {}
      i = 0
      for column_value in row:
        column_name = column_names[i]
        query_data[column_name] = column_value

        i += 1
      data.append(query_data)

  except sqlite3.Error as e:
    print(f"The error {e} occured")

  return data

def execute_query(connection: sqlite3.Connection, query: str) -> list:
  """Implémentation de la récupération de données à partir d'une requête

  Args:
      connection (sqlite3.Connection): La connection à la DB
      query (str): La requête

  Returns:
      list: La liste de retour
  """

  try:
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()

  except sqlite3.Error as e:
    print(f"The error {e} occured")
