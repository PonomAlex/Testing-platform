#!/usr/bin/env sh
set -eu

host="$1"
port="$2"
shift 2

if [ "$1" = "--" ]; then
  shift
fi

echo "Waiting for ${host}:${port} ..."
until nc -z "$host" "$port"; do
  sleep 1
done
echo "${host}:${port} is ready."

exec "$@"