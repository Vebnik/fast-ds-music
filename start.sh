#!/usr/bin/env bash
parent_dir="$(dirname $BASH_SOURCE)"

exec {$parent_dir}/venv/bin/python {$parent_dir}/main.py