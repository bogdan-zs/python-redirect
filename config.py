import os 

DATABASE_URL = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost/postgres'