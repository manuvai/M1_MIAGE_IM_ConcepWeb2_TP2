"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database
from .AbstractTable import AbstractTable

class ChoixActivitesTable(AbstractTable):

    _table_name = 'choix_activites'

    def insert_lines(self, codParticipant: int, codCongres: int, codeActivites: list):
        """Surcharge de la méthode parente avec les colonnes préremplies

        Args:
            codParticipant (int): L'identifiant du participant
            codCongres (int): L'identifiant du congres
            codeActivites (list): La liste des activités choisies

        """
        columns = [
            'CODPARTICIPANT',
            'CODCONGRES',
            'CODEACTIVITE',
        ]

        values = []
        for codeActivite in codeActivites:
            values.append((codParticipant, codCongres, codeActivite,))

        return super().insert_lines(values, columns)

if __name__ == '__main__':
    table = ChoixActivitesTable(Database.get_instance())
    table.insert_lines(1, 1, [1, 2, 3])
