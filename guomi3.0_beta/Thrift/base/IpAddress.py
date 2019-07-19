import sys
import socket

class IpAddress(object):
    def __init__(self, ip = "127.0.0.1", socket = 8080):
        self.__ip = ip
        self.__socket = socket
        self.dump()

    def dump(self):
        print("the ip is " + str(self.__ip) + " the socket is " + str(self.__socket))
        
    def updateIp(self,ip):
        self.__ip = ip
    
    def updateSocket(self, socket):
        self.__socket = socket
        return self
    
    def update(self, ip, socket):
        updateIp(ip)
        updateSocket(socket)
        
    def getIp(self):
        return self.__ip
    
    def getSocket(self):
        return self.__socket
    