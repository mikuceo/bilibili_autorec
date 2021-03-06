import subprocess
from pymediainfo import MediaInfo
from utils.log import Log
from utils.load_conf import Config
from utils.threadRecoder import threadRecorder
from utils.infos import Infos
import threading
import os
import re
import datetime
import time
import json

logger = Log()()


class Queue():
    def __init__(self):
        self._lock = threading.Lock()
        self._lock2 = threading.Lock()
        self.config = Config()
        self.infos = Infos()
        self.queue = []
        self.qname = ''
        self.func = lambda x:time.sleep(400)
        self.threadRecorder = threadRecorder()
        self.base_num = 0

    def func_call(self, key):
        with self._lock2:
            logger.info('%s 开始%s' % (self.infos.copy()[key]['uname'], self.qname))
            live_info = self.infos.copy()[key]
            live_info['queue_status'] = self.base_num
            self.infos.update(key, live_info)
            self.func(key)
            live_info['queue_status'] = self.base_num + 500
            live_info['finish_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.infos.update(key, live_info)

    def update_status(self):
        for key in self.queue:
            live_info = self.infos.copy()[key]
            live_info['queue_status'] = self.base_num + self.queue.index(key) + 1
            self.infos.update(key, live_info)

    def enqueue(self, key):
        with self._lock:
            live_info = self.infos.copy()[key]
            live_info['queue_status'] = self.base_num + len(self.queue) + 1
            if key not in self.queue:
                self.queue.append(key)
                logger.info('%s 进入%s等待队列' % (self.infos.copy()[key]['uname'],self.qname))
            else:
                self.queue.remove(key)
                self.queue.append(key)
                logger.info('%s 在%s等待队列中的状态更新了' % (self.infos.copy()[key]['uname'],self.qname))
            self.infos.update(key, live_info)

    def dequeue(self):
        if self._lock2.locked():
            return None
        with self._lock:
            with self._lock2:
                if len(self.queue) > 0:
                    key = self.queue[0]
                    del self.queue[0]
                    self.update_status()
                    logger.info('%s 退出%s等待队列' % (self.infos.copy()[key]['uname'],self.qname))
                    return key
                else:
                    return None

    def run(self):
        self.threadRecorder.add('%s heartbeat' % self.qname,self.heartbeat,None,True)
        while True:
            time.sleep(1)
            if len(self.queue) > 0:
                key = self.dequeue()
                if key is not None:
                    self.threadRecorder.add('%s_%s' % (self.qname,key),self.func_call,[key,],False)

    def heartbeat(self):
        while True:
            time.sleep(180)
            logger.info('当前%s队列情况: %s' % (self.qname, ' '.join([self.infos.copy()[key]['uname'] for key in self.queue])))
