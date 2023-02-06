"""
@author: manuvai.rehua@ut-capitole.fr
"""

from AbstractTable import AbstractTable

class ProposerTable(AbstractTable):

    _table_name = 'proposer'
        
    def insert_lines(self, values: list):
        columns = [
            'codCongres',
            'codeActivite',
        ]

        return super().insert_lines(values, columns)