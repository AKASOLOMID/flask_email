import sqlite3


db_file_name = 'email_flask.db'

def create_db(db_name):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("""create table email(id integer primary key, from_address text, from_name text, subject text, body text, state text, time text);""")
    c.execute("""create table recipient_email (email_id integer, to_address text, to_name text, to_type text, time text);""")
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    create_db(db_file_name)
