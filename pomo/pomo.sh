#!/bin/bash

# get user input in minutes
read -p "Enter countdown time in minutes: " countdown_minutes

# convert minutes to seconds
countdown_time=$((countdown_minutes * 60))

# countdown loop
for i in $(seq $countdown_time -1 1); do
  # calculate progress percentage
  progress=$(echo "scale=2; ($countdown_time - $i + 1) * 100 / $countdown_time" | bc)

  # build progress bar
  bar=$(printf "%-${countdown_minutes}s" " ")
  bar=${bar// /#}
  bar="${bar:0:$((i / 60))}>"

  # output progress bar and countdown timer
  echo -ne "$bar $progress% ($(date -u -d @$i +%M:%S))\r"

  sleep 1
done

# beep and send notification when countdown is complete
echo "Time is up!"
paplay /usr/share/sounds/freedesktop/stereo/complete.oga &
notify-send "Countdown complete!" "The countdown has finished."

