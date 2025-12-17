#!/bin/bash
set -e
set -o pipefail

program_flash \
  -f ./BOOT.bin \
  -offset 0 \
  -flash_type qspi-x4-dual_stacked \
  -fsbl ./fsbl.elf \
  -url TCP:10.0.142.173:3121
