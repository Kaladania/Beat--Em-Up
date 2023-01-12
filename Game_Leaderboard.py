import sqlite3  # python module for database

conn = sqlite3.connect('highscores.db')  # connects the program to said database

cursor = conn.cursor()  # allows SQL to be implimented

#import pandas as pd


#opens and reads the leaderbaord database (stored as an external sql file)
#Database = open('highscores.db', 'r')
#sqlFile = Database.read()
#Database.close()
    
# This will skip and report errors
# For example, if the tables do not yet exist, this will skip over the DROP TABLE commands

def clean_data(record):  # records are normally added as tuples: ('Emily',), removes the excess characters to make sure added data is due the desired values

    record = record.replace("(", "")
    record = record.replace(",", "")
    record = record.replace("'", "")
    record = record.replace(")", "")

    return record


def create_leaderboard(database_solo_names, database_solo_avatars, database_solo_scores):

    for row in cursor.execute('SELECT Name FROM HIGHSCORES_SOLO ORDER BY score DESC'):

        record = clean_data(str(row))

        if record not in database_solo_names:  # prevents duplicates from forming due to the looping (due to being primary key)
            database_solo_names.append(record)


    for row in cursor.execute('SELECT Avatar FROM HIGHSCORES_SOLO ORDER BY score DESC'):

        record = clean_data(str(row))

        database_solo_avatars.append(record)


    for row in cursor.execute('SELECT Score FROM HIGHSCORES_SOLO ORDER BY score DESC'):

        record = clean_data(str(row))

        if int(record) < 10:  # makes sure everything is double digits
            record = '0' + record

        database_solo_scores.append(record)

    return database_solo_names, database_solo_avatars, database_solo_scores


def get_names(database_solo_names):

    for row in cursor.execute('SELECT Name FROM HIGHSCORES_SOLO ORDER BY score DESC'):

        record = clean_data(str(row))

        if record not in database_solo_names:  # prevents duplicates from forming due to the looping (due to being primary key)
            database_solo_names.append(record)

    return database_solo_names


def enter_leaderboard(new_name, new_avatar, new_score):

    cursor.execute('''INSERT INTO HIGHSCORES_SOLO (Name, Avatar, Score) VALUES ('%s', '%s', %s)''' % (new_name.title(), new_avatar, new_score))

    conn.commit()



#
#except OperationalError:

#def create_leaderboard():
#    database_solo_names = []
#    database_solo_avatars = []
#    database_solo_scores = []
#    database_solo_rankings = []

#    i = 1

#    try:
#        for row in c.execute('SELECT Name FROM HIGHSCORES_SOLO ORDER BY score'):
#            database_solo_rankings.append(i)

#            i += 1

#        for row in c.execute('SELECT Name FROM HIGHSCORES_SOLO ORDER BY score'):
#            database_solo_names.append(row)

#        for row in c.execute('SELECT Avatar FROM HIGHSCORES_SOLO ORDER BY score'):
#            database_solo_avatars.append(row)

#        for row in c.execute('SELECT Score FROM HIGHSCORES_SOLO ORDER BY score'):
#            database_solo_scores.append(row)

        
#        df = pd.DataFrame({'NAme': database_solo_names,
#                           'Class':  ['B','A','C'],
#                            'Score' : [75,92,56]})
##
##except OperationalError:
#    print("Error: ", command)
