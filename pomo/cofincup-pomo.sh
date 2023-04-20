#!/bin/bash

# get user input in minutes
read -p "Enter countdown time in minutes: " countdown_minutes

# confirm countdown time with user
read -p "Start a countdown of $countdown_minutes minutes? [Y/n]" confirm
confirm=${confirm:-Y} # set default value to Y if user presses enter without entering a value
echo "OK. Will notify you when time's up."

# exit script if user doesn't confirm countdown
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
  echo "Countdown canceled."
  exit 0
fi

# convert minutes to seconds
countdown_time=$((countdown_minutes * 60))

# ignore hangup signal and continue running in the background
nohup bash -c "sleep $countdown_time && paplay /usr/share/sounds/freedesktop/stereo/complete.oga && notify-send 'Countdown complete!' 'The countdown has finished.'" > /dev/null 2>&1 & disown

