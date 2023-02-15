"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database
from .AbstractTable import AbstractTable

class ChoixThematiquesTable(AbstractTable):

    _table_name = 'choix_thematiques'

    def insert_lines(self, codParticipant: int, codCongres: int, codeThematiques: list):
        """Surcharge de la méthode parente avec les colonnes préremplies

        Args:
            codParticipant (int): L'identifiant du participant
            codCongres (int): L'identifiant du congres
            codeThematiques (list): La liste des thématiques choisies

        """
        columns = [
            'CODPARTICIPANT',
            'CODCONGRES',
            'CODETHEMATIQUE',
        ]

        values = []
        for codeThematique in codeThematiques:
            values.append((codParticipant, codCongres, codeThematique,))

        return super().insert_lines(values, columns)
