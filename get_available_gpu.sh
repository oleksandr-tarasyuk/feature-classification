#!/bin/bash

set -e
if hash nvidia-smi 2>/dev/null; then
  export CUDA_VISIBLE_DEVICES=$(nvidia-smi --query-gpu=memory.free,index --format=csv | sort -h -r | head -1 | awk -F',' '{ print $2}')
fi

exec "$@"