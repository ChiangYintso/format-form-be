from flask import make_response


class CustomException(Exception):

    def __init__(self, err_code, err_msg, status_code=200):
        self.err_code = err_code
        self.err_msg = err_msg
        self.status_code = status_code

    def make_response(self, request_str):
        res = make_response({
            'err_code': self.err_code,
            'err_msg': self.err_msg,
            'request': request_str
        }, self.status_code)
        res.mimetype = 'application/json'

        return res
