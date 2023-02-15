"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database

class AbstractTable:

    _table_name = None

    def __init__(self, db: Database) -> None:
        self.table_name = self._table_name
        self.db = db

    def all(self):
        """Méthode permettant de récupérer tout le contenu d'une table
        
        Keyword arguments:
        argument -- description
        Return: return_description
        """
        
        query = """
        SELECT *
        FROM {table_name}
        """

        query = query.format(table_name=self.table_name)

        return self.db.execute_read_query(query)

    def find_by_key(self, key: str, values: any, operator: str = '=') -> list:
        """Méthode abstraite permettant de récupérer les 
        lignes de la table correspondant aux critères 
        renseignés
        """
        
        query = """
        SELECT *
        FROM {table_name}
        WHERE {key} {operator} ?
        """
        values = tuple(values)
        query = query.format(table_name=self.table_name, key=key, operator=operator)
 
        return self.db.execute_read_query(query, values)

    def find_by_ids(self, ids: list, key: str):
        """Méthode abstraite permettant de récupérer les 
        lignes de la table correspondant aux critères 
        renseignés
        
        """
        
        
        query = """
        SELECT *
        FROM {table_name}
        WHERE {key} IN ({parametered_list})
        """
        values = tuple(ids)
        parametered_list = ['?' for i in range(len(ids))]
        parametered_list = ','.join(parametered_list)
        query = query.format(table_name=self.table_name, key=key, parametered_list=parametered_list)
 
        return self.db.execute_read_query(query, values)
    
    def insert_line(self, values: list, columns: list):
        """Méthode abstraite permettant d'ajouter 
        une ligne dans la table

        Args:
            values (list): La liste des valeurs
            columns (list): La liste des colonnes

        Returns:
            any: Le retour de l'exécution en base
        """
        query = "INSERT INTO {table_name} ({columns}) VALUES ({values_str})"
        
        values_str = ['?' for i in range(len(columns))]
        query = query.format(
            table_name = self.table_name,
            columns = ','.join(columns),
            values_str = ','.join(values_str)
        )

        return self.db.execute_query(query, tuple(values))
    
    def insert_lines(self, values: list, columns: list):
        """Méthode abstraite permettant d'ajouter 
        plusieurs lignes dans la table

        Args:
            values (list): _description_
            columns (list): _description_

        Returns:
            _type_: _description_
        """
        query = "INSERT INTO {table_name} ({columns}) VALUES ({values_str})"
        
        values_str = ['?' for i in range(len(columns))]
        query = query.format(
            table_name = self.table_name,
            columns = ','.join(columns),
            values_str = ','.join(values_str)
        )

        return self.db.execute_query(query, values)

if (__name__ == '__main__'):
    table = AbstractTable(Database.get_instance())