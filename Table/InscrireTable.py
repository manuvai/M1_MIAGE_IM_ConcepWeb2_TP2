"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database
from .AbstractTable import AbstractTable

class InscrireTable(AbstractTable):

    _table_name = 'inscrire'

    def insert_line(self, codParticipant: int, codCongres: int):
        """Surcharge de la méthode parente avec les noms de colonne spécifiés

        Args:
            codParticipant (int): _description_
            codCongres (int): _description_

        Returns:
            _type_: _description_
        """
        columns = [
            'CODPARTICIPANT',
            'CODCONGRES',
        ]
        return super().insert_line((codParticipant, codCongres,), columns)

if (__name__ == '__main__'):
    table = InscrireTable(Database.get_instance())
    table.insert_line(4, 3)
