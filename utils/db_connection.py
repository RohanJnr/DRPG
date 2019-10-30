import mysql.connector
import yaml
from pathlib import Path


def dbconnection():
    NAMEFILE = Path('config.yaml')

    with open(NAMEFILE, encoding='utf8') as f:
        data = yaml.safe_load(f)

    db_connection = mysql.connector.connect(
        host=data['database']['host'],
        user=data['database']['user'],
        passwd=data['database']['passwd'],
        database=data['database']['database']
    )

    return db_connection
