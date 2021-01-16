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
#### Product search results ( ex: coca )
    # Page de résultat des produits :

      0- Coca-Cola Classic             18- coca cola light taste                   
      1- Coca-Cola Zero 330 ml         19- Coca Cola Zero Zucker                   
      2- Coca-Cola Goût Original       20- Coca Cola 450 ml                        
      3- Coca-Cola 1 l                 21- Coca-Cola 2 L                           
      4- Coca-Cola zero® sans sucres   22- Coca Cola zéro sans caféine             
      5- Coca-cola 330 ml              23- Coca-cola light 1 l                     
      6- Coca Zéro                     24- Coca-Cola Cherry 330 ml                 
      7- Coca Cola zéro 330 ml         25- Coca-Cola Saveur Framboise Zéro Sucres  
      8- Coca Cola® zéro sucres        26- Coca Cola 2 l                           
      9- Coca-Cola 2 L                 27- Coca-Cola cherry 33 cl                  
     10- Coca-Cola 50 cl               28- Coca Cola Cherry 500 ml                 
     11- Coca-Cola Zero 50 cl          29- Coca-Cola 0,25 l                        
     12- Coca-Cola Light 330 ml        30- Coca-Cola 330 ml                        
     13- Coca-Cola 50 cl e             31- Coca cola cherry 1.25L                  
     14- Coca-Cola Zero 2 l            32- Coca cola light                         
     15- Coca cola 1,25L               33- Coca-Cola Energy                        
     16- coca cola 25cl                34- Coca Cola zéro 33 cl                    
     17- Coca-cola Zéro Sans caféine   35- Coca-Cola Lemon sans sucres             
 
    h - Page d'accueil   r - retour   q - Quitter
    Choix? 
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
