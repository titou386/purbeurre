# Pur Beurre
An application for the company Pure beurre

## Requirements
- Linux, MacOS
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
