#!/usr/bin/fish

# Config
set SERVER localhost
set PORT 6667
set CHANS test
set NICK notfish
set IRCUSER "$NICK $SERVER $SERVER :$NICK"
set LEADER '$'

# Constants
set IN 'bot.input'
set OUT 'bot.output'
set ERR 'bot.error'
set LOG 'bot.log'

# Functions
function log -d 'Write to log file'
    echo (date '+[%y:%m:%d %T]')' '$argv[1] | tee -a $LOG
end

function out -d "Write to IRC server"
    set -l output $argv[1]
    log '> '$output
    echo $output | head -c 512 >>$OUT
end

function msg -d "Send a PRIVMSG"
    set -l chan $argv[1]
    set -l rest $argv[2..-1]
    out "PRIVMSG $chan :$rest"
end

function me -d "Send a PRIVMSG ACTION"
    set -l chan $argv[1]
    set -l rest $argv[2..-1]
    msg $chan \001'ACTION '$rest
end

function clean_chan -d "Cleanup a channel name"
    echo $argv[1] | tr -d ' \007,'
end

function join -d "Join a channel"
    set -l chan (clean_chan $argv[1])
    if test -n $chan
        out "JOIN $chan"
    end
end

function part -d "Part a channel"
    set -l chan (clean_chan $argv[1])
    if test -n $chan
        out "PART $chan :blub blub"
    end
end

# Initialization
echo "" >$OUT
mkdir -p var/

# Session
log ">>>>> New Session <<<<<"
out "NICK $NICK"
out "USER $IRCUSER"
for chan in $CHANS
    join "#$chan"
end
tail -f $OUT | telnet $SERVER $PORT ^$ERR | tee $IN | while read input;
    log '< '$input
    switch $input
        case 'PING*'
            out $input | sed 's/I/O/'
        case '*PRIVMSG*'
            set components (echo $input | tr ' ' \n)
            if [ (count $components) -ge '4' ]
                set nick (echo $components[1] | sed 's/^:\(.*\)!.*/\1/')
                set chan $components[3]
                # if a user is PM'ing us, rather than a chan
                if test $chan = $NICK
                    set chan $nick
                end
                set cmd (echo $components[4] | sed -n 's/:'$LEADER'\([[:alnum:]]\+\)/\1/p')
                if [ (count $components) -ge '5' ]
                    set rest (echo $components[5..-1] | tr \n ' ' | sed 's/[[:space:]]*$//')
                else
                    set rest ''
                end
                if test -n "$cmd" -a -f bin/$cmd.fish
                    log '. 'bin/$cmd.fish
                    . bin/$cmd.fish
                end
            end
    end
end
