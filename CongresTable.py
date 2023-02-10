"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database
from AbstractTable import AbstractTable

class CongresTable(AbstractTable):

    _table_name = 'congres'

    def find_by_code(self, code: int):
        return super().find_by_key('CODCONGRES', (code,))

    # TODO 1. Afficher la liste des inscriptions de l'utilisateur.
    # TODO 2. Vérifier que l'utilisateur n'est pas déjà inscrit
    # TODO 3. Vérifier que l'utilisateur n'a pas de soucis

    def find_participant_tarif(self, congres_id, participant_id):
        query = """
        SELECT tar.montantTarif
        FROM congres c, tarifs tar, statuts s, participants p
        WHERE p.codeStatut = s.codeStatut
            AND s.codeStatut = tar.codeStatut
            AND tar.codCongres = c.codCongres
            AND p.codParticipant = ?
            AND c.codCongres = ?
        """
        response = self.db.execute_read_query(query, (participant_id, congres_id,))
        print(response)
        return response

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
        
    def insert_line(self, values: list):
        columns = [
            'TITRECONGRES',
            'NUMEDITIONCONGRES',
            'DTDEBUTCONGRES',
            'DTFINCONGRES',
            'URLSITEWEBCONGRES',
        ]

        return super().insert_line(values, columns)