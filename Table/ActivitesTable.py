"""
@author: manuvai.Rehua@ut-capitole.fr
"""

from .AbstractTable import AbstractTable

class ActivitesTable(AbstractTable):
    _table_name = 'activites'

    def find_by_ids(self, ids: list):
        """Surcharge de la méthode parente avec la clé spécifique

        Args:
            ids (list): La liste des identifiants

        """
        return super().find_by_ids(ids, 'codeActivite')

    def find_for_congres(self, congres_id):
        """Récupération des activités liées 
        à un congres en particulier
        
        """
        
        query = """
        SELECT a.*
        FROM congres c, proposer p, activites a
        WHERE c.codCongres = p.codCongres
            AND p.codeActivite = a.codeActivite
            AND c.codCongres = ?
        """

        return self.db.execute_read_query(query, (congres_id,))

