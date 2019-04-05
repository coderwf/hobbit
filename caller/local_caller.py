# -*- coding:utf-8 -*-

"""
  提供一组调用协议,不同模块之间禁止直接导入包进行调用,必须通过该协议进行调用
"""
import re
import logging
from common.cache.lru import LruCache


logging.basicConfig(level=logging.DEBUG)


class LocalServiceFuncNotFound(Exception):
    def __init__(self, url):
        self.url = url

    def __str__(self):
        return "无法找到本地服务%s" % self.url

    def __repr__(self):
        return self.__str__()


class BaseCaller:
    """

    """
    def exec(self, *args, **kwargs):
        raise NotImplementedError()


class LocalCaller(BaseCaller):
    """
        缓存最近调用,避免重复解析
    """
    def __init__(self, name="default", cached=1024*1024):
        """
          1M
        :param cached:
        """
        self._cache = LruCache(cached)
        self._alias = {}
        self._name = name

    def register_alias(self, alias, func):
        if alias in self._alias:
            logging.warning("[LocalCaller][register_alias][%s] alias %s already exists", self._name, alias)
            return
        if not callable(func):
            logging.warning("[LocalCaller][register_alias][%s] alias %s func is not callable", self._name, alias)
            return
        self._alias[alias] = func
        logging.info("[LocalCaller][register_alias][%s] register alias %s", self._name, alias)

    @staticmethod
    def _parse_func(url: str):
        params = url.split("/")
        if len(params) != 2:
            return None
        module_name = params[0]
        try:
            module = __import__(module_name, {}, {}, ["models"])
        except Exception as e:
            logging.error("[LocalCaller][_parse_func] import module %s error with %s", module_name, e)
            return None
        service_name = params[1]
        pattern = r"^([a-zA-Z_][\w]*\.)*([a-zA-Z_][\w]*)$"
        matcher = re.search(pattern, service_name)
        if matcher is None:
            logging.error("[LocalCaller][_parse_func] service name %s invalid", url)
            return None
        params = service_name.split(".")
        func = None
        for param in params:
            func = getattr(module, param)
        if not callable(func):
            logging.error("[LocalCaller][_parse_func] service %s is not callable", url)
            return None
        return func

    def _exec_alias(self, url: str, *args, **kwargs):
        alias = url[6:]
        if alias not in self._alias:
            logging.warning("[LocalCaller][_exec_alisa] alias[%s] not found", alias)
            return None
        func = self._alias.get(alias)
        return func(*args, **kwargs)

    def _exec_service(self, url: str, *args, **kwargs):
        """
        1.查找是否在缓存中
        2.解析并导入
        3.执行
        4.将其暂时缓存起来
        :param url:
        :param args:
        :param kwargs:
        :return:
        """
        func = self._cache.get(url)
        if func:
            return func(*args, **kwargs)
        logging.info("[LocalCaller][_exec_service] service %s not cached", url)
        func = self._parse_func(url)
        if not func:
            return None
        res = func(*args, **kwargs)
        # cache it
        logging.info("[LocalCaller][_exec_service] cache service %s", url)
        self._cache.set(url, func)
        return res

    def exec(self, url: str, *args, **kwargs):
        """

        :param url: common.util/hash_encode or alias:hash_encode
        :param args:
        :param kwargs:
        :return:
        """
        if url.startswith("alias:"):
            return self._exec_alias(url, *args, **kwargs)
        return self._exec_service(url, *args, **kwargs)


class LocalCallerService:
    local_caller_map = {"default": LocalCaller()}

    @staticmethod
    def register_alias(alias, func, group=None):
        """

        :param alias:
        :param func:
        :param group
        :return:
        """
        if not group:
            group = "default"
        if group not in LocalCallerService.local_caller_map:
            LocalCallerService.local_caller_map[group] = LocalCaller(name=group)
        caller = LocalCallerService.local_caller_map.get(group)
        caller.register_alias(alias, func)

    @staticmethod
    def exec(url: str, *args, **kwargs):
        """

        :param url:
        :param args:
        :param kwargs:
        :return:
        """
        # "[default]alias:hash_encode"
        # "[default]service.ser1/A.c"
        # 是否分group
        group_matcher = re.search(r"^\[(\w+)\]", url)
        group = "default"
        if group_matcher:
            group = group_matcher.group(1)
            url = re.search(r"^\[(\w+)\](?P<url>\S+)$", url)
            if url is None:
                logging.error("[LocalCallerService][exec] service %s  invalid ", url)
                return None
            url = url.group("url")
        if group not in LocalCallerService.local_caller_map:
            logging.error("[LocalCallerService][exec] service %s group %s not found", url, group)
            return None
        caller = LocalCallerService.local_caller_map.get(group)
        return caller.exec(url, *args, **kwargs)


def register_local_service(alias, group="default"):
    def wrapper(func):
        if not alias:
            logging.error("[register_local_service] bad alias %s ", alias)
        else:
            LocalCallerService.register_alias(alias, func, group=group)
        return func
    return wrapper


@register_local_service(alias="hash_code", group="service")
def hash_code(param):
    print(param)


if __name__ == "__main__":
    LocalCallerService.exec("[service]alias:hash_code", "i love you")



