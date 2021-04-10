##################----Manuel d'utilisation Flask--------##################
############ Quelques sites à visiter éventuellement pour se documenter en Flask ##################

https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
https://virtualenv.pypa.io/en/latest/cli_interface.html
https://flask.palletsprojects.com/en/1.1.x/installation/#install-create-env
https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

########## Un forum qui explique bien comment définir un schéma mongodb en python #####

https://stackoverflow.com/questions/61074297/how-to-create-schema-in-mongodb-using-python


################## Les commandes à taper pour la configurations et l'installation de l'environnement Flask ############

1. py -3 -m venv venv
###### installation du Framework Flask ########

1. pip install Flask
2. $ pip install -U https://github.com/pallets/flask/archive/master.tar.gz
########## ---Création de l'environnement Flask ########

    pip install virtualenv
python2 -m virtualenv venv

1. $env:FLASK_APP = "hello.py" #### Ici il faudra remplacer le "hello" par le nom de votre application ###

2. set FLASK_ENV= developement

####### ---Lancement de l'application  Flask sur le navigateur -------######
 
flask run 


