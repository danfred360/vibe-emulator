#!/bin/bash

. .secret
alias v-init="python3.10 -m venv project/venv && . project/venv/bin/activate && pip3.10 install -r requirements.txt"
alias v-run=". project/venv/bin/activate && python3.10 project"