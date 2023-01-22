from ftplib import FTP
import os
import io
import time
import random
import threading
ftp = FTP(timeout=30)
host = '10.1.38.38'
port = 2121
ftp.connect(host, port)
ftp.login()

client_name = input('Enter client name\n')


def listenForResponses(client_name):

    def display(mesg):
        print(mesg)
    while True:
        files = []
        ftp.dir('./responses', files.append)
        for file in files:
            lst = file.split(' ')
            fname = lst[-1]
            client_ = fname.split('_')[2]
            if client_ == client_name:
                ftp.retrlines('RETR ./responses/'+fname, display)
                ftp.delete('./responses/'+fname)
        time.sleep(1)


#create a thread for listening for responses
thread=threading.Thread(target=listenForResponses,args=(client_name,))
thread.start()

while True:

    command = input('Enter the command\n')
    if command == "quit":
        break
    # now check which server can serve this request
    # iterate through registers.txt file and find out the server that can handle this request

    operation = command.split()[0]

    def display(mesg):
        global lst
        lst.append(mesg)

    lst = []
    ftp.retrlines('RETR register.txt', display)
    #print(lst)
    required_server = None
    for line in lst:
        server_and_command = line.split()
        server = server_and_command[0]
        comm = server_and_command[1:]
        if operation in comm:
            required_server = server

    #print(required_server)

    # now construct the message
    # format is `commmand <server> <client_name_randomNumber>`
    random_number = random.randint(1, 10000)
    request_file_name = 'req_'+required_server + \
        '_'+client_name+'_'+str(random_number)+'.txt'
    request_message = command+' '+required_server+' '+client_name
    # now send/upload the message in the requests folder in
    ftp.storlines('STOR ./requests/'+request_file_name,
                  io.BytesIO(request_message.encode()))
