# coding=utf-8

import os
import sys

# __all__ = ['__init__', 'download']


class QQMusicSongList:
    """
    QQ音乐歌曲信息列表类，包含一系列歌曲的songmid和标题信息
    """
    def __init__(self, song_list):
        """
        初始化

        :param song_list: 输入的歌曲信息列表
        """
        self.song_list = song_list

    def __len__(self):
        return len(self.song_list)

    def __iter__(self):
        return self.song_list

    def __getitem__(self, n):
        if isinstance(n, int):
            return self.song_list[n]
        elif isinstance(n, slice):
            return self.song_list[n]

    def download(self, folder='song'):
        """
        下载歌曲列表中的所有歌曲

        :param folder: 歌曲保存的目录名，若指定的是完整的绝对地址，则按照绝对地址存放。默认值是'song'文件夹
        """
        idx = 1
        if os.path.exists(folder):
            path = folder
        else:
            path = os.path.join(sys.path[0], folder)
        print('开始下载......')
        print('歌曲总数：{}'.format(len(self)))
        print('保存路径：{}'.format(os.path.abspath(path)))
        for song in self.song_list:
            print('第 {} 首：'.format(idx))
            song.download(path)
            idx += 1
        print('完成下载......')

    def print(self):
        """
        在控制台输出歌曲列表
        """
        print('列表包含 {} 首歌曲：'.format(len(self)))
        str_len = len(str(len(self)))
        for idx, song in enumerate(self.song_list):
            print('  {}. {}'.format(str(idx + 1).ljust(str_len), song))
