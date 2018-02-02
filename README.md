# QQMusicAPI

网页QQ音乐的一些API

## 安装

1. 下载[离线whl文件](https://github.com/metesa/QQMusicAPI/releases)

2. 命令行输入安装命令
```shell
$ pip install qqmusicapi-0.3.0-py3-none-any.whl
```

## 用法

1. 搜索歌曲并下载
```python
from qqmusicapi import QQMusicUtil as qmu

# 从歌单抓取信息（https://y.qq.com/n/yqq/playlist/1177101483.html），并下载到song文件夹

# 写法一
qmu.grab_playlist(list_id=1177101483).download(folder='song')

# 写法二
song_list = qmu.grab_playlist(list_id=1177101483)
song_list.download(folder='song')
```
2. 抓取歌单并下载
```python
from qqmusicapi import QQMusicUtil as qmu

# 搜索包含Panama的歌曲，显示第1页，前5个元素，并下载想要的歌曲到 Panama 文件夹
# 搜索完成后会显示搜索结果，输入想要的歌曲序号即可下载（输入0为全部下载）

# 写法一
qmu.search_song(key_word='Panama', page=1, num=5).download(folder='panama')

# 写法二
song_list = search_song(key_word='Panama', page=1, num=5)
song_list.download(folder='panama')
```
3. 查看歌曲列表中的歌曲信息
```python
from qqmusicapi import QQMusicUtil as qmu

# 生成歌曲列表，输出列表中的歌曲信息

# 写法一
qmu.grab_playlist(list_id=1177101483).print()
qmu.search_song(key_word='Panama', page=1, num=5).print()

# 写法二
song_list1 = qmu.grab_playlist(list_id=1177101483)
song_list1.print()
song_list2 = qmu.search_song(key_word='Panama', page=1, num=5)
song_list2.print()
```