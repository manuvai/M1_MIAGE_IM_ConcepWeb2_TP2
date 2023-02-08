"""
@author: manuvai.rehua@ut-capitole.fr
"""

from AbstractValidator import AbstractValidator
from Database import Database
from ParticipantsTable import ParticipantsTable

class ConnectionValidator(AbstractValidator):

    def __init__(self, data: any, table: ParticipantsTable):
        validators = {
            'email': ['required', 'email']
        }
        super().__init__(data, validators)

        self.table = table

    def validate(self):
        errors = super().validate()

        if (len(errors) <= 0):
            res = self.table.find_by_email(self.data.get('email'))

            if (len(res) <= 0):
                errors.append('Cet utilisateur n\'existe pas.')

        return errors
    
if (__name__ == '__main__'):
    table = ParticipantsTable(Database.get_instance())
    v = ConnectionValidator({
        'email': 'kameni@ut1c.fr', 
    }, table)

    print(v.validate())
