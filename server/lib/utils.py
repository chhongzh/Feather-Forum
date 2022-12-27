"""
此文件属于Feather-Forum!
© 2022 chhongzh

实用工具
"""
import sys
from . import share
log = share.log


def is_in(string: str, specil: str = "!@#$%^&*()+_|\\[]{}:;\"\'?/>.<,") -> bool:
    """判断是否存在于string

    Args:
        string: 需查询的字符串
        specil: 需查询的字符串

    Returns:
        True/False
    """
    for char in specil:
        if (char in string):
            return True
    else:
        return False


def check_version(target=(3, 9, 6)) -> bool:
    """判断是否存在于string

    Args:
        string: 需查询的字符串
        specil: 需查询的字符串

    Returns:
        True/False
    """
    return (sys.version_info.major, sys.version_info.minor,
            sys.version_info.micro) >= target
