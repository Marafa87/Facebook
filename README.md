# Facebook
Projet Mongo Réseaux sociaux

Afin de pouvoir utiliser l’application, voici la procédure d’installation sous Windows: 

Cloner le repository Github:  

git clone Procédure d’installation de l’application Flask 

Aller dans le répertoire de l’API:  

Cd  Facebook\app_social_networks\ 

Activer la variable d’environnement: 

. Venv/bin/activate 

Installer les dépendances: 

Pip install -r ./flask-api/requirements.txt 

 

Désactiver la variable d’environnement: 

venv\Scripts\deactivate . 

Installer la bdd neo4J 

Créer une base de données neo4J, avec comme utilisateur neo4J et admin, lancer la base de données et exécuter le script script.cypher (joint à ce dossier) 

Lancer Flask: 

cd ./ flask-api 

Flask run 

 

L’API est dès lors disponible à l’url suivante: 

http://127.0.0.1:5000/ 

Pour d’autre OS que Windows, se référer à la documentation Flask pour l’activation des environnements: 

https://docs.ovh.com/fr/web-power/python-installer-flask/ 

