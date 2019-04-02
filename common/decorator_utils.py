# -*- coding:utf-8 -*-
import logging
import time
import functools
from collections import Iterable


def time_cost(prefix=""):
    # 耗时统计
    def wrapper(func):
        @functools.wraps(func)
        def inner_func(*args, **kwargs):
            start_t = time.time()
            res = func(*args, **kwargs)
            cost = time.time() - start_t
            if prefix:
                logging.info("[%s][%s] cost %ss", prefix, func.__name__, cost)
            inner_func.cost_time = cost
            return res
        return inner_func
    return wrapper


# 类型强校验,一个变量可以允许多种类型判断
def type_checker(*ty_args, **ty_kwargs):
    def get_name_values_map(func, *args, **kwargs):
        arg_name_values_map = {}
        arg_names = func.__code__.co_varnames
        for c in range(len(args)):
            arg_name_values_map[arg_names[c]] = args[c]
        for arg_name, arg_value in kwargs.items():
            arg_name_values_map[arg_name] = arg_value
        return arg_name_values_map

    def get_name_bound_types(func):
        arg_names = func.__code__.co_varnames
        arg_name_values_map = {arg_name: set() for arg_name in arg_names}
        for c in range(len(ty_args)):
            arg_types = ty_args[c]
            arg_name = arg_names[c]
            if isinstance(arg_types, Iterable):
                for arg_type in arg_types:
                    arg_name_values_map[arg_name].add(arg_type)
            else:
                arg_name_values_map[arg_name].add(arg_types)
        for arg_name, arg_types in ty_kwargs.items():
            if isinstance(arg_types, Iterable):
                for arg_type in arg_types:
                    arg_name_values_map[arg_name].add(arg_type)
            else:
                arg_name_values_map[arg_name].add(arg_types)
        return arg_name_values_map

    # 类型检查,可以规定只检查部分类型,且支持多种类型检查
    def wrapper(func):
        # 变量名和检查的类型绑定
        name_bound_types = get_name_bound_types(func)

        @functools.wraps(func)
        def inner_func(*args, **kwargs):
            arg_name_values_map = get_name_values_map(func, *args, **kwargs)
            for bound_name, bound_types in name_bound_types.items():
                if len(bound_types) == 0:
                    continue
                value = arg_name_values_map[bound_name]
                need_types = tuple(name_bound_types[bound_name])
                if isinstance(value, need_types):
                    raise TypeError("arg %s(%s) must be %s type" % (bound_name, value, need_types))
            return func(*args, **kwargs)
        return inner_func
    return wrapper
