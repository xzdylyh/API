#_*_coding:utf-8_*_
#_*_coding:utf-8_*_
import requests,json
from interface_project.base.base_config import BaseConfig
from interface_project.library.scripts import getYamlfield
from interface_project.library.scripts import retry
from interface_project.globalVar import gl

class ChargeClass(object):
    url = "/charge/receiptbatch"
    payload = '------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="req"\r\n\r\n{"cno":1262797,"shop_id":"1429830612","money":1,"biz_id":1234,"cashier_id":1127401356}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="appid"\r\n\r\ndp1svA1gkNt8cQMkoIv7HmD1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="ts"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="sig"\r\n\r\n1\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="v"\r\n\r\n2.0\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--'
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'cache-control': "no-cache",
        'postman-token': "07801abb-5d4e-6c77-6e76-61c0221106c5"
    }

    def __init__(self):
        self.baseUrl  = BaseConfig().base_url
        self.url = self.baseUrl + self.url

    #储值预览
    @property
    @retry(reNum=getYamlfield(gl.configFile)['RETRY']['ReNum'])
    def chargeReceiptbatch(self):
        res = requests.request("POST",self.url,data=self.payload,headers=self.headers)
        if res.status_code ==200:
            return res.json()
        else:
            return {"errcode": 9001, "errmsg": str(res)}

if __name__=="__main__":
    print json.dumps(ChargeClass().chargeReceiptbatch).decode('unicode-escape')