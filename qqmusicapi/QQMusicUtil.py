# coding=utf-8

import urllib
import sys
import json

from qqmusicapi import QQMusicSongList
from qqmusicapi import QQMusicSong
from qqmusicapi import ConstVar

# __all__ = ['search_song', 'grab_playlist']


"""
QQ音乐API的操作类，所有方法用于生成歌曲信息列表，目前实现的操作包括：

1.搜索关键词查找歌曲，生成歌曲信息列表
2.提取歌单歌曲，生成歌曲信息列表
"""


def search_song(key_word, page=1, num=20):
    """
    根据关键词查找歌曲

    :param key_word: 搜索关键词
    :param page: 显示的页面
    :param num: 显示的数量
    :returns: 歌曲信息列表类。可以直接下载
    """
    print('====================\n开始查找歌曲并生成歌曲列表：')
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
    url += '?new_json=1&aggr=1&cr=1&flag_qc=0&p=%d&n=%d&w=%s' \
           % (page, num, urllib.parse.quote(key_word))
    response = ConstVar.session.get(url=url)
    response.encoding = 'utf-8'

    try:
        song_list = json.loads(response.text[9:-1])['data']['song']['list']
        print("查找到的歌曲如下：")
        for num, music in enumerate(song_list):
            sys.stdout.write('{}, {}, {}\n'.format(num + 1, music['title'], music['singer'][0]['title']))
        select_num = int(input('请输入意向歌曲的序号（全部下载请输入0）: '))
        if select_num < 1:
            return QQMusicSongList.QQMusicSongList(
                [QQMusicSong.QQMusicSong(
                    song['mid'],
                    song['title'].replace('/', '\\'),
                    song['singer'][0]['title']
                ) for song in song_list]
            )
        else:
            select_num -= 1
            return QQMusicSongList.QQMusicSongList(
                [QQMusicSong.QQMusicSong(
                    song_list[select_num]['mid'],
                    song_list[select_num]['title'].replace('/', '\\'),
                    song_list[select_num]['singer'][0]['title']
                )]
            )
    except ValueError:
        print('  [错误]: 不能成功解析搜索结果的json字符串\n  字符串内容:"{}"'.format(response.text))
        print('  请求url:' + url)
        print('任务失败')
        raise Exception()
    finally:
        print('====================')


def grab_playlist(list_id):
    """
    根据歌单id号生成歌曲信息

    :param list_id: 歌单id号，是一串数字，比如3575040006
    :returns 歌曲信息列表类。可以直接下载
    """
    print('====================\n开始抓取歌单并生成歌曲列表：')
    url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?format=json&disstid={}' \
          '&type=1&json=1&utf8=1&nosign=1&song_begin=0&song_num=100'.format(list_id)
    response = ConstVar.session.get(url=url, headers=ConstVar.text_headers)
    response.encoding = 'utf-8'

    try:
        song_list = json.loads(response.text)['cdlist'][0]['songlist']
        return QQMusicSongList.QQMusicSongList(
            [QQMusicSong.QQMusicSong(
                song['songmid'],
                song['songname'],
                song['singer'][0]['name']
            ) for song in song_list]
        )
    except ValueError:
        print('  [错误]: 不能成功解析抓取歌单的json字符串\n  字符串内容:"{}"'.format(response.text))
        print('  请求url:' + url)
        print('任务失败')
        raise Exception()
    finally:
        print('====================')


def test():
    print('Test 1: To download a playlist with id=3575040006 and save to folder named "依然范特西".')
    print('    url = https://y.qq.com/n/yqq/playlist/1177101483.html')
    song_list = grab_playlist(list_id=1177101483)
    song_list.print()
    # playlist.download(folder='依然范特西')
    print('Test 2: To download a song with key_word="Panama" within first 5 songs in search result page 1 and save to '
          'folder named "playlist1".')
    search_song(key_word='Panama', page=1, num=5).download(folder='panama')


if __name__ == "__main__":
    test()
