#!/usr/bin/env bash

# This script waits for multiple TCP connections to be ready
# Usage: wait-for-it.sh host:port ... [-t timeout] [-- command args]

TIMEOUT=30
QUIET=0
HOSTS=()

usage() {
    echo "Usage: $0 host:port ... [-t timeout] [-- command args]"
    exit 1
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        *:* )
        HOSTS+=("$1")
        shift 1
        ;;
        -t)
        TIMEOUT="$2"
        shift 2
        ;;
        --)
        shift
        CMD="$@"
        break
        ;;
        *)
        usage
        ;;
    esac
done

if [[ ${#HOSTS[@]} -eq 0 ]]; then
    usage
fi

for HOSTPORT in "${HOSTS[@]}"; do
    HOST=$(echo "$HOSTPORT" | cut -d: -f1)
    PORT=$(echo "$HOSTPORT" | cut -d: -f2)
    echo "Waiting for $HOST:$PORT..."

    for i in $(seq $TIMEOUT); do
        nc -z "$HOST" "$PORT" && break
        echo "Waiting for $HOST:$PORT..."
        sleep 1
    done

    if [[ "$i" == "$TIMEOUT" ]]; then
        echo "Timed out waiting for $HOST:$PORT"
        exit 1
    fi
done

echo "All services are available, executing command"
exec $CMD
