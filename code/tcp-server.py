#!/usr/bin/python2.7

"""
tcp-server.py

Code sample from https://nostarch.com/blackhatpython
Forked from https://github.com/WillPennell/Python

@author Will Pennel
@author Don Taylor

@updated: March 17, 2019
"""
import socket
import multiprocessing


def create_server(target, port):
    """ Helper function to create a listener for the target address:port combination via IPv4 as a stream
    :param target: the ip address to bind the socket
    :param port: the port number to bind the socket
    :return server: python socket instance object
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)
    print "[*] Listening on %s:%d" % (target, port)
    return server


def handle_client(client_socket):
    """ Helper function to accept client connections

    :param client_socket: python object representing client socket instance
    """
    client_socket.send("Connected\r\n")
    request = client_socket.recv(1024)
    print "[*] Received: %s" % request
    client_socket.send("ACK!\r\n")
    client_socket.close()


def main(target, port):
    server = create_server(target, port)
    while True:
        client, addr = server.accept()
        print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])
        # spin up our client process to handle incoming data
        client_handler = multiprocessing.Process(target=handle_client, args=(client,))
        client_handler.start()


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='Create a simple TCP client server connection')
    parser.add_argument('-t', '--target', dest='target', help='Target IP address')
    parser.add_argument('-p', '--port', dest='port', type=int, help='Target port number')
    args = parser.parse_args()
    main(args.target, args.port)
