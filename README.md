# Pur Beurre
An application for the company Pure beurre   
"Pure Beurre" aims to find a better (at least an equivalent) substitute for the product you are looking for.    

You will be able to :   
* Search a product by name
* Search a product by category
* Watch/save a product detail and a proposed substitute
* delete/watch in your saved subtitutes

## Requirements
- Linux, MacOS, Windows
- Python 3
- Mysql server

## Installation
Download the repository:

    $ git clone https://github.com/titou386/purbeurre.git
    $ pip install -r requirements.txt

## Mysql server configuration

    $ mysql -u root -p --default-character-set=utf8

In mysql prompt :
Create your database and your credentials:

    $ mysql> CREATE DATABASE your_database;
    $ mysql> CREATE USER 'your_user'@'%' IDENTIFIED BY 'your_user_pass';
    $ mysql> GRANT ALL PRIVILEGES ON your_database.* TO 'your_user'@'%';

## Mysql client configuration
You can modify directly DB_* variables in constant.py or
configure by configuring your environment by this command.

    $ export DB_USER='your_user' DB_PASSWORD='your_user_pass' DB_HOST='your_server' DB_NAME='your_database'

## Import
Before using the application for the first time, you must import data from
openfoodfacts.com into mysql database.
( You can change the number of imported products in contants.py )

    $ python3 import.py

## Usage

Execute main.py in purbeurre folder:

    $ python3 main.py
### All screens of the application
#### Homepage
When you start the application and the application was able to establish a connection with mysql,  
you have this page and you can back at this page at any moment in the application.

    # Page d'accueil

    Bienvenue

    Choisissez une option :

    1 - Rechercher un produit par nom
    2 - Rechercher une catégorie
    3 - Afficher mes substituts sauvegardés
    q - Quitter


    Choix? 
#### Product search
    # Page de recherche de produits

    h! - Page d'accueil
    q! - Quitter


    Produit? 
#### Product search by category
    # Page de recherche de categories

    h! - Page d'accueil
    q! - Quitter


    Catégorie?
#### Saved substitutions

    # Page des subtituts sauvegardés

    Aucun substitut sauvegardé pour l'instant.

    h - Page d'accueil   q - Quitter
    option? 

#### Detailed product and substitute
    # Page de détail du produit :

    Nom du produit :   Coca cola
    Description :      
    Quantité :         1,25L
    Magasin de vente : Magasins U, Auchan
    Pays de vente :    France, Suisse

    Pour 100g/ml
    Energie :          42.00
    Matières grasses : 0.00g
       dont saturées : 0.00
    Glucides :         10.60g
         dont sucres : 10.60g
    Fibres :           
    Protéines :        0.00g
    Sel :              0.00g

    Nutriscore :       e
    Nova :             4
    URL de la fiche :  https://fr.openfoodfacts.org/produit/5000112611748


    # Produit de substitution

    Nom du produit :   Original
    Description :      Boisson rafraîchissante aux extraits végétaux
    Quantité :         1,25 L
    Magasin de vente : 
    Pays de vente :    France, Belgium, Spain, Germany, United Kingdom

    Pour 100g/ml
    Energie :          42.00
    Matières grasses : 0.00g
       dont saturées : 0.00
    Glucides :         10.60g
         dont sucres : 10.60g
    Fibres :           
    Protéines :        0.00g
    Sel :              0.00g

    Nutriscore :       e
    Nova :             4
    URL de la fiche :  https://fr.openfoodfacts.org/produit/5449000267412



    h - Page d'accueil   r - retour   q - Quitter
    s - Saugarder le produit de substitution
    Choix? 
