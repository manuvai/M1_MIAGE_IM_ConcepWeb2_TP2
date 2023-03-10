"""
@author: manuvai.Rehua@ut-capitole.fr
"""

from .AbstractTable import AbstractTable

class ThematiquesTable(AbstractTable):
    _table_name = 'thematiques'
    
    def find_by_ids(self, ids: list):
        """Surcharge de la méthode parente avec les noms de colonne spécifiés

        Args:
            ids (list): La liste des valeurs à chercher

        """
        
        return super().find_by_ids(ids, 'codeThematique')

    def find_for_congres(self, congres_id: int):
        """Récupération des thématiques liées à un congres
        
        """
        
        query = """
        SELECT t.*
        FROM congres c, thematiques t, traiter tr
        WHERE c.codCongres = tr.codCongres
            AND tr.codeThematique = t.codeThematique
            AND c.codCongres = ?
        """

        return self.db.execute_read_query(query, (congres_id,))

    def find_by_congres_participants(self, congres_id: int, participant_email: str):
        """Récupération des thématiques auxquel un participant est inscrit
        
        """
        
        query = """
        SELECT t.*
        FROM congres c, choix_thematiques ct, participants p, thematiques t
        WHERE c.codCongres = ct.codCongres
            AND ct.codParticipant = p.codParticipant
            AND t.codeThematique = ct.codeThematique
            AND p.EMAILPART = ?
            AND c.codCongres = ?
        """
        query = query.format()
        temp_list_thematiques = self.db.execute_read_query(query, (participant_email, congres_id,))

        return temp_list_thematiques
