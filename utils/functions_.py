from utils.db_connection import dbconnection


def is_empty(structure):
    if structure:
        # structure is not empty return false
        return False
    else:
        # structure is empty return true
        return True


async def has_job(job, user_id):
    db_connection = await dbconnection()
    cursor = await db_connection.cursor()
    sql = "SELECT job FROM jobs WHERE current_job = %s AND character_id = '%s' AND job = %s"
    val = ('true', user_id, job)
    await cursor.execute(sql, val)
    result = await cursor.fetchall()
    await cursor.close()
    db_connection.close()
    if is_empty(result):
        return False
    else:
        return True
