#coding:utf-8
__author__ = "ila"

import os
import urllib.request, json
import base64
import urllib.parse
import requests

class BaiDuBce(object):

    client_id = '7Otjpv2kn0ljQk45qXOXh5MO'  # ak
    client_secret = 'BMfbXRbTIVaB4C3SbRTtGqDv1wHDvyXS'  # sk

    def get_alitoken(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + self.client_id + '&client_secret=' + self.client_secret + ''
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        access_token = 'err'

        if (content):
            # print(content)
            access_token = json.loads(content.decode('utf-8'))['access_token']
            # print(access_token)

        return access_token

    def open_pic2base64(self,image):
        f = open(image, 'rb')
        img = base64.b64encode(f.read()).decode('utf-8')
        return img

    def bd_check2pic(self,image1, image2):

        request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
        params = json.dumps(
            [{"image": self.open_pic2base64(image1), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
             {"image": self.open_pic2base64(image2), "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"}])

        access_token = self.get_alitoken()
        request_url = request_url + "?access_token=" + access_token

        params = params.encode("utf-8")

        req = urllib.request.Request(url=request_url, data=params)
        req.add_header('Content-Type', 'application/json')

        res = urllib.request.urlopen(req)
        content = res.read()

        score = 0
        
        if content:
            try:
                score = json.loads(content.decode('utf-8'))['result']['score']
            except:
                pass

        return score

    def ocr_checkpic(self, image):

        access_token = self.get_alitoken()
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={}".format(access_token)

        payload={
            "image": self.open_pic2base64(image),
            "language_type": "CHN_ENG",
            "detect_direction": "true",
            "detect_language": "true",
            "paragraph": "true",
            "probability": "false"
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", request_url, headers=headers, data=payload)
        json_res = json.loads(response.text)

        result = ""
        try:
            for item in json_res.get("words_result"):
                result = result + item["words"] + '\n'
        except:
            pass

        return result

    def dish_checkpic(self,image):

        access_token = self.get_alitoken()
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/dish?access_token={}".format(access_token)

        payload={"image": self.open_pic2base64(image), "baike_num": 1}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", request_url, headers=headers, data=payload)
        json_res = json.loads(response.text)

        return json_res.get("result")[0]

    def animal_checkpic(self, image):

        access_token = self.get_alitoken()
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/animal?access_token={}".format(access_token)

        payload={"image": self.open_pic2base64(image), "baike_num": 1}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", request_url, headers=headers, data=payload)
        json_res = json.loads(response.text)

        return json_res.get("result")[0]

    def plant_checkpic(self, image):

        access_token = self.get_alitoken()
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/plant?access_token={}".format(access_token)

        payload={"image": self.open_pic2base64(image), "baike_num": 1}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        
        response = requests.request("POST", request_url, headers=headers, data=payload)
        json_res = json.loads(response.text)

        return json_res.get("result")[0]

    def advanced_general(self, image):

        access_token = self.get_alitoken()
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v2/advanced_general?access_token={}".format(access_token)

        payload={"image": self.open_pic2base64(image), "baike_num": 1}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        response = requests.request("POST", request_url, headers=headers, data=payload)
        json_res = json.loads(response.text)

        return json_res.get("result")[0]

    def car_checkpic(self,image):

        access_token = self.get_alitoken()
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/car?access_token={}".format(access_token)

        payload={"image": self.open_pic2base64(image), "baike_num": 1}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        response = requests.request("POST", request_url, headers=headers, data=payload)
        json_res = json.loads(response.text)

        return json_res.get("result")[0]

    def bodynum_checkpic(self, image):

        access_token = self.get_alitoken()
        request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_num?access_token={}".format(access_token)

        payload={"image": self.open_pic2base64(image)}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        response = requests.request("POST", request_url, headers=headers, data=payload)
        json_res = json.loads(response.text)

        return json_res.get("person_num")

    def get_file_content_as_base64(self,path, urlencoded=False):
        """
        获取文件base64编码
        :param path: 文件路径
        :param urlencoded: 是否对结果进行urlencoded
        :return: base64编码信息
        """
        with open(path, "rb") as f:
            content = base64.b64encode(f.read()).decode("utf8")
            if urlencoded:
                content = urllib.parse.quote_plus(content)
        return content

    def asr_checkpic(self, filePath):
        url = "https://vop.baidu.com/server_api"

        payload = json.dumps({
            "format": "pcm",
            "rate": 16000,
            "channel": 1,
            "cuid": "cY0cQnusBPD596qZ9HllYtM75yIqaCGj",
            "token": self.get_alitoken(),
            "speech": self.get_file_content_as_base64(filePath),
            "len": os.path.getsize(filePath)
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_res = json.loads(response.text)

        return json_res.get("result")[0]



if __name__=='__main__':
    client_id = 'x20xOjtOsAtbQhm2WBuifuQw'  # ak
    client_secret = 'O7yMp2dmOnCtQtBokUt1gN6hgFCcLLcp'  # sk

    # 本地图片地址，根据自己的图片进行修改
    image1 = 'nude1.jpg'
    image2 = 'nude2.jpg'

    bdb=BaiDuBce()
    bdb.bd_check2pic(image1, image2)