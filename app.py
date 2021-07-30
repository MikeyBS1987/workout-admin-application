import os
import MySQLdb

from flask import Flask, render_template, json, request

import database.db_connector as db

# create database connection
db_connection = db.connect_to_database()

# Configuration
app = Flask(__name__)

# Routes
@app.route('/muscle-groups', methods=['GET', 'POST'])
def muscle_groups():
    if request.method == 'GET':
        query = "SELECT * FROM muscle_groups"
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query
        )
        results = json.dumps(cursor.fetchall())
        return results
    
    if request.method == 'POST':
        muscle_group_name = request.form.get('muscle_group_name')
        query = '''
            INSERT INTO
                MUSCLE_GROUPS(muscle_group_name)
            VALUES
                (%s)
        '''
        args = (muscle_group_name,)  # Enforce the tuple with comma
        
        try:
            cursor = db.execute_query(
                db_connection=db_connection,
                query=query,
                query_params=args
            )
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print(e)
            return 'Insert unsuccessfull!'
        return 'Insert successfull!'

@app.route('/muscle-groups', methods=['PUT'])
def update_muscle_groups():
    muscle_group_name = request.form.get('muscle_group_name')
    muscle_group_id = request.form.get('muscle_group_id')
    query = '''
        UPDATE
            MUSCLE_GROUPS
        SET
            muscle_group_name = %s
        WHERE
            muscle_group_id = %s
    '''
    # TO DO - get id from form using form.get
    args = (muscle_group_name, muscle_group_id)

    try:
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=args
        )
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return 'Update unsuccessfull!'
    return 'Update successfull!'

@app.route('/muscle-groups', methods=['DELETE'])
def delete_muscle_groups():
    muscle_group_id = request.form.get('muscle_group_id')
    query = '''
        DELETE FROM
            MUSCLE_GROUPS
        WHERE
            muscle_group_id = %s 
    '''
    args = (muscle_group_id,)
    try:
        cursor = db.execute_query(
            db_connection=db_connection,
            query=query,
            query_params=args
        )
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return 'Delete unsuccessfull!'
    return 'Delete successfull!'


# Listener
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)
