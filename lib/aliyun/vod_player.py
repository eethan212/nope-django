# -*- coding: UTF-8 -*-
import json
from django.conf import settings
import traceback
from aliyunsdkcore.client import AcsClient
from aliyunsdkvod.request.v20170321 import GetPlayInfoRequest
from aliyunsdkvod.request.v20170321 import GetVideoPlayAuthRequest


class VodPlayer(object):
    """
    安装:
    pip install aliyun-python-sdk-vod
    https://help.aliyun.com/document_detail/61051.html?spm=a2c4g.11186623.2.43.33b7276dZ0AnXq#topic499
    使用:
    https://help.aliyun.com/document_detail/61052.html?spm=a2c4g.11186623.2.14.2ec979f0kNg219#InitVodClient
    https://help.aliyun.com/document_detail/61055.html?spm=a2c4g.11186623.2.18.56a0480fOozDsi#GetVideoPlayAuth
    """
    def __init__(self, vo_id):
        self.access_key_id = settings.ALIYUN_VOD_ACCESS_KEY
        self.access_key_secret = settings.ALIYUN_VOD_SECRET_KEY
        self.vo_id = vo_id
        self.client = None
        self.playinfo = None

    def init_vod_client(self, accessKeyId, accessKeySecret):
        regionId = 'cn-shanghai'   # 点播服务接入区域
        connectTimeout = 3         # 连接超时，单位为秒
        return AcsClient(accessKeyId, accessKeySecret, regionId,
                         auto_retry=True, max_retry_time=3, timeout=connectTimeout)

    def get_client(self):
        client = None
        try:
            client = self.init_vod_client(self.access_key_id, self.access_key_secret)
        except Exception as e:
            print(e)
            traceback.print_exec()
        self.client = client

    def get_play_info(self):
        self.get_client()
        request = GetPlayInfoRequest.GetPlayInfoRequest()
        request.set_accept_format('JSON')
        request.set_VideoId(self.vo_id)
        request.set_AuthTimeout(3600*5)
        response = json.loads(self.client.do_action_with_exception(request))
        return response

    def get_video_playauth(self):
        self.get_client()
        request = GetVideoPlayAuthRequest.GetVideoPlayAuthRequest()
        request.set_accept_format('JSON')
        request.set_VideoId(self.vo_id)
        request.set_AuthInfoTimeout(3000)
        response = json.loads(self.client.do_action_with_exception(request))
        return response
