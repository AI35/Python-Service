#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#  Dev By : Ali B Othman

import logging
from logging.handlers import SysLogHandler
import time,os

from service import find_syslog, Service


class MyService(Service):
    def __init__(self, *args, **kwargs):
        super(MyService, self).__init__(*args, **kwargs)
        # Set logger (sys log)
        self.logger.addHandler(SysLogHandler(address=find_syslog(),
                               facility=SysLogHandler.LOG_DAEMON))
        self.logger.setLevel(logging.INFO)

    def run(self):
        # What you want from service To Do
        while not self.got_sigterm():
            self.logger.info("I'm working...")
            time.sleep(5)


if __name__ == '__main__':
    # Service name
    servicename = 'My service'
    # Pid file name
    pidname = ('%s.pid' % servicename)
    import sys

    if len(sys.argv) != 2:
        sys.exit('Syntax: %s COMMAND\n[--start] to start service.\n[--stop] to stop service.\n[--status] to check service status.' % sys.argv[0])

    cmd = sys.argv[1].lower()
    # Pid dir
    service = MyService(servicename, pid_dir='/tmp')

    if cmd == '--start':
        if service.is_running():
            print('Service is already running.\nUse (%s --stop) to stop service' % sys.argv[0])
        else:
            service.start()
    elif cmd == '--stop':
        if not service.is_running():
            print('Service is already not running.')
        else:
            try:
                while service.is_running():
                    service.stop()
                    # Don't change time.sleep(1)
                    time.sleep(1)
            except Exception as e:
                if e == '[Errno 3] No such process':
                    os.remove('/tmp/%s' % pidname)
            if pidname in os.listdir('/tmp'):
                os.remove('/tmp/%s' % pidname)
    elif cmd == '--status':
        if service.is_running():
            print("Service is running.")
        else:
            print("Service is not running.")
    else:
        sys.exit('Unknown command "%s".\n[--start] to start service.\n[--stop] to stop service.\n[--status] to check service status.' % cmd)
