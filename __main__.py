__author__ = '@siliconchris'

from flask import Flask
import argparse
import sys

from hd44780_class import HD44780
from rest_writer_class import rest_writer


app = Flask(__name__)

if __name__ == '__main__':
    lcd = HD44780()
    app.debug = True

    inetaddr = '0.0.0.0'
    inetport = 5000
    security_enable = False
    security_token = ''
    security_token_key = ''

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
        rest_writer.run(inetaddr, inetport)
    except:
        if app.debug:
            print "Unexpected error:", sys.exc_info()[0]
        else:
            print "Unexpected error"
        raise
