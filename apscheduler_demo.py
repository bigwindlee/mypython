import datetime
import logging
import pytz
from apscheduler.schedulers.blocking import BlockingScheduler


class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""

    def new_converter(self, timestamp):
        """
        把vps本地的时间转换为北京时间（不同时区的时间转换）
        :param self: 本函数赋值给Formatter的成员函数，而成员函数的第一个参数为self，需要为self保留位置；
        :param timestamp:
        :return: 返回time.struct_time结构表示的时间；
        """
        _ = self  # Just remove the warning
        return datetime.datetime.fromtimestamp(timestamp).astimezone(pytz.timezone('Asia/Shanghai')).timetuple()

    converter = new_converter


def ashares_main():
    pass


def task2():
    pass


def ashares_main_wrapper(logger):
    try:
        ashares_main(logger)
    except:
        logger.exception('Exception Logged')


if __name__ == '__main__':
    logger = logging.getLogger('ashares')  # 父logger
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('my.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)

    scheduler = BlockingScheduler()

    # 定时任务
    scheduler.add_job(ashares_main_wrapper, 'cron', args=(logger,), hour=4, minute=11, timezone='Asia/Shanghai')

    # 立即启动
    scheduler.add_job(task2)

    scheduler.start()
