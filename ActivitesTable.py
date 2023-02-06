"""
@author: manuvai.Rehua@ut-capitole.fr
"""

from AbstractTable import AbstractTable

class ActivitesTable(AbstractTable):
    _table_name = 'activites'

    def find_by_ids(self, ids: list):
        
        return super().find_by_ids(ids, 'codeActivite')