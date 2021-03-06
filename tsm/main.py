# -*- coding: utf-8 -*-
# import logging
# import logging.config
#
# import os
# import ConfigParser
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
#
# baseconfdir="conf"
# loggingconf= "logging.config"
# businessconf= "business.ini"
#
# def main():
#     try:
#         from auto.mainengine import Monitor
#         from auto.mainengine import BatchOrder
#         from PyQt4.QtCore import QCoreApplication
#         """主程序入口"""
#         app = QCoreApplication(sys.argv)
#
#         logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
#         logger = logging.getLogger("run")
#
#         cf = ConfigParser.ConfigParser()
#         cf.read(os.path.join(os.getcwd(), baseconfdir, businessconf))
#
#         me = Monitor(cf)
#         #bo = BatchOrder(cf)
#
#         sys.exit(app.exec_())
#     except BaseException,e:
#         logger.exception(e)
#
#
# if __name__ == '__main__':
#     main()

import logging
import logging.config

from datetime import datetime
import os
import ConfigParser
import sys
reload(sys)
sys.setdefaultencoding('utf8')

baseconfdir="conf"
loggingconf= "logging.config"
businessconf= "business.ini"


from auto.mainengine import Monitor
from PyQt4.QtCore import QCoreApplication


logging.config.fileConfig(os.path.join(os.getcwd(), baseconfdir, loggingconf))
logger = logging.getLogger("run")

cf = ConfigParser.ConfigParser()
cf.read(os.path.join(os.getcwd(), baseconfdir, businessconf))


def start():
    try:
        """主程序入口"""
        logger.info('start')

        global me
        me.start()

    except BaseException,e:
        logger.exception(e)

def stop():
    try:
        logger.info('stop')

        global me
        me.stop()

    except BaseException,e:
        logger.exception(e)


def monitor():
    try:
        from apscheduler.schedulers.qt import QtScheduler
        app = QCoreApplication(sys.argv)
        global me
        me = Monitor(cf)
        sched = QtScheduler()
        # m = Main()
        # sched.add_job(start, 'cron', id='first', day_of_week ='0-4', hour = 9, minute = 11)
        # sched.add_job(stop, 'cron', id='second', day_of_week ='0-4', hour = 15, minute = 20)
    #    sched.add_job(start, 'cron', id='first',  hour = 9, minute = 16)
    #    sched.add_job(stop, 'cron', id='second',  hour = 15, minute = 10)
        #如有显式配置调度时间，则根据调度时间来设置调度计划
        #如果没有配置，则分别取工作时间的最前和最后时间作为任务计划的开始和结束时间
        if cf.has_option('monitor','schedtime'):
            schedtime = cf.get('monitor', 'schedtime').strip().split('~')
            startime = schedtime[0].split(':')
            stoptime = schedtime[1].split(':')

        else:
            workingtimelist = []
            for x in cf.get('monitor', 'workingtime').strip().split(','):
                for x1 in x.split('~'):
                    workingtimelist.append(x1)
            #workingtimelist.sort()
            startime = workingtimelist[0].split(':')
            stoptime = workingtimelist[-1].split(':')

        sched.add_job(start, 'cron', id='first', day_of_week='0-4', hour=int(startime[0]), minute=int(startime[1]))
        sched.add_job(stop, 'cron', id='second', day_of_week='0-4', hour=int(stoptime[0]), minute=int(stoptime[1]))
        logger.info('schedulers startime:%s stoptime:%s', startime, stoptime)
        sched.start()


        #上面的任务调度只有在未来时间才会触发
        #这里加上判断当前时间如果在工作时间，则要开启
        worktime = cf.get("monitor", "workingtime").split(',')
        worktimerange = []
        for i in range(len(worktime)):
            worktimerange.append(worktime[i].split('~'))

        time_now = datetime.now().strftime("%H:%M")
        for i in range(len(worktimerange)):
            if time_now > worktimerange[i][0] and time_now < worktimerange[i][1]:
                logger.info('now:%s is in the worktimerange,will start the job immediately', time_now)
                start()

        app.exec_()
    except BaseException,e:
        logger.exception(e)

def test():
    try:
        from apscheduler.schedulers.qt import QtScheduler
        app = QCoreApplication(sys.argv)
        global me
        me = Monitor(cf)
        sched = QtScheduler()
        # m = Main()
        # sched.add_job(start, 'cron', id='first', day_of_week ='0-4', hour = 9, minute = 11)
        # sched.add_job(stop, 'cron', id='second', day_of_week ='0-4', hour = 15, minute = 20)
        sched.add_job(start, 'cron', id='first',  hour = 17, minute = 21,second = 0)
        sched.add_job(stop, 'cron', id='second',  hour = 21, minute = 10)
        sched.start()
        app.exec_()
    except BaseException,e:
        logger.exception(e)


def runow():
    try:
        app = QCoreApplication(sys.argv)
        me = Monitor(cf)
        me.start()
        sys.exit(app.exec_())
    except BaseException, e:
        logger.exception(e)

if __name__ == '__main__':
    monitor()
