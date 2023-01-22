import sys
import os
import io
import random
from ftplib import FTP
import time
import threading


def connectToFtpServer(server):

    ftp = FTP(timeout=30)
    host = '10.1.38.38'
    port = 2121
    ftp.set_pasv(False)
    ftp.connect(host, port)
    ftp.login()
    ftp.storlines('APPE register.txt', io.BytesIO(server.encode()))

    def handle_request(fname, send_to):
        #print(f'fname is {fname}\n')
        #print("inside handle request\n")
        l = server.split()
        supported_commands = server.split(' ')[1:]
        supported_commands = [x[:3] for x in supported_commands]
        print(supported_commands)

        def add(mesg):
            #print("inside add\n")
            command = mesg.split()[0]
            operands = mesg.split()[1:3]
            #print(command.split())
            val = int(operands[0])+int(operands[1])
            response_mesg = "the query "+command+' response is '+str(val)
            # now send the response
            random_val = random.randint(1, 100000)
            response_file = 'resp_'+l[0]+'_'+send_to+'_'+str(random_val)+'.txt'
            ftp.storlines('STOR ./responses/'+response_file,
                          io.BytesIO(response_mesg.encode()))

        def sub(mesg):
            #print("inside sub\n")
            command = mesg.split()[0]
            operands = mesg.split()[1:3]
            val = int(operands[0])-int(operands[1])
            response_mesg = "the query "+command+' response is '+str(val)
            # now send the response
            random_val = random.randint(1, 100000)
            response_file = 'resp_'+l[0]+'_'+send_to+'_'+str(random_val)+'.txt'
            ftp.storlines('STOR ./responses/'+response_file,
                          io.BytesIO(response_mesg.encode()))

        def mul(mesg):
            #print("inside mul\n")
            command = mesg.split()[0]
            operands = mesg.split()[1:3]
            val = int(operands[0])*int(operands[1])
            response_mesg = "the query "+command+' response is '+str(val)
            # now send the response
            random_val = random.randint(1, 100000)
            response_file = 'resp_'+l[0]+'_'+send_to+'_'+str(random_val)+'.txt'
            ftp.storlines('STOR ./responses/'+response_file,
                          io.BytesIO(response_mesg.encode()))
        if "add" in supported_commands:
            #print("inside ...add")
            ftp.retrlines('RETR ./requests/'+fname, add)
        elif "sub" in supported_commands:
            ftp.retrlines('RETR ./requests/'+fname, sub)
        elif "mul" in supported_commands:
            ftp.retrlines('RETR ./requests/'+fname, mul)
        ftp.delete('./requests/'+fname)
    while True:
        # keep listening in the requests folder
        # and whenever you get a request from the client...create a thread and delete the file from the requests folder
        # create a thread for each request from the client
        # after processing the request send the response to the responses folder
        # the client will keep listening to the responses folder
        # whenever the desired response is there in the responses folder...the client will print it and delete that response from the folder
        files = []
        ftp.dir('./requests', files.append)
        for file in files:
            # now create a thread for each file
            #print("creating thread\n")
            lst = file.split(' ')
            fname = lst[-1]
            file_split = fname.split('_')
            server_split = server.split(' ')
            send_to = file_split[2]
            if (file_split[1] == server_split[0]):
                # now create a thread for the file
                thr = threading.Thread(
                    target=handle_request, args=(fname, send_to,))
                thr.start()

        time.sleep(2)


def main():
    st = input("Enter the server and the functions of the server\n")
    st += '\n'
    t1 = threading.Thread(target=connectToFtpServer, args=(st,))
    t1.start()


if __name__ == '__main__':
    main()
