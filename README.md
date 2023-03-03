# TP2 ConceptionWeb2 - Gestion de congres

## Informations
Lien vers le dépôt Github : https://github.com/manuvai/M1_MIAGE_IM_ConcepWeb2_TP2

Nom : REHUA
Prénom : Manuvai

## Requirements
Avant de lancer l'application web, il faudra disposer de certains modules.
Pour ce faire, vous pouvez installer les dépendances en exécutant :
```bash
pip install -r requirements.txt
```

## Lancement
Pour pouvoir lancer l'application vous devrez exécuter :
```bash
python main.py
```
ou 
```bash
py main.py
```

## Description
Ce dépôt contient les sources pour réaliser le TP2 de Conception Web 2 du deuxième semestre du Master M1 MIAGE IM.

## Architecture choisie
Pour mener à bien se projet, j'ai décidé de séparer la logique des controlleurs et de la gestion de la base de données. C'est pour cela que j'ai choisi de créer un simple fichier `main.py` qui se chargera de gérer essentiellement les requêtes HTTP en faisant appel à des fonctions du module `utils` et des modules `Table.*` pour garantir la gestion de la base de données (Récupération, Modification, Création).
Pour ne pas complexifier la structure actuelle, je n'ai pas adopté le schéma "classique" du MVC. Je me limiterai donc à l'utilisation de "Helpers" pour la gestion de la base de données, de la validation des données entrées via le module `Validator.*` et des templates dans le répertoire `template/`.
