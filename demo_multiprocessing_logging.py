#!/usr/bin/env python
"""
    ** python跨进程logger demo **
    pip install multiprocessing-logging
    https://pypi.org/project/multiprocessing-logging/
    Only works on POSIX systems and only Linux is supported. It does not work on Windows.
"""
import os
import time
import random
import logging
from multiprocessing import Pool
from multiprocessing_logging import install_mp_handler


def test_process(n):
    my_sum = 0
    for x in range(n):
        my_sum += x

    time.sleep(random.randint(0, 4))
    logger.info(f'[PID: {os.getpid()}] sum is {my_sum}.')


if __name__ == '__main__':
    # log utility
    global logger
    logger = logging.getLogger('demo_mp_logging')  # 父logger
    install_mp_handler(logger)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('multiprocessing_logging.log', encoding='utf-8')
    fh.setLevel(logging.DEBUG)
    # Using the customized Formatter due to timezone issue.
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)

    logger.info('Initialized multiprocessing logger.')

    p = Pool(os.cpu_count())

    for i in range(100, 400):
        p.apply_async(test_process, args=(i,))

    p.close()
    p.join()
    logger.info('End multi process.')
