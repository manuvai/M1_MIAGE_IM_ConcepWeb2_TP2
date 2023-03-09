"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database
from .AbstractTable import AbstractTable

class ParticipantsTable(AbstractTable):

    _table_name = 'participants'

    def find_by_code(self, code: str):
        """Récupération d'un participant par son identifiant

        Args:
            code (str): L'identifiant d'un participant

        """

        response = self.find_by_key('CODPARTICIPANT', (code,))

        return response

    def find_by_email(self, value: str):
        """Récupération d'un participant par son email

        Args:
            value (str): L'email d'un participant

        """
        response = self.find_by_key('EMAILPART', (value,))

        return response
    
    def update(self, code: str, values: list):
        """_summary_

        Args:
            code (str): _description_
            values (list): _description_
        """
        
        columns = [
            'CODESTATUT',
            'NOMPART',
            'PRENOMPART',
            'ORGANISMEPART',
            'CPPART',
            'ADRPART',
            'VILLEPART',
            'PAYSPART',
            'EMAILPART',
        ]

        return super().update(code, 'CODPARTICIPANT', values, columns)

    def insert_participant(self, values: list, is_prepared: bool):
        if (is_prepared):
            return self.insert_line(values)
        
        columns = [
            'CODESTATUT',
            'NOMPART',
            'PRENOMPART',
            'ORGANISMEPART',
            'CPPART',
            'ADRPART',
            'VILLEPART',
            'PAYSPART',
            'EMAILPART',
            'DTINSCRIPTION',
        ]
        values_str = ", ".join(values)

        columns_str = ", ".join(columns)

        query = """
            INSERT INTO {table_name} ({columns_str}) VALUES 
                ({values_str})
        """
        query = query.format(
            table_name=self.table_name, 
            columns_str=columns_str, 
            values_str=values_str
        )

        return self.db.execute_query(query)

    def insert_line(self, values: list):
        """Surcharge de la méthode parente avec les noms de colonne spécifiés

        Args:
            values (list): La liste des valeurs à insérer

        """
        columns = [
            'CODESTATUT',
            'NOMPART',
            'PRENOMPART',
            'ORGANISMEPART',
            'CPPART',
            'ADRPART',
            'VILLEPART',
            'PAYSPART',
            'EMAILPART',
            'DTINSCRIPTION',
        ]

        return super().insert_line(values, columns)

