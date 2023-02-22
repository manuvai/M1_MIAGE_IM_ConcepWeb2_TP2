"""
@author: manuvai.rehua@ut-capitole.fr
"""

from .AbstractValidator import AbstractValidator

class ParticipantUpdateValidator(AbstractValidator):
    
    def __init__(self, data: any):
        validators = {
            'CODESTATUT': ['required'], 
            'NOMPART': ['required'], 
            'PRENOMPART': ['required'], 
            'ORGANISMEPART': ['required'], 
            'CPPART': ['required'], 
            'ADRPART': ['required'], 
            'VILLEPART': ['required'], 
            'PAYSPART': ['required'], 
            'EMAILPART': ['required', 'email'], 
        }

        super().__init__(data, validators)
