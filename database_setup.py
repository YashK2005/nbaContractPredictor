import sqlite3
from sqlite3 import Error
from api_fetch import getStats, getSalary, get_per

database = "sqlite.db"

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return (conn)

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_salaries(conn, project):
    """
    Create a new salary into the salary table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO salaries(player_id, first_name, last_name, height, weight, experience, birth_date, salary)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def create_stats(conn, task):
    """
    Create a new stat table entry
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO stats(player_id, games_played, minutes, fg, fga, three_pt, three_pta, ft, fta, pts, reb, ass, stl, blk, turn, pf, tspct, usg)
              VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def join_tables(conn):
    sql = '''   CREATE TABLE combined_table AS 
                SELECT * FROM salaries
                INNER JOIN stats ON salaries.player_id = stats.player_id;      
    '''
    cur = conn.cursor()
    cur.execute(sql)

def per_update(conn):
    data = get_per()
    sql = ''' UPDATE combined_table 
    SET per = ?
    WHERE player_id = ?
    '''
    cur = conn.cursor()
    
    for stat in data:
        cur.execute(sql, stat)
        conn.commit()
        print(stat)

def data_plot_fetcher():
    sql = 'SELECT * FROM combined_table;'
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(row)
    return data

def data_by_name(name):
    print(name)
    sql = '''SELECT * FROM combined_table
             WHERE first_name LIKE ? COLLATE NOCASE OR last_name LIKE ? COLLATE NOCASE OR first_name || ' ' || last_name LIKE ? COLLATE NOCASE OR last_name || ' ' || first_name LIKE ? COLLATE NOCASE
             ORDER BY salary DESC'''
    print("hello")
    conn = create_connection(database)
    cur = conn.cursor()
    print("hi")
    cur.execute(sql, [name + '%', name + '%', name + '%', name + '%'])
    print("hey")
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(row)
    print(data[0])
    return data[0]

def autocomplete_fetcher(query):
    sql = '''SELECT first_name || ' ' || last_name AS full_name FROM combined_table
             WHERE first_name LIKE ? COLLATE NOCASE OR last_name LIKE ? COLLATE NOCASE OR full_name LIKE ? COLLATE NOCASE OR last_name || ' ' || first_name LIKE ? COLLATE NOCASE
             ORDER BY salary DESC'''
    conn = create_connection(database)
    print(query)
    cur = conn.cursor()
    cur.execute(sql, [query + '%', query + '%', query + '%', query + '%'])
    rows = cur.fetchall()
    data = [row[0] for row in rows]  # Extracting only the full name from each row
    return data

def main():
    

    # sql_create_player_table = """ CREATE TABLE IF NOT EXISTS salaries (
    #                                     player_id integer PRIMARY KEY,
    #                                     first_name text NOT NULL,
    #                                     last_name text NOT NULL,
    #                                     height integer NOT NULL,
    #                                     weight integer NOT NULL,
    #                                     experience integer NOT NULL,
    #                                     birth_date text NOT NULL,
    #                                     salary integer NOT NULL
    #                                 ); """

    # sql_create_stats_table = """CREATE TABLE IF NOT EXISTS stats (
    #                                 player_id integer PRIMARY KEY,
    #                                 games_played integer NOT NULL,
    #                                 minutes integer NOT NULL,
    #                                 fg numeric NOT NULL,
    #                                 fga numeric NOT NULL,
    #                                 three_pt numeric NOT NULL,
    #                                 three_pta numeric NOT NULL,
    #                                 ft numeric NOT NULL,
    #                                 fta numeric NOT NULL,
    #                                 pts numeric NOT NULL,
    #                                 reb numeric NOT NULL,
    #                                 ass numeric NOT NULL,
    #                                 stl numeric NOT NULL,
    #                                 blk numeric NOT NULL,
    #                                 turn numeric NOT NULL,
    #                                 pf numeric NOT NULL,
    #                                 tspct numeric NOT NULL,
    #                                 usg numeric NOT NULL
    #                             );"""
    #salaries = getSalary()
    #stats = getStats()

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        
        # create player table
        #create_table(conn, sql_create_player_table)
    
        # create stats table
        #create_table(conn, sql_create_stats_table)

        #fetch and insert salaries
        # for salary in salaries:
        #     create_salaries(conn, salary)
        # for stat in stats:
        #     create_stats(conn, stat)
        #join_tables(conn)
        #per_update(conn)
        pass
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()