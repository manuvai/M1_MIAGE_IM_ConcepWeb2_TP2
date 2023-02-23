"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Database import Database
from .AbstractTable import AbstractTable

class CongresTable(AbstractTable):

    _table_name = 'congres'

    def find_by_code(self, code: int):
        """Surcharge de la méthode parente avec la colonne spécifiée

        Args:
            code (int): L'identifiant du congres

        """
        return super().find_by_key('CODCONGRES', (code,))

    # TODO 2. Vérifier que l'utilisateur n'a pas de soucis
    # TODO 3. Vérifier le nombre d'inscrits

    def find_participant_tarif(self, congres_id, participant_id):
        """Récupération des tarifs correspondant à un participant pour un congres donné
        
        """
        
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
        return response

    def find_by_participant_email(self, email: str):
        """Récupération d'un congres d'un participant par son email
        
        """
        
        query = """
        SELECT c.*
        FROM congres c, inscrire i, participants p
        WHERE c.codCongres = i.codCongres
            AND i.codParticipant = p.codParticipant
            AND p.EMAILPART = ?
        """

        list_congres = self.db.execute_read_query(query, (email,))

        return list_congres
    
    def find_where_participant_unregistered(self, user_id: int):
        """Récupération des congres que l'utilisateur n'est pas inscrit

        Args:
            user_id (int): L'identifiant d'un utilisateur
        """

        query = """
        SELECT c1.*
        FROM congres c1
        WHERE c1.codCongres NOT IN (
            SELECT c2.codCongres
            FROM congres c2, inscrire i
            WHERE c2.codCongres = i.codCongres
                AND i.codParticipant = ?
        )
        """
        list_congres = self.db.execute_read_query(query, (user_id,))
        return list_congres
        
    def insert_line(self, values: list):
        """Surcharge de la méthode parente avec les colonnes spécifiées

        Args:
            values (list): La liste des valeurs à insérer

        """
        columns = [
            'TITRECONGRES',
            'NUMEDITIONCONGRES',
            'DTDEBUTCONGRES',
            'DTFINCONGRES',
            'URLSITEWEBCONGRES',
        ]

        return super().insert_line(values, columns)