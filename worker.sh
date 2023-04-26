#! /usr/bin/env bash
set -e

python3 project/queue/pre_start.py

if [ -n "${RUN}" ]; then
  ${RUN}
else
  celery -A project.queue.worker worker -l info -Q ${DMP_QUEUE_NAME} -c 1
fi
