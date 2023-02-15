"""
@author: manuvai.rehua@ut-capitole.fr
"""

from .AbstractTable import AbstractTable

class TraiterTable(AbstractTable):

    _table_name = 'traiter'
        
    def insert_lines(self, values: list):
        """Surcharge de la méthode parente avec les noms de colonne spécifiés

        Args:
            values (list): La liste des valeurs

        """
        columns = [
            'codCongres',
            'codeThematique',
        ]

        return super().insert_lines(values, columns)