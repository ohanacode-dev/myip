from flask import Flask, render_template, request, redirect, make_response, url_for
import sqlite3
from contextlib import closing

SERV_NAME = "myip.ohanacode-dev.com"
DB_NAME = "ip_log"

application = Flask(__name__)
# application.config['SERVER_NAME'] = SERV_NAME
# application.config['SESSION_COOKIE_DOMAIN'] = SERV_NAME


def create_db():
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS {} (id TEXT, ip TEXT)".format(DB_NAME))


def set_ip(dev_id, ip_addr):
    result = None

    if ip_addr is not None and dev_id is not None:
        with closing(sqlite3.connect(DB_NAME)) as connection:
            with closing(connection.cursor()) as cursor:
                try:
                    rows = cursor.execute('SELECT ip FROM {} WHERE id = "{}"'.format(DB_NAME, dev_id)).fetchone()

                    if rows is not None and len(rows) > 0:
                        # Already there
                        cursor.execute("UPDATE {} SET ip = ? WHERE id = ?".format(DB_NAME), (ip_addr, dev_id))
                    else:
                        # Insert new
                        query = "INSERT INTO {} VALUES ('{}', '{}')".format(DB_NAME, dev_id, ip_addr)
                        cursor.execute(query)

                    connection.commit()
                    result = 'OK'
                except Exception as e:
                    if str(e).startswith('no such table'):
                        # Create the table
                        create_db()
                        result = "Table created. Try again."
                    else:
                        print(e)

    return result


def get_ip(dev_id):
    result = None

    if dev_id is not None:
        with closing(sqlite3.connect(DB_NAME)) as connection:
            with closing(connection.cursor()) as cursor:
                try:
                    row = cursor.execute('SELECT ip FROM {} WHERE id="{}" '.format(DB_NAME, dev_id)).fetchone()
                    if len(row) > 0:
                        result = row[0]
                except Exception as e:
                    if str(e).startswith('no such table'):
                        # Create the table
                        create_db()
                        result = "Table created. Try again."
                    else:
                        print(e)

    print("RETURN:", result)
    return result


@application.route('/')
def home():
    return render_template('index.html')


@application.route('/set', methods=['GET'])
def set_ip_blank():
    msg = "<h1>ERROR 406</h1> " \
          "<p>This page is not intended to be used like this. You should select a device ID " \
          "(Any random, unique, HTML escaped set of characters and " \
          "add it to the GET request sent from your device like: <br>" \
          "&nbsp &nbsp <b>{}/[your_device_id]</b><br><br>Then to get the devices IP address, go to: <br>" \
          "&nbsp &nbsp <b>{}/get/[your_device_id]</b><br><br></p>" \
          "<h2>NOTE</h2> " \
          "<p>If this service is on an external hosting service, for improved security, it is recommended to use " \
          "https protocol so append <b>'https://'</b> to the url examples above.</p>".format(SERV_NAME, SERV_NAME)
    return msg, 406


@application.route('/set/<id>', methods=['GET'])
def set_ip_dev(id):
    response = make_response(set_ip(id, request.remote_addr), 200)
    response.mimetype = "text/plain"
    return response


@application.route('/get', methods=['GET'])
def get_ip_blank():
    response = make_response(request.remote_addr, 200)
    response.mimetype = "text/plain"
    return response


@application.route('/get/<id>', methods=['GET'])
def get_ip_dev(id):
    result = get_ip(id)

    response = make_response("{}".format(result), 200)
    response.mimetype = "text/plain"
    return response


if __name__ == '__main__':
    # uncomment this if you are hosting the application on an external hosting provider
    # application.run()

    # Use this instead to run on your local computer
    application.run('0.0.0.0', 8888, threaded=True, debug=False)
