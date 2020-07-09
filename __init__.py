from .HttpAPI import *
__version__ = "1.0"

class CwtestLibrary(HttpTest):
    '''
        Library to be used test Http  API
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        self.test = ""

    def opens_requst(self):
        self.test = HttpTest()
        return self.test.openrequst()

    def sets_ip(self, ip):
        return self.test.setip(ip)

    def sets_port(self, port):
        return self.test.setport(port)

    def sets_header(self, k, v):
        return self.test.setheader(k, v)

    def gets_requst(self):
        return self.test.getrequst()

    def posts_requst(self):
        return self.test.postrequst()

    def getimage(self, ):
        pass