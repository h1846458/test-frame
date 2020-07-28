from .HttpAPI import *
from .comm.comms import getTimeStamp
from .comm.comms import setimageData
from .comm.comms import getVerificationcode
from .comm.comms import getCaptchaKey
import ast
import json
from .comm.comms import addstr
__version__ = "1.0"

class CwtestLibrary(HttpTest):
    '''
        Library to be used test Http  API
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        self.test = ""


    def get_base64image(self, ):
        return setimageData()[1]

    def set_timestamp(self):
        return getTimeStamp()

    def get_Verificationcode(self, ip, url):
        return getVerificationcode(ip, url)

    def get_CaptchaKey(self):
        return getCaptchaKey()

    def create_dict(self):
        return {}

    def add_json(self, key, value, d={}):
        print(key)
        d[key] = value
        return json.dumps(d)

    def add_string(self, v1, v2, strs=""):
        if (v1 == "Basic"):
            tmp = strs + v1 + " " + v2
            return tmp
        else:
            tmp = strs + str(v1) + str(v2)
            return tmp

    def to_dict(self, strs):
        if(strs[0] == "{" and strs[-1] == "}"):
            str_dict = ast.literal_eval(strs)
            return str_dict
        else:
            print("传入的字符串不符合字典格式")


    def collect_json(self, key, text):
        try:
            json_object = json.loads(text)
            for k in json_object.keys():
                if(k == key):
                    return json_object[k]
                else:
                    if(type(json_object[k]) == type({})):
                        for ks in json_object[k].keys():
                            if (ks == key):
                                return json_object[k][ks]

        except TypeError as e:
            return False

    def collect_dict(self, key, text):
        if(type(text) == type({})):
            return text[key]
        else:
            print("传入数据不是字典")
