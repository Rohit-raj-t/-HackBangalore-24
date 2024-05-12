import pymysql


def execute_query(query):
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="hackbangalore",
        host="hackbangalore-24-rohitrajt2005-754e.l.aivencloud.com",
        password="AVNS_2DaRXKukpFlFS8aSqUY",
        read_timeout=timeout,
        port=16602,
        user="avnadmin",
        write_timeout=timeout,
    )
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result
