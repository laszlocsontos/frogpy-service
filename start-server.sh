#!/bin/sh

if [ -z "${ENVIRONMENT}" ]; then
  export ENVIRONMENT=development
fi

logs_dir=logs
log_file=$logs_dir/server.log

if [ "${ENVIRONMENT}" != "development" ]; then
  mkdir -p logs

  timestamp=$(date +%Y%m%d.%H%M%S.%s)

  if [ -f $log_file ]; then
    mv $log_file $log_file.$timestamp
  fi

  exec 1<&-
  exec 2<&-
  exec 1<>$log_file
  exec 2>&1
fi

. ./init-venv.sh

echo "Running in a ${ENVIRONMENT} environment"

envfile="env/${ENVIRONMENT}"

if [ -f $envfile ]; then
  echo "Loading additional variables from ${envfile}"

  set -a
  . $envfile
fi

if [ "${ENVIRONMENT}" != "development" ]; then
  python runserver.py &
  echo $! > logs/server.pid
else
  python runserver.py
fi
