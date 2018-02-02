# coding=utf-8

import os
import json


def find_valid_name(path, ext):
    """
    在前后缀之间加入序号用来生成一个不同名的保存名称

    :param path: 固定的路径前缀
    :param ext: 固定的路径后缀
    :returns: 保存文件名
    """
    if os.path.exists(path + ext):
        idx = 1
        current_path = '{}_{}{}'.format(path, idx, ext)
        while os.path.exists(current_path):
            idx += 1
            current_path = '{}_{}{}'.format(path, idx, ext)
        return current_path
    else:
        return path + ext


def print_json(json_content):
    """
    格式化显示json内容

    :param json_content: json内容
    """
    print(json.dumps(json_content, indent=4, sort_keys=False, ensure_ascii=False))
