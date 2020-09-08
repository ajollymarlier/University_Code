



#!/usr/bin/bash

./echo_arg csc209 > ./echo_out.txt #Command 1
./echo_stdin < ./echo_stdin.c  #Command 2
./count 210 | wc --chars #Command 3
ls -S | ./echo_stdin #Command 4

