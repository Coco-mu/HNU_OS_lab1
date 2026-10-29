#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$SCRIPT_DIR"

# sh makeMiniEuler.sh 不打印编译命令
# sh makeMiniEuler.sh -v 打印编译命令等详细信息
cmake -S src -B build
cmake --build build -- "$@"
