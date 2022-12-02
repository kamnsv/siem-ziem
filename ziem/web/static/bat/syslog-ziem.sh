ip_address_ziem=192.168.154.8
ip_address_ziem="${1:-$ip_address_ziem}"

# Будут внесены правки в конфигурационный файл `/etc/audit/auditd.conf`.

sed -i '/max_log_file = /c\max_log_file = 4096' /etc/audit/auditd.conf
sed -i '/max_log_file_action = /c\max_log_file_action = ROTATE' /etc/audit/auditd.conf
sed -i '/space_left = /c\space_left = 256' /etc/audit/auditd.conf
sed -i '/space_left_action = /c\space_left_action = SYSLOG' /etc/audit/auditd.conf

# Будет добавлен файл с правилами аудита `/etc/audit/rules.d/ziem.rules`.

echo "# Registration and audit of information security events


## Audit access to password and group files, as well as the consequences of their changes

-w /etc/group -p wa -F auid!=4294967295 -k sysobj_access
-w /etc/passwd -p wa -F auid!=4294967295 -k sysobj_access
-w /etc/shadow -F auid!=4294967295 -k sysobj_access
-w /etc/login.defs -p wa -F auid!=4294967295 -k sysobj_access
-w /etc/securetty -F auid!=4294967295 -k sysobj_access
-w /etc/sudoers  -p wa -F auid!=4294967295 -k sysobj_access


## Track access to system directories

-w /boot/ -p wa -k system_obj_modification
-w /bin/ -p wa -k system_obj_modification
-w /sbin/ -p wa -k system_obj_modification
-w /usr/bin/ -p wa -k system_obj_modification
-w /usr/sbin/ -p wa -k system_obj_modification


## Monitor access to the system event scheduler

-w /etc/cron.allow -p wa -k cron
-w /etc/cron.deny -p wa -k cron
-w /etc/cron.d/ -p wa -k cron
-w /etc/cron.daily/ -p wa -k cron
-w /etc/cron.hourly/ -p wa -k cron
-w /etc/cron.monthly/ -p wa -k cron
-w /etc/cron.weekly/ -p wa -k cron
-w /etc/crontab -p wa -k cron
-w /var/spool/cron/crontabs/ -k cron


## Monitor access to general operating system security settings

-w /etc/hosts -p wa -F auid!=4294967295 -k sysobj_access
-w /etc/sysctl.conf -p wa -F auid!=4294967295 -k sysobj_access
-w /etc/ssh/sshd_config -F auid!=4294967295 -k sysobj_access
-w /etc/localtime -p wa -F auid!=4294967295 -k time-change
-a exit,always -F arch=b32 -S adjtimex -S settimeofday -S stime -S clock_settime -F uid!=ntp -F auid!=4294967295 -k time-change
-a exit,always -F arch=b64 -S adjtimex -S settimeofday -S clock_settime -F uid!=ntp -F auid!=4294967295 -k time-change
-a exit,always -F arch=b32 -S mknod -S mount -S umount -S umount2 -S ptrace -F auid!=4294967295 -k mount
-a exit,always -F arch=b64 -S mknod -S mount -S umount2 -S ptrace -F auid!=4294967295 -k mount


## Monitor usage of the privilege escalation mechanism

w /bin/su -p x -k priv_esc
-w /usr/bin/sudo -p x -k priv_esc
-w /etc/sudoers -p rw -k priv_esc


## Monitor shutdown and restart operations

-w /sbin/shutdown -p x -k power
-w /sbin/poweroff -p x -k power
-w /sbin/reboot -p x -k power
-w /sbin/halt -p x -k power


## Track changes to audit settings

-w /etc/audit/auditd.conf -p wa -F auid!=4294967295 -k audit_change
-w /etc/audit/audit.rules -p wa -F auid!=4294967295 -k audit_change
-w /etc/libaudit.conf -p wa -F auid!=4294967295 -k audit_change
-w /etc/audisp/plugins.d/syslog.conf -F auid!=4294967295 -k audit_change
-w /etc/audisp/audispd.conf -F auid!=4294967295 -k audit_change
-w /etc/rsyslog.conf -F auid!=4294967295 -k audit_change
-w /etc/init.d/auditd -p wa -F auid!=4294967295 -k audit_change

" > /etc/audit/rules.d/ziem.rules

# Будет добавлен файл с инструкцией отправки Syslog `/etc/syslog-ng/conf.d/ziem.conf`.

echo "destination d_ziem {
    udp(\"$ip_address_ziem\" port(514));
};

log {
    source(s_src); 
    destination(d_ziem);
};" > /etc/syslog-ng/conf.d/ziem.conf

# Будут перезапущены службы `auditd` и `syslog-ng`.

systemctl restart auditd
systemctl restart syslog-ng