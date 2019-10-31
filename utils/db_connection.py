import aiomysql
import yaml
from pathlib import Path


async def dbconnection():
    NAMEFILE = Path('config.yaml')

    with open(NAMEFILE, encoding='utf8') as f:
        data = yaml.safe_load(f)

    db_connection = await aiomysql.connect(
        host=data['database']['host'],
        user=data['database']['user'],
        password=data['database']['passwd'],
        db=data['database']['database']
    )

    return db_connection
