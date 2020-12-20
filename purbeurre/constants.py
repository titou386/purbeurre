"""Constants for 'Purbeurre' application."""
import os

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

MAX_CATEGORIES = 15
MAX_PRODUCTS = 1000
