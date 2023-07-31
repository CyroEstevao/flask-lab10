from flask import Flask, redirect, url_for
import psycopg2
import os

app = Flask(__name__)
app.debug = True

# db_connection_url = "postgresql://cyro_render_db_user:SawRA23f0nyv6IMuJfs6PNa7zrrwRtqH@dpg-cj2t8hd9aq0e0q4tci40-a.oregon-postgres.render.com/cyro_render_db"

# db_connection_url = "postgres://cyro_render_db_user:SawRA23f0nyv6IMuJfs6PNa7zrrwRtqH@dpg-cj2t8hd9aq0e0q4tci40-a/cyro_render_db"

db_connection_url: "postgres://cyro_render_db_user:SawRA23f0nyv6IMuJfs6PNa7zrrwRtqH@dpg-cj2t8hd9aq0e0q4tci40-a.oregon-postgres.render.com/cyro_render_db"

@app.route('/')
def hello_world():
    return 'Hello Folks!'

#test conn
@app.route('/db_test')
def testing():
    conn = psycopg2.connect(db_connection_url)
    print("Connection URL:", db_connection_url)

    conn.close()
    return "Database Connection Successful"


#create table
@app.route('/db_create')
def creating():
    conn = psycopg2.connect(db_connection_url)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Basketball (
        First varchar(255),
        Last varchar(255),
        City varchar(255),
        Name varchar(255),
        Number int
        );
        ''')
    conn.commit()
    conn.close()
    return "Table created successfully!"


#populate table
@app.route('/db_insert')
def inserting():
    conn = psycopg2.connect(db_connection_url)    
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO Basketball (First, Last, City, Name, Number)
        Values
        ('Jayson', 'Tatum', 'Boston', 'Celtics', 0),
        ('Stephen', 'Curry', 'San Francisco', 'Warriors', 30),
        ('Nikola', 'Jokic', 'Denver', 'Nuggets', 15),
        ('Kawhi', 'Leonard', 'Los Angeles', 'Clippers', 2);
        ''')
    conn.commit()
    conn.close()
    return "Table correctly filled!"

#Select items
@app.route('/db_select')
def selecting():
    conn = psycopg2.connect(db_connection_url)
    cur = conn.cursor()
    cur.execute('''
        SELECT * FROM Basketball;
        ''')
    table_val = cur.fetchall()
    conn.close()
    res=""
    res +="<table>"
    
    for player in table_val:
        res +="<tr>"
        
        for info in player:
            res +="<td>{}</td>".format(info)
        res+="</tr>"
    res+="</table>"
    return res


#drop table
@app.route('/db_drop')
def dropping():
    conn = psycopg2.connect(db_connection_url)
    cur = conn.cursor()
    cur.execute('''
        DROP TABLE Basketball;
        ''')
    conn.commit()
    conn.close()
    return "Table Successfully dropped!"


def create_app():
    app_obj = Flask(__name__)
    app_obj.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")



    # Register the main blueprint
    app_obj.register_blueprint(app.main)

    # Call the create_table() function to create the database table
    app.creating()
    
    return app_obj


if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server using port 3308 instead of port 5000.
    # app.run(host='0.0.0.0', port=3308)
    app.run(host='0.0.0.0', port=10000)

    # app.run()
    
