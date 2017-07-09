#!/usr/bin/expect

# exp_internal 1 # if you want debug log, uncomment.

set HOST_NAME      [lindex $argv 0]
set LOG_CMD        [lindex $argv 1]
set REMOTE_LOG_DIR [lindex $argv 2]
set REMOTE_DST_DIR [lindex $argv 3]
set PROMPT         "\[#$%>\]"
set timeout        10

spawn env LANG=C /usr/bin/ssh ${HOST_NAME}

expect {
    -glob "${PROMPT}" {
        send "${LOG_CMD}\n"
    }
}

expect {
    -glob "${PROMPT}" {
        send -- "cd ${REMOTE_LOG_DIR}\n"
    }
}

expect {
    -glob "${PROMPT}" {
        send -- "LOG_FILE=`ls -t | head -1`\n"
    }
}

expect {
    -glob "${PROMPT}" {
        send -- "mv \${LOG_FILE} ${REMOTE_DST_DIR}\n"
    }
}

expect {
    -glob "${PROMPT}" {
        send "exit\n"
        exit 0
    }
}

