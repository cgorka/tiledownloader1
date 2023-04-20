#!/bin/bash

# Define an array of parameter values
params=("a" "b" "c")
echo "Starting script..."
# Loop through the parameter values
for param in "${params[@]}"
do
    # Start a new screen session with a name based on the parameter value
    screen -dmS "session_$param"

    # Send a command to the screen session to run the Python script with the current parameter value
    screen -S "session_$param" -X stuff "python3 a.py $param^M"
    sleep 1
    echo  "session_$param" -X stuff "python3 a.py $param^M"
    sleep 1
done