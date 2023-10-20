#!/bin/bash

# enable running inner commands (e.g. starting a new GUI terminal) with a healthy environment
# by saving the environment in a temporary file
cd
environment_temp_file=$(mktemp)
env | sed 's/^\([^=]*\)=\(.*\)$/export \1="\2"/' > "$environment_temp_file"

# Define the tmux session name
TMUX_SESSION_NAME="violetdeck"

# Check if the session exists, discarding output
# We're just looking for the exit code here
already_running=false
ps aux | grep [v]ioletdeck &>/dev/null
if [ $? = 0 ] ; then
    already_running=true
fi

echo already running $already_running

working_dir=~/git/violet/vsdlib

echo $(date): whoami $(whoafull_commandmi) HOME $HOME >> $working_dir/nohup.out

# make sure user has X authorization
# cp /tmp/xauth_* /home/violet/.Xauthority
export XAUTHORITY=$(ls -1 /tmp/xauth_*|head -1)

# If the exit code wasn't 0, the session doesn't exist, so create it
if ! $already_running ; then
    # Start a detached session
    tmux new-session -d -s $TMUX_SESSION_NAME # -c $working_dir

    # create a bottom pane
    # don't set `# tmux -c $working_dir` because then any processes started in the tmux session
    # is started in that working directory
    tmux split-window -v -t $TMUX_SESSION_NAME

    # # both panes
    # for pane in {0..1} ; do
    #     # set working directory
    #     tmux send-keys -t $TMUX_SESSION_NAME:0.$pane "cd $working_dir" C-m
    #     # make sure stuff can interact with X server
    #     # tmux send-keys -t $TMUX_SESSION_NAME:0.$pane "export XAUTHORITY=/home/violet/.Xauthority" C-m
    # done

    # bottom pane: start the stream deck
    tmux send-keys -t $TMUX_SESSION_NAME:0.1 'export DISPLAY=:0.0' C-m
    tmux send-keys -t $TMUX_SESSION_NAME:0.1 "export HOME=$HOME" C-m
    tmux send-keys -t $TMUX_SESSION_NAME:0.1 'export XDG_RUNTIME_DIR=/run/user/1000' C-m
    # tmux send-keys -t $TMUX_SESSION_NAME:0.1 'sleep 10' C-m
    tmux send-keys -t $TMUX_SESSION_NAME:0.1 "/home/violet/bin/violetdeck --environment-file $environment_temp_file" C-m

fi
