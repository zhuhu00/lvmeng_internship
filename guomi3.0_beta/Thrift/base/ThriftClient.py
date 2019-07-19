import sys
# sys.path.append("/usr/lib/python2.7/site-packages")
sys.path.append("/opt/aurora/python-lib/WIFI/")
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


class ThriftClient(object):
    def __init__(self, ip, client):
        self.__ip = ip
        self.__client = client

    def __del__(self):
        self.close()

    def create(self):
        self.__transport = TSocket.TSocket(self.__ip.getIp(), self.__ip.getSocket())
        self.__transport = TTransport.TBufferedTransport(self.__transport)
        self.__protocol = TBinaryProtocol.TBinaryProtocol(self.__transport)
        #         self.__protocol = TCompactProtocol.TCompactProtocol(self.__transport)

        self.__transport.open()

        return self.__client.Client(self.__protocol)

    def close(self):  # the destroy is better?
        pass
#         self.__transport.close()
