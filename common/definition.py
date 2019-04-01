# -*- coding:utf-8 -*-


class FunctionRes:
    def __init__(self, success=True, message="", data=None):
        self.success = success
        self.message = message
        self.data = data

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def build_res(success=True, message="", data=None):
        return dict(success=success, message=message, data=data)
