"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database
from AbstractTable import AbstractTable

class CongresTable(AbstractTable):

    _table_name = 'congres'

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