"""
@author: manuvai.rehua@ut-capitole.fr
"""

from .AbstractTable import AbstractTable

class TraiterTable(AbstractTable):

    _table_name = 'traiter'
        
    def insert_lines(self, values: list):
        columns = [
            'codCongres',
            'codeThematique',
        ]

        return super().insert_lines(values, columns)