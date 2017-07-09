#!/bin/sh

LOCAL_SRC_DIR=$1
LOCAL_DST_DIR=$2

cd ${LOCAL_SRC_DIR}
LOG_FILE=`ls -t | head -1`

mv ${LOCAL_SRC_DIR}/${LOG_FILE} ${LOCAL_DST_DIR}/

