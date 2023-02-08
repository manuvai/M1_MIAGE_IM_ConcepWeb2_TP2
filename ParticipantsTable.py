"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database
from AbstractTable import AbstractTable

class ParticipantsTable(AbstractTable):

    _table_name = 'participants'

    def find_by_code(self, code: str):
        response = self.find_by_key('CODPARTICIPANT', (code,))

        return response

    def find_by_email(self, value: str):
        response = self.find_by_key('EMAILPART', (value,))

        return response

    def insert_line(self, values: list):
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

