from django.db import connection

def delete_data():
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM comment')
        connection.commit()