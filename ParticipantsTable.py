"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database
from AbstractTable import AbstractTable

class ParticipantsTable(AbstractTable):

    _table_name = 'participants'

    def find_by_email(self, value: str):
        response = self.find_by_key('EMAILPART', value)

        return response

