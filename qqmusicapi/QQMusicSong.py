# coding=utf-8

import base64
import os
import sys
import json

import qqmusicapi.ConstVar as ConstVar
import qqmusicapi.GeneralUtil as GeneralUtil

# __all__ = ['__init__', 'download']


class QQMusicSong:
    """
    QQ音乐歌曲类，存储了每首歌的关键信息
    """
    def __init__(self, media_mid, title, singer, download_lrc=True):
        """
        初始化音乐类

        :param media_mid: mid参数
        :param title: 歌曲名称
        :param singer: 歌手名称
        :param download_lrc: 是否下载歌词。默认值是下载歌词
        """
        self.filename = "C400%s.m4a" % media_mid
        self.song_mid = media_mid
        self._title = title
        self._singer = singer
        self.vkey = self._get_vkey()
        self.download_lrc = download_lrc

    def __str__(self):
        """
        生成歌曲信息字符串

        :return: 歌曲信息字符串
        """
        return '{} - {}'.format(self.title, self.singer)

    __repr__ = __str__

    def _get_vkey(self):
        """
        根据歌曲信息查找vkey值

        :returns: vkey值
        """
        url = 'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?'
        url += 'format=json&platform=yqq&cid=205361747&songmid=%s&filename=%s&guid=%s' \
               % (self.song_mid, self.filename, ConstVar.guid)
        response = ConstVar.session.get(url)
        try:
            vkey = json.loads(response.text)['data']['items'][0]['vkey']
            return vkey
        except ValueError:
            print('  [错误]: 不能成功解析vkey的json字符串\n  字符串内容:"{}"'.format(response.text))
            print('  请求url:' + url)
            raise Exception()

    def _music_save(self, path=os.path.join(sys.path[0], 'song')):
        """
        下载歌曲文件

        :param path: 歌曲保存路径。默认值是脚本同目录下的song文件夹
        """
        if not os.path.exists(path):
            os.makedirs(path)
        music_url = 'http://dl.stream.qqmusic.qq.com/%s?vkey=%s&guid=%s' % (self.filename, self.vkey, ConstVar.guid)
        music_data = ConstVar.session.get(music_url, headers=ConstVar.music_headers)
        if music_data.status_code != 200:
            print('  [错误]: 歌曲或网络错误')
            return
        desti_path = os.path.join(path, '{} - {}'.format(self.title, self.singer))
        with open(GeneralUtil.find_valid_name(desti_path, '.m4a'), 'wb') as music_file:
            for chunk in music_data.iter_content(chunk_size=512):
                if chunk:
                    music_file.write(chunk)
        print('  [信息]: 歌曲下载完成')

    def _lrc_save(self, path=os.path.join(sys.path[0], 'song')):
        """
        下载歌词文件

        :param path: 歌曲保存路径。默认值是脚本同目录下的song文件夹
        """
        if not os.path.exists(path):
            os.makedirs(path)
        lrc_url = 'http://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?g_tk=753738303&songmid=' + self.song_mid
        lrc_data = ConstVar.session.get(lrc_url, headers=ConstVar.text_headers)
        if lrc_data.status_code != 200:
            print('  [错误]: 歌词不存在或网络错误')
        desti_path = os.path.join(path, '{} - {}'.format(self.title, self.singer))

        try:
            lrc_dict = json.loads(lrc_data.text[18:-1])
            lrc_data = base64.b64decode(lrc_dict['lyric'])
            with open(GeneralUtil.find_valid_name(desti_path, '.lrc'), 'wb') as lrc_file:
                lrc_file.write(lrc_data)
            # 若有翻译歌词
            if lrc_dict['trans'] != "":
                lrc_data = base64.b64decode(lrc_dict['trans'])
                with open(GeneralUtil.find_valid_name(desti_path, '-trans.lrc'), 'wb') as lrc_file:
                    lrc_file.write(lrc_data)
            print('  [信息]: 歌词下载完成')
        except ValueError:
            print('  [错误]: 不能成功解析歌词的json字符串\n  字符串内容:"{}"'.format(lrc_data.text))
            print('  请求url:' + lrc_url)
            print('  [错误]: 歌词下载失败')
            raise Exception()

    def download(self, path=os.path.join(sys.path[0], 'song')):
        """
        下载歌词文件

        :param path: 保存路径。默认值是脚本同目录下的song文件夹
        """
        print('  [信息]: 开始下载歌曲 - {}'.format(self.title))
        self._music_save(path)
        if self.download_lrc:
            self._lrc_save(path)
        print('  [信息]: 完成下载歌曲 - {}'.format(self.title))

    @property
    def singer(self):
        return self._singer

    @singer.setter
    def singer(self, value):
        self._singer = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
