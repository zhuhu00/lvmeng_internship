import sys

sys.path.append("/opt/aurora/python-lib/WIFI/")
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class ThriftServer:
    def __init__(self, handler, ipAddress, type):
        self.__handler = handler
        self.__ipAddress = ipAddress
        self.__type = type
        self.__transport = None
        self.__server = None
        self.__tfactory = None

    def __del__(self):
        self.stop()

    def createServer(self):
        print('Creating the server...')
        #         self.__ipAddress.dump()
        print(self.__type)
        print(self.__handler)
        processor = self.__type.Processor(self.__handler)
        self.__transport = TSocket.TServerSocket(self.__ipAddress.getIp(), self.__ipAddress.getSocket())
        self.__tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        #         pfactory = TCompactProtocol.TCompactProtocolFactory()
        # the TSimpleServer is not very good, need to be writed in complex situation, which one the the cooprater uses?
        self.__server = TServer.TSimpleServer(processor, self.__transport, self.__tfactory, pfactory)
        print('done.')

    def start(self):
        print('Starting the server...')
        self.__server.serve()
        print('done.')

    def getHandler(self):
        return self.__handler

    def stop(self):
        print('Stopping the server...')
        #         self.__transport.close()
        print("the second stop")
        #         self.__tfactory.
        print('done.')
