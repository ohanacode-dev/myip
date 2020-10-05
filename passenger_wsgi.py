from flask import Flask, render_template, request, redirect, make_response, url_for
import sqlite3
from contextlib import closing
from time import time

SERV_NAME = "myip.ohanacode-dev.com"
DB_NAME = "ip_log"
SPAM_PROTECTION_TIMEOUT = 10

application = Flask(__name__)
# application.config['SERVER_NAME'] = SERV_NAME
# application.config['SESSION_COOKIE_DOMAIN'] = SERV_NAME


def create_db():
    with closing(sqlite3.connect(DB_NAME)) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS {} (id TEXT, ip TEXT, time INT)".format(DB_NAME))


def set_ip(dev_id, ip_addr):
    result = 'None'

    if ip_addr is not None and dev_id is not None:
        with closing(sqlite3.connect(DB_NAME)) as connection:
            with closing(connection.cursor()) as cursor:
                try:
                    id_row = cursor.execute('SELECT * FROM {} WHERE id = "{}"'.format(DB_NAME, dev_id)).fetchone()
                    ip_row = cursor.execute('SELECT * FROM {} WHERE ip = "{}"'.format(DB_NAME, ip_addr)).fetchone()
                    timestamp = int(time())

                    if ip_row is not None and len(ip_row) > 0:
                        # We already have records from this IP
                        ip_timestamp = ip_row[2]
                        timeout = SPAM_PROTECTION_TIMEOUT - (timestamp - ip_timestamp)

                        if timeout < 0:
                            # Only allow updating every 10 seconds or more.
                            # Delete all records with this IP
                            cursor.execute("DELETE FROM {} WHERE ip = ?".format(DB_NAME), (ip_addr,))
                            # Delete all records with this device ID
                            cursor.execute("DELETE FROM {} WHERE id = ?".format(DB_NAME), (dev_id,))

                            # Insert new data
                            query = "INSERT INTO {} VALUES ('{}', '{}', {})".format(DB_NAME, dev_id, ip_addr, timestamp)
                            cursor.execute(query)
                            connection.commit()
                            result = 'OK'
                        else:
                            result = 'ERROR: Spam protection. Please wait {}s'.format(timeout)
                    else:
                        # Insert new data
                        query = "INSERT INTO {} VALUES ('{}', '{}', {})".format(DB_NAME, dev_id, ip_addr, timestamp)
                        cursor.execute(query)
                        connection.commit()
                        result = 'OK'

                except Exception as e:
                    if str(e).startswith('no such table'):
                        # Create the table
                        create_db()
                        result = "Initial database created. Try again."
                    else:
                        print(e)

                # Cleanup old data
                old_timestamp = time() - (60 * 60 * 48)
                cursor.execute("DELETE FROM {} WHERE time < ?".format(DB_NAME), (old_timestamp,))
                connection.commit()
    return result


def get_ip(dev_id):
    result = None

    if dev_id is not None:
        with closing(sqlite3.connect(DB_NAME)) as connection:
            with closing(connection.cursor()) as cursor:
                try:
                    row = cursor.execute('SELECT ip FROM {} WHERE id = ?'.format(DB_NAME), (dev_id,)).fetchone()
                    if row is not None and len(row) > 0:
                        result = row[0]

                except Exception as e:
                    if str(e).startswith('no such table'):
                        # Create the table
                        create_db()
                        result = "Initial database created. Try again."
                    else:
                        print(e)

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


@application.route('/redirect_http/<id>', methods=['GET'])
def redirect_http(id):
    result = get_ip(id)

    if result is not None and len(result) < 17:
        # Result is not a database created message, but an actual IP address. Show a redirect page.
        dev_url = 'http://{}'.format(result)
        return render_template('redirect.html', dev_ip=result, dev_url=dev_url)
    else:
        response = make_response("{}".format(result), 200)
        response.mimetype = "text/plain"
        return response


@application.route('/redirect_https/<id>', methods=['GET'])
def redirect_https(id):
    result = get_ip(id)

    if result is not None and len(result) < 17:
        # Result is not a database created message, but an actual IP address. Show a redirect page.
        dev_url = 'https://{}'.format(result)
        return render_template('redirect.html', dev_ip=result, dev_url=dev_url)
    else:
        response = make_response("{}".format(result), 200)
        response.mimetype = "text/plain"
        return response


if __name__ == '__main__':
    # uncomment this if you are hosting the application on an external hosting provider
    # application.run()

    # Use this instead to run on your local computer
    application.run('0.0.0.0', 8888, threaded=True, debug=False)
