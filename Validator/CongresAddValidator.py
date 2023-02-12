"""
@author: manuvai.rehua@ut-capitole.fr
"""

from .AbstractValidator import AbstractValidator

class CongresAddValidator(AbstractValidator):
    def __init__(self, data: any):
        validators = {
            'TITRECONGRES': ['required'],
            'NUMEDITIONCONGRES': ['required'],
            'DTDEBUTCONGRES': ['required'],
            'DTFINCONGRES': ['required'],
            'URLSITEWEBCONGRES': ['required'],
        }
        super().__init__(data, validators)


if __name__ == '__main__':

    form_data = {
        'TITRECONGRES': 'TITRECONGRES',
        'NUMEDITIONCONGRES': 'NUMEDITIONCONGRES',
        'DTDEBUTCONGRES': 'DTDEBUTCONGRES',
        'DTFINCONGRES': 'DTFINCONGRES',
        'URLSITEWEBCONGRES': 'URLSITEWEBCONGRES',
    }

    v = CongresAddValidator(form_data)
    print(v.validate())
