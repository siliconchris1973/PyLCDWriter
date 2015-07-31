__author__ = '@siliconchris'

from flask import Flask
from flask import json
from flask import request
from flask import render_template
import sys

app = Flask(__name__)

class rest_writer:
    @app.route('/')
    def api_root():
        return render_template('info.html')

    @app.route('/messageform')
    def api_form():
        return render_template('messageform.html')

    @app.route('/write', methods = ['POST'])
    def api_message():
        if request.headers['Content-Type'] == 'text/plain':
            writetext = request.data
            return "Text Message: " + request.data
        elif request.headers['Content-Type'] == 'application/json':
            try:
                data = json.loads(json.dumps(request.json))
                row1 = data['row1']
                row2 = data['row2']
                if app.debug:
                    print 'row1: ' + row1
                    print 'row2: ' + row2

                writetext = row1 + '\\n' + row2
            except:
                if app.debug:
                    print "Error parsing the json:", sys.exc_info()[0]
                else:
                    print "Error parsing the json"

            return "JSON Message: " + json.dumps(request.json)
        elif request.form['text']:
            try:
                row1 = request.form['row1']
                row2 = request.form['row2']
                if app.debug:
                    print 'row1: ' + row1
                    print 'row2: ' + row2

                writetext = row1 + '\\n' + row2
            except:
                if app.debug:
                    print "Error parsing the json:", sys.exc_info()[0]
                else:
                    print "Error parsing the json"

            return "Form Message: " + request.data
        else:
            return "415 Unsupported Media Type ;)"

        if app.debug:
            print(writetext)
        # now write received text to the LCD
        lcd.message(writetext)
