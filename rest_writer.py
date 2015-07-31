__author__ = '@siliconchris'


from flask import json
from flask import request
from flask import Flask
from flask import render_template

import argparse
import sys


app = Flask(__name__)

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
    #lcd.message(writetext)


if __name__ == '__main__':
    app.debug = True

    inetaddr = '0.0.0.0'
    inetport = 5000
    security_enable = False
    security_token = ''
    security_token_key = ''
    row1 = ''
    row2 = ''
    txtmessage = ''

    parser = argparse.ArgumentParser(description='Write a message on a 16x2 LCD. The service waits for the text to display to be passed at the endpoint /write/')
    parser.add_argument('-f', '--foreground', action='store_true', dest="demonize", default=False,
                        help='Run in foreground. Start the RESTful API at port 5000 (or whatever port given with --port) but don\'t detach from the console.')
    parser.add_argument('-i', '--interface', action="store", dest="interface",
                        help='You can provide a specific ip-address here (standard is 0.0.0.0 causing the service to listen on ALL interfaces)')
    parser.add_argument('-p', '--port', type=int, action="store", dest="port",
                        help='The port to bind to - please be aware, that the program must be started as root, if port is below 1024 on most *nix like OS')
    parser.add_argument('-a', '--authentication', action="store_true", dest="sec_enable", default=False,
                        help='Enable authentication with token and token-key. Token and Key must be provided with their respective arguments.')
    parser.add_argument('-s', '--security-token', action="store", dest="sec_token",
                        help='The security token')
    parser.add_argument('-k', '--security-token-key', action="store", dest="sec_token_key",
                        help='The security token key')

    args = parser.parse_args()

    assert isinstance(args, object)
    # check command lin arguments
    if args.interface:
        inetaddr = args.interface
    if args.port:
        inetport = args.port
    if args.sec_token:
        security_token = args.sec_token
    if args.sec_token_key:
        security_token_key = args.sec_token_key
    if args.sec_enable:
        security_enable = args.sec_enable

    try:
        app.run(inetaddr, inetport)
    except:
        if app.debug:
            print "Unexpected error:", sys.exc_info()[0]
        else:
            print "Unexpected error"
        raise
