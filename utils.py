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

    activitesTable = ActivitesTable(Database.get_instance())

    result = activitesTable.find_by_ids(ids)
    if not result:
        return []
    return result

def find_thematiques(ids) -> list:
    thematiquesTable = ThematiquesTable(Database.get_instance())

    result = thematiquesTable.find_by_ids(ids)
    if not result:
        return []
    return result

def add_traiter_line(thematiques_ids: list, congres_id: int):
    
    values = []
    for thematique_id in thematiques_ids:
        values.append([congres_id, thematique_id])

    traiterTable = TraiterTable(Database.get_instance())
    traiterTable.insert_lines(values)

def auth() -> bool:
    user_id = session.get('user_id')
    is_auth = not user_id is None

    if (is_auth):
        
        table = ParticipantsTable(Database.get_instance())
        participant = table.find_by_code(user_id)

        is_auth = is_auth and len(participant) > 0

    return is_auth

def add_proposer_line(activites_ids: list, congres_id: int):
   
    values = []
    for activite_id in activites_ids:
        values.append([congres_id, activite_id])

    proposerTable = ProposerTable(Database.get_instance())
    proposerTable.insert_lines(values)

def find_participant_by_email(email: str) -> dict|None:
    participantsTable = ParticipantsTable(Database.get_instance())
    
    return participantsTable.find_by_email(email)

