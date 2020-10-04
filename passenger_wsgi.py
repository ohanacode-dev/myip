from flask import Flask, render_template
 
application = Flask(__name__)
# application.config['SERVER_NAME'] = "myip.ohanacode-dev.com"
application.config['SESSION_COOKIE_DOMAIN'] = "myip.ohanacode-dev.com"


@application.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    # application.run()
    application.run('0.0.0.0', 8888, threaded=True, debug=False)
