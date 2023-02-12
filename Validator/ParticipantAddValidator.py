"""
@author: manuvai.rehua@ut-capitole.fr
"""

from .AbstractValidator import AbstractValidator

class ParticipantAddValidator(AbstractValidator):
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


if __name__ == '__main__':

    form_data = {
        'CODESTATUT': 'required', 
        'NOMPART': 'required', 
        'PRENOMPART': 'required', 
        'ORGANISMEPART': 'required', 
        'CPPART': 'required', 
        'ADRPART': 'required', 
        'VILLEPART': 'required', 
        'PAYSPART': 'required', 
        'EMAILPART': 'mail.mail@mail.com', 
    }

    v = ParticipantAddValidator(form_data)
    print(v.validate())
