#!/usr/bin/python2.7

"""
tcp-client.py

Code sample from https://nostarch.com/blackhatpython
Forked from https://github.com/WillPennell/Python

@author Will Pennel
@author Don Taylor

@updated: March 17, 2019
"""
import socket


def main(target, port, message):
    """
    Simple TCP Client based off of an example in BlackHatPython by Will Pennell

    Uses python's socket library to establish an IPv4 Stream connection to a target host:port.
    The width of the pipe created is 4096 bytes
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target, port))
    client.send(message)
    response = client.recv(4096)
    print response


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Create a simple TCP client socket connection')
    parser.add_argument('-t', '--target', dest='target', help='Target IP address')
    parser.add_argument('-p', '--port', dest='port', type=int, help='Target port number')
    parser.add_argument('-m', '--message', default='GET / HTTP/1.1\r\nHost: www.wright.edu\r\n\r\n')
    args = parser.parse_args()
    main(args.target, args.port, args.message)
