#!/bin/sh

command_name=mlog
file_name="${command_name}-complete.sh"
upper_name=$(echo $command_name | tr "[:lower:]" "[:upper:]")

eval _${upper_name}_COMPLETE=source ${command_name} > ${file_name}
mv ${file_name} ~/
cat <<EOF >> ~/.bashrc

# mlog command completion
. ~/${file_name}
EOF

