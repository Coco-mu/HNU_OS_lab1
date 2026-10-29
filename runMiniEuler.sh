#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"
QEMU=${QEMU:-qemu-system-aarch64}

# sh runMiniEuler.sh 直接运行
# sh runMiniEuler.sh -S 启动后在入口处暂停等待调试
printf '%s\n' "$QEMU -machine virt,gic-version=2 -m 1024M -cpu cortex-a53 -nographic -kernel build/miniEuler -s $*"
exec "$QEMU" -machine virt,gic-version=2 -m 1024M -cpu cortex-a53 -nographic -kernel build/miniEuler -s "$@"
