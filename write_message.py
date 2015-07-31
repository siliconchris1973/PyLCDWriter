#!/usr/bin/env python

__author__ = '@siliconchris'

import RPi.GPIO as GPIO
from time import sleep, time
import argparse
import sys


class HD44780:
    def __init__(self, pin_rs=4, pin_e=17, pins_db=[18, 22, 23, 24]):
        """ Initialise GPIO """
        self.pin_rs=pin_rs
        self.pin_e=pin_e
        self.pins_db=pins_db

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)
        GPIO.setup(self.pin_rs, GPIO.OUT)

        for pin in self.pins_db:
            GPIO.setup(pin, GPIO.OUT)

        self.clear()

    def clear(self):
        """ Blank / Reset LCD """
        self.cmd(0x33) # $33 8-bit mode
        self.cmd(0x32) # $32 8-bit mode
        self.cmd(0x28) # $28 8-bit mode
        self.cmd(0x0C) # $0C 8-bit mode
        self.cmd(0x06) # $06 8-bit mode
        self.cmd(0x01) # $01 8-bit mode

    def cmd(self, bits, char_mode=False):
        """ Send command to LCD """
        sleep(0.001)
        bits=bin(bits)[2:].zfill(8)

        GPIO.output(self.pin_rs, char_mode)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

        for pin in self.pins_db:
            GPIO.output(pin, False)

        for i in range(4,8):
            if bits[i] == "1":
                GPIO.output(self.pins_db[::-1][i-4], True)

        GPIO.output(self.pin_e, True)
        GPIO.output(self.pin_e, False)

    def message(self, text):
        """ Send string to LCD. Newline wraps to second line"""
        for char in text:
            if char == '\n':
                self.cmd(0xC0) # next line
            else:
                self.cmd(ord(char),True)


if __name__ == '__main__':
    lcd = HD44780()

    parser = argparse.ArgumentParser(description='Write a message on a 16x2 LCD')
    parser.add_argument('-t', '--text', action="store", dest="text",
                        help='The text to display - max 16 characters. Use \\n to separate two lines')

    parser.add_argument('-d', '--demonize', action='store_true', dest="demonize", default=False,
                        help='Run in server mode. Starts a RESTful API at port 3033 (or whatever port given with --port) and waits for the text to display to be passed on the endpoint /write/')
    parser.add_argument('-s', '--servermode', action='store_true', dest="demonize", default=False,
                        help='Same as -d')

    parser.add_argument('-i', '--interface', action="store", dest="interface",
                        help='If run in server mode, you can provide a specific ip-address here. Standard is to listen on ALL interfaces')
    parser.add_argument('-p', '--port', action="store", dest="port",
                        help='The port to bind to for the REST API.')

    args = parser.parse_args()

    assert isinstance(args, object)

    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(-1)

    if args.text:
        writetext = args.text
    else:
        writetext = "Raspberry Pi\n  Take a byte!"

    lcd.message(writetext)
    GPIO.cleanup()