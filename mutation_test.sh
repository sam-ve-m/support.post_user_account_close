#! /bin/bash
export PYTHONPATH=$PWD/func
mutatest -s ./func/src -y 'if' 'nc' 'ix' 'su' 'bs' 'bc' 'bn' -x 60 -n 1000 -t 'python3 -m pytest'