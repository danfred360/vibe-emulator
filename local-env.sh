#!/bin/bash

. .secret
alias v-init="python3.10 -m venv project/venv && . project/venv/bin/activate && pip3.10 install -r requirements.txt"
alias vibe-emulator="python3.10 project"