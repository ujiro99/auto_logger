FROM panubo/sshd:latest

MAINTAINER Yujiro Takeda <siro.cola@gmail.com>

Add .ssh/id_rsa.pub /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys

Add log_to_rom /usr/local/bin/log_to_rom
RUN chmod a+x /usr/local/bin/log_to_rom

