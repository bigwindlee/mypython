#!/bin/sh
/usr/local/python3/bin/celery -A parallel.celery worker --concurrency=5 -l info
