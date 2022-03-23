#!/bin/sh

if [ ! -d logs ]; then
  exit 1
fi

pid_file=logs/server.pid

if [ ! -f $pid_file ]; then
  exit 1
fi

server_ppid=$(cat $pid_file)
server_pid=$(pgrep -P $server_ppid)
pids=$(pidof python)

for pid in $pids; do
  if [ "${pid}" != "${server_ppid}" -a "${pid}" != "${server_pid}" ]; then
    continue
  fi

  kill $pid
  sleep 1
  kill -9 $pid
done

rm -f $pid_file
