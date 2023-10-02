#  coding: utf-8 
import socketserver, os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        reqInfo = self.data.decode().split()
        #print(reqInfo)
        reqType = reqInfo[0] #should be GET
        #print(reqType)
        reqPath = reqInfo[1]
        #print(reqPath)
        if (reqType != "GET"):
            self.handle405()
            return
        else:
            fullPath = os.path.abspath("www") + reqPath
            if reqPath.find("..") != -1: #if trying to go back, 404
                self.handle404()
                return
            if not os.path.exists(fullPath): #if path doesn't exist, 404
                self.handle404()
                return
            if os.path.isfile(fullPath):
                fileType = reqPath.split(".")[1]
                #print(fileType)
            else:
                fileType = "dir"
            if fileType == "dir":
                if reqPath[-1] == "/":
                    fullPath += "index.html"
                    #print(fullPath)
                    self.html("HTTP/1.1 ", fullPath, "200 OK")
                else:
                    path += "/"
                    sendData = "HTTP/1.1 301 Moved Permanently\r\nLocation:http://127.0.0.1:8080" + reqPath + "\r\n\r\n"
                    self.request.sendall(sendData.encode())
            elif fileType == "html":
                self.html("HTTP/1.1 ", fullPath, "200 OK")
            elif fileType == "css":
                self.css("HTTP/1.1 ", fullPath, "200 OK")
            else:
                print("Unsupported File Type")
            

    def handle405(self): # handle error 405
        self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n\r\n405 Method Not Allowed", "utf-8"))
        return
    
    def handle404(self): # handle error 404
        self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n\r\n404 Method Not Allowed", "utf-8"))
        return
    
    def html(self, header, path, status):
        file = open(path)
        data = file.read()
        sendData = header + status + "\r\nContent-Type: text/html\r\n\r\n" + data
        self.request.sendall(sendData.encode())
    
    def css(self, header, path, status):
        file = open(path)
        data = file.read()
        sendData = header + status + "\r\nContent-Type: text/css\r\n\r\n" + data
        self.request.sendall(sendData.encode())

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
