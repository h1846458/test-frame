from .HttpAPI import *
from .comm.comms import getTimeStamp
from .comm.comms import getimageData
from .comm.comms import getVerificationcode, getfacedetect
import ast
import json
import robot.utils.dotdict

__version__ = "1.0"

class CwtestLibrary(HttpTest):
    '''
        Library to be used test Http  API
    '''

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        self.test = ""


    def get_base64image(self, pth, fl = ''):
        return getimageData(pth, fl)[1]

    def get_timestamp(self):
        return getTimeStamp()

    def get_Verificationcode(self, ip, url):
        return getVerificationcode(ip, url)

    def get_facedetect(self, imagepath):
        return getfacedetect(imagepath)

    def add_json(self, **kwargs):
        if(type(kwargs) == type({})):
            return json.dumps(kwargs)
        else:
            print("传入的数据格式不对")


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
        key = str(key)
        if(type(text) == str):
            json_object = json.loads(text)
            for k in json_object.keys():
                if(k == key):
                    return json_object[k]
                else:
                    if(type(json_object[k]) == type({})):
                        for ks in json_object[k].keys():
                            if (ks == key):
                                return json_object[k][ks]
        elif(type(text) == dict or type(text) == robot.utils.dotdict.DotDict):
            for k in text.keys():
                if (k == key):
                    return text[k]
                else:
                    if (type(text[k]) == type({})):
                        for ks in text[k].keys():
                            if (ks == key):
                                return text[k][ks]

    def collect_dict(self, key, text):
        if(type(text) == type({})):
            return text[key]
        else:
            print("传入数据不是字典")

    def replace_str(self, restr, rp, *args):
        lsstr = restr.split(rp)
        tmp = ''
        for s in range(len(args)):
            tmp += lsstr[s] + rp + str(args[s])
        return tmp

    def create_lis(self, *value):
        ls = []
        for k in value:
            ls.append(k)
        return ls

    def insert_lis(self, lis, v):
        lis.append(v)

    def edit_json(self, dicts, **kwargs):
        for k in kwargs.keys():
            dicts[k] = kwargs[k]
        return dicts

    def get_sizeslist(self, lis):
        return len(lis)

    def add_dict(self,dicts, k, v):
        dicts[k] = v

    def update_ver(self, ver, v):
        ver = v

    def should_equal(self, v1, v2):
        assert str(v1) == str(v2), v1 + "和" + "值不相等"

