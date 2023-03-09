"""
@author: manuvai.rehua@ut-capitole.fr
"""

from Table.ActivitesTable import ActivitesTable
from Database import Database
from Table.ThematiquesTable import ThematiquesTable
from Table.TraiterTable import TraiterTable
from Table.ParticipantsTable import ParticipantsTable
from Table.ProposerTable import ProposerTable
from flask import session

def find_activites(ids: list) -> list:
    """Récupère des activités à partir d'une liste passée en paramètre

    Args:
        ids (list): La liste des IDs

    Returns:
        list: La liste des activités trouvées
    """
    activitesTable = ActivitesTable(Database.get_instance())

    result = activitesTable.find_by_ids(ids)
    if not result:
        return []
    return result

def find_thematiques(ids) -> list:
    """Récupère des thématiques à partir d'une liste passée en paramètre

    Args:
        ids (list): La liste des IDs

    Returns:
        list: La liste des thématiques trouvées
    """
    thematiquesTable = ThematiquesTable(Database.get_instance())

    result = thematiquesTable.find_by_ids(ids)
    if not result:
        return []
    return result

def add_traiter_line(thematiques_ids: list, congres_id: int):
    """Ajout des thématiques liées à un congres

    Args:
        thematiques_ids (list): La liste des IDs des thématiques
        congres_id (int): L'IDS du congres
    """
    values = []
    for thematique_id in thematiques_ids:
        values.append([congres_id, thematique_id])

    traiterTable = TraiterTable(Database.get_instance())
    traiterTable.insert_lines(values)

def auth() -> bool:
    """Détermine si l'utilisateur est connecté

    Returns:
        bool: Bool
    """
    user_id = session.get('user_id')
    is_auth = not user_id is None

    if (is_auth):
        
        table = ParticipantsTable(Database.get_instance())
        participant = table.find_by_code(user_id)

        is_auth = is_auth and len(participant) > 0

    return is_auth

def add_proposer_line(activites_ids: list, congres_id: int):
    """Ajout des activités liées à un congres

    Args:
        thematiques_ids (list): La liste des IDs des activités
        congres_id (int): L'IDS du congres
    """
   
    values = []
    for activite_id in activites_ids:
        values.append([congres_id, activite_id])

    proposerTable = ProposerTable(Database.get_instance())
    proposerTable.insert_lines(values)

def find_participant_by_email(email: str) -> any:
    participantsTable = ParticipantsTable(Database.get_instance())
    
    return participantsTable.find_by_email(email)

