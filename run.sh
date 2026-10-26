#!/bin/sh
if [ "$1" == "competition" ]; then
    python3 RubiksCube3.py "$1"
elif [ "$#" -eq 4 ]; then
    python3 RubiksCubeSol.py "$1" "$2" "$3" "$4"
elif [ "$#" -eq 3 ]; then
    python3 RubiksCubeSol.py "$1" "$2" "$3"
elif [ "$#" -eq 2 ]; then
    python3 RubiksCubeSol.py "$1" "$2"
else
    python3 RubiksCubeSol.py "$1"
fi
