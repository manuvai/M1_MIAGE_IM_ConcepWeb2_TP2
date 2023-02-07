"""
@author: manuvai.rehua@ut-capitole.fr
"""
import re

class AbstractValidator:

    _stop_on_first_error = False

    def __init__(self, data: any, validators: dict):
        self.data = data
        self.validators = validators

    def validate(self):
        errors = []
        for key, values in self.validators.items():
            for val in values:
                if ((val == 'required') and (self.data.get(key, None) is None)):
                    errors.append("Le champ {} est requis, veuillez le renseigner".format(key))
                elif ((val == 'email') and (not self.data.get(key, None) is None)):
                    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    est_email = re.match(pat, self.data.get(key))
                    if (not est_email):
                        errors.append(f"Le champs {key} doit être un email valide (ex : nom.prenom@example.com). Veuillez réessayer")
                if (self._stop_on_first_error and len(errors) > 0):
                    return errors
        
        return errors
