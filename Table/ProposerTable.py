"""
@author: manuvai.rehua@ut-capitole.fr
"""

from .AbstractTable import AbstractTable

class ProposerTable(AbstractTable):

    _table_name = 'proposer'
        
    def insert_lines(self, values: list):
        """Surcharge de la méthode parente avec les noms de colonne spécifiés

        Args:
            values (list): La liste des valeurs à insérer

        """
        columns = [
            'codCongres',
            'codeActivite',
        ]

        return super().insert_lines(values, columns)