"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database
from AbstractTable import AbstractTable

class CongresTable(AbstractTable):

    _table_name = 'congres'

    def find_by_code(self, code: int):
        return super().find_by_key('CODCONGRES', (code,))

    def find_by_participant_email(self, email: str):
        
        query = """
        SELECT c.*
        FROM congres c, inscrire i, participants p
        WHERE c.codCongres = i.codCongres
            AND i.codParticipant = p.codParticipant
            AND p.EMAILPART = ?
        """

        list_congres = self.db.execute_read_query(query, (email,))

        return list_congres
        
    def insert_line(self, values: list):
        columns = [
            'TITRECONGRES',
            'NUMEDITIONCONGRES',
            'DTDEBUTCONGRES',
            'DTFINCONGRES',
            'URLSITEWEBCONGRES',
        ]

        return super().insert_line(values, columns)