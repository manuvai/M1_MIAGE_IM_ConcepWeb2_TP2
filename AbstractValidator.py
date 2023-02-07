"""
@author: manuvai.rehua@ut-capitole.fr
"""
import re

class AbstractValidator:

    _stop_on_first_error = False

    def __init__(self, data: any, validators: dict):
        self.data = data
        self.validators = validators

    def validateRequired(self, key: str, value: any):
        if (value is None):
            return f"Le champs {key} n'est pas présent dans le formulaire, veuillez renseigner une donnée"
        elif (value == ''):
            return f"Le champs {key} est vide, veuillez renseigner une valeur"

    def validateEmail(self, key: str, value: any):
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        est_email = re.match(pat, value)
        if (not est_email):
            return f"Le champs {key} doit être un email valide (ex : nom.prenom@example.com). Veuillez réessayer"

    def validate(self):
        errors = []
        for key, values in self.validators.items():
            for val in values:
                if (val == 'required'):
                    validation = self.validateRequired(key, self.data.get(key, None))
                    if (validation):
                        errors.append(validation)
                elif ((val == 'email') and (not (self.data.get(key, None) is None))):
                    validation = self.validateEmail(key, self.data.get(key, None))
                    if (validation):
                        errors.append(validation)
                    
                if (self._stop_on_first_error and len(errors) > 0):
                    return errors
        
        return errors
