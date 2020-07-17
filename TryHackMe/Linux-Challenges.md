## Find the difference between two script files to find flag 13.
use `diff`
## MOTD
`/etc/update-motd`
## find information about the system, such as the kernel version etc.
`cat /etc/*release`
## Flag 16 lies within another system mount.
```console
bob@ip-10-10-90-207:~/flag13$ cat /proc/mounts
sysfs /sys sysfs rw,nosuid,nodev,noexec,relatime 0 0
proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0
udev /dev devtmpfs rw,nosuid,relatime,size=497280k,nr_inodes=124320,mode=755 0 0
devpts /dev/pts devpts rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000 0 0
tmpfs /run tmpfs rw,nosuid,noexec,relatime,size=101444k,mode=755 0 0
/dev/xvda1 / ext4 rw,relatime,discard,data=ordered 0 0
securityfs /sys/kernel/security securityfs rw,nosuid,nodev,noexec,relatime 0 0
tmpfs /dev/shm tmpfs rw,nosuid,nodev 0 0
tmpfs /run/lock tmpfs rw,nosuid,nodev,noexec,relatime,size=5120k 0 0
tmpfs /sys/fs/cgroup tmpfs ro,nosuid,nodev,noexec,mode=755 0 0
cgroup /sys/fs/cgroup/systemd cgroup rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/lib/systemd/systemd-cgroups-agent,name=systemd 0 0
pstore /sys/fs/pstore pstore rw,nosuid,nodev,noexec,relatime 0 0
cgroup /sys/fs/cgroup/perf_event cgroup rw,nosuid,nodev,noexec,relatime,perf_event 0 0
cgroup /sys/fs/cgroup/net_cls,net_prio cgroup rw,nosuid,nodev,noexec,relatime,net_cls,net_prio 0 0
cgroup /sys/fs/cgroup/blkio cgroup rw,nosuid,nodev,noexec,relatime,blkio 0 0
cgroup /sys/fs/cgroup/pids cgroup rw,nosuid,nodev,noexec,relatime,pids 0 0
cgroup /sys/fs/cgroup/freezer cgroup rw,nosuid,nodev,noexec,relatime,freezer 0 0
cgroup /sys/fs/cgroup/devices cgroup rw,nosuid,nodev,noexec,relatime,devices 0 0
cgroup /sys/fs/cgroup/cpuset cgroup rw,nosuid,nodev,noexec,relatime,cpuset 0 0
cgroup /sys/fs/cgroup/hugetlb cgroup rw,nosuid,nodev,noexec,relatime,hugetlb 0 0
cgroup /sys/fs/cgroup/cpu,cpuacct cgroup rw,nosuid,nodev,noexec,relatime,cpu,cpuacct 0 0
cgroup /sys/fs/cgroup/memory cgroup rw,nosuid,nodev,noexec,relatime,memory 0 0
systemd-1 /proc/sys/fs/binfmt_misc autofs rw,relatime,fd=31,pgrp=1,timeout=0,minproto=5,maxproto=5,direct 0 0
debugfs /sys/kernel/debug debugfs rw,relatime 0 0
mqueue /dev/mqueue mqueue rw,relatime 0 0
hugetlbfs /dev/hugepages hugetlbfs rw,relatime 0 0
fusectl /sys/fs/fuse/connections fusectl rw,relatime 0 0
/dev/loop0 /snap/core/5742 squashfs ro,nodev,relatime 0 0
/dev/loop1 /snap/amazon-ssm-agent/784 squashfs ro,nodev,relatime 0 0
/dev/loop2 /snap/amazon-ssm-agent/930 squashfs ro,nodev,relatime 0 0
/dev/loop3 /snap/core/6405 squashfs ro,nodev,relatime 0 0
/dev/loop4 /snap/amazon-ssm-agent/1068 squashfs ro,nodev,relatime 0 0
lxcfs /var/lib/lxcfs fuse.lxcfs rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other 0 0
tmpfs /run/user/126 tmpfs rw,nosuid,nodev,relatime,size=101444k,mode=700,uid=126,gid=131 0 0
tmpfs /run/user/1004 tmpfs rw,nosuid,nodev,relatime,size=101444k,mode=700,uid=1004,gid=1006 0 0
binfmt_misc /proc/sys/fs/binfmt_misc binfmt_misc rw,relatime 0 0
bob@ip-10-10-90-207:~/flag13$ mount
sysfs on /sys type sysfs (rw,nosuid,nodev,noexec,relatime)
proc on /proc type proc (rw,nosuid,nodev,noexec,relatime)
udev on /dev type devtmpfs (rw,nosuid,relatime,size=497280k,nr_inodes=124320,mode=755)
devpts on /dev/pts type devpts (rw,nosuid,noexec,relatime,gid=5,mode=620,ptmxmode=000)
tmpfs on /run type tmpfs (rw,nosuid,noexec,relatime,size=101444k,mode=755)
/dev/xvda1 on / type ext4 (rw,relatime,discard,data=ordered)
securityfs on /sys/kernel/security type securityfs (rw,nosuid,nodev,noexec,relatime)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
tmpfs on /run/lock type tmpfs (rw,nosuid,nodev,noexec,relatime,size=5120k)
tmpfs on /sys/fs/cgroup type tmpfs (ro,nosuid,nodev,noexec,mode=755)
cgroup on /sys/fs/cgroup/systemd type cgroup (rw,nosuid,nodev,noexec,relatime,xattr,release_agent=/lib/systemd/systemd-cgroups-agent,name=systemd)
pstore on /sys/fs/pstore type pstore (rw,nosuid,nodev,noexec,relatime)
cgroup on /sys/fs/cgroup/perf_event type cgroup (rw,nosuid,nodev,noexec,relatime,perf_event)
cgroup on /sys/fs/cgroup/net_cls,net_prio type cgroup (rw,nosuid,nodev,noexec,relatime,net_cls,net_prio)
cgroup on /sys/fs/cgroup/blkio type cgroup (rw,nosuid,nodev,noexec,relatime,blkio)
cgroup on /sys/fs/cgroup/pids type cgroup (rw,nosuid,nodev,noexec,relatime,pids)
cgroup on /sys/fs/cgroup/freezer type cgroup (rw,nosuid,nodev,noexec,relatime,freezer)
cgroup on /sys/fs/cgroup/devices type cgroup (rw,nosuid,nodev,noexec,relatime,devices)
cgroup on /sys/fs/cgroup/cpuset type cgroup (rw,nosuid,nodev,noexec,relatime,cpuset)
cgroup on /sys/fs/cgroup/hugetlb type cgroup (rw,nosuid,nodev,noexec,relatime,hugetlb)
cgroup on /sys/fs/cgroup/cpu,cpuacct type cgroup (rw,nosuid,nodev,noexec,relatime,cpu,cpuacct)
cgroup on /sys/fs/cgroup/memory type cgroup (rw,nosuid,nodev,noexec,relatime,memory)
systemd-1 on /proc/sys/fs/binfmt_misc type autofs (rw,relatime,fd=31,pgrp=1,timeout=0,minproto=5,maxproto=5,direct)
debugfs on /sys/kernel/debug type debugfs (rw,relatime)
mqueue on /dev/mqueue type mqueue (rw,relatime)
hugetlbfs on /dev/hugepages type hugetlbfs (rw,relatime)
fusectl on /sys/fs/fuse/connections type fusectl (rw,relatime)
/var/lib/snapd/snaps/core_5742.snap on /snap/core/5742 type squashfs (ro,nodev,relatime)
/var/lib/snapd/snaps/amazon-ssm-agent_784.snap on /snap/amazon-ssm-agent/784 type squashfs (ro,nodev,relatime)
/var/lib/snapd/snaps/amazon-ssm-agent_930.snap on /snap/amazon-ssm-agent/930 type squashfs (ro,nodev,relatime)
/var/lib/snapd/snaps/core_6405.snap on /snap/core/6405 type squashfs (ro,nodev,relatime)
/var/lib/snapd/snaps/amazon-ssm-agent_1068.snap on /snap/amazon-ssm-agent/1068 type squashfs (ro,nodev,relatime)
lxcfs on /var/lib/lxcfs type fuse.lxcfs (rw,nosuid,nodev,relatime,user_id=0,group_id=0,allow_other)
tmpfs on /run/user/126 type tmpfs (rw,nosuid,nodev,relatime,size=101444k,mode=700,uid=126,gid=131)
tmpfs on /run/user/1004 type tmpfs (rw,nosuid,nodev,relatime,size=101444k,mode=700,uid=1004,gid=1006)
binfmt_misc on /proc/sys/fs/binfmt_misc type binfmt_misc (rw,relatime)
bob@ip-10-10-90-207:~/flag13$ df -ath
df: no file systems processed
bob@ip-10-10-90-207:~/flag13$ df -aTh
Filesystem     Type         Size  Used Avail Use% Mounted on
sysfs          sysfs           0     0     0    - /sys
proc           proc            0     0     0    - /proc
udev           devtmpfs     486M     0  486M   0% /dev
devpts         devpts          0     0     0    - /dev/pts
tmpfs          tmpfs        100M  4.7M   95M   5% /run
/dev/xvda1     ext4         7.7G  4.2G  3.6G  55% /
securityfs     securityfs      0     0     0    - /sys/kernel/security
tmpfs          tmpfs        496M  108K  496M   1% /dev/shm
tmpfs          tmpfs        5.0M     0  5.0M   0% /run/lock
tmpfs          tmpfs        496M     0  496M   0% /sys/fs/cgroup
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/systemd
pstore         pstore          0     0     0    - /sys/fs/pstore
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/perf_event
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/net_cls,net_prio
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/blkio
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/pids
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/freezer
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/devices
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/cpuset
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/hugetlb
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/cpu,cpuacct
cgroup         cgroup          0     0     0    - /sys/fs/cgroup/memory
systemd-1      -               -     -     -    - /proc/sys/fs/binfmt_misc
debugfs        debugfs         0     0     0    - /sys/kernel/debug
mqueue         mqueue          0     0     0    - /dev/mqueue
hugetlbfs      hugetlbfs       0     0     0    - /dev/hugepages
fusectl        fusectl         0     0     0    - /sys/fs/fuse/connections
/dev/loop0     squashfs      88M   88M     0 100% /snap/core/5742
/dev/loop1     squashfs      17M   17M     0 100% /snap/amazon-ssm-agent/784
/dev/loop2     squashfs      18M   18M     0 100% /snap/amazon-ssm-agent/930
/dev/loop3     squashfs      91M   91M     0 100% /snap/core/6405
/dev/loop4     squashfs      18M   18M     0 100% /snap/amazon-ssm-agent/1068
lxcfs          fuse.lxcfs      0     0     0    - /var/lib/lxcfs
tmpfs          tmpfs        100M   16K  100M   1% /run/user/126
tmpfs          tmpfs        100M     0  100M   0% /run/user/1004
binfmt_misc    binfmt_misc     0     0     0    - /proc/sys/fs/binfmt_misc
bob@ip-10-10-90-207:~/flag13$ find mnt
find: ‘mnt’: No such file or directory
bob@ip-10-10-90-207:~/flag13$ findmnt
TARGET                                SOURCE      FSTYPE   OPTIONS
/                                     /dev/xvda1  ext4     rw,relatime,discard,data=ordered
├─/sys                                sysfs       sysfs    rw,nosuid,nodev,noexec,relatime
│ ├─/sys/kernel/security              securityfs  security rw,nosuid,nodev,noexec,relatime
│ ├─/sys/fs/cgroup                    tmpfs       tmpfs    ro,nosuid,nodev,noexec,mode=755
│ │ ├─/sys/fs/cgroup/systemd          cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,xattr,re
│ │ ├─/sys/fs/cgroup/perf_event       cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,perf_eve
│ │ ├─/sys/fs/cgroup/net_cls,net_prio cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,net_cls,
│ │ ├─/sys/fs/cgroup/blkio            cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,blkio
│ │ ├─/sys/fs/cgroup/pids             cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,pids
│ │ ├─/sys/fs/cgroup/freezer          cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,freezer
│ │ ├─/sys/fs/cgroup/devices          cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,devices
│ │ ├─/sys/fs/cgroup/cpuset           cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,cpuset
│ │ ├─/sys/fs/cgroup/hugetlb          cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,hugetlb
│ │ ├─/sys/fs/cgroup/cpu,cpuacct      cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,cpu,cpua
│ │ └─/sys/fs/cgroup/memory           cgroup      cgroup   rw,nosuid,nodev,noexec,relatime,memory
│ ├─/sys/fs/pstore                    pstore      pstore   rw,nosuid,nodev,noexec,relatime
│ ├─/sys/kernel/debug                 debugfs     debugfs  rw,relatime
│ └─/sys/fs/fuse/connections          fusectl     fusectl  rw,relatime
├─/proc                               proc        proc     rw,nosuid,nodev,noexec,relatime
│ └─/proc/sys/fs/binfmt_misc          systemd-1   autofs   rw,relatime,fd=31,pgrp=1,timeout=0,minpr
│   └─/proc/sys/fs/binfmt_misc        binfmt_misc binfmt_m rw,relatime
├─/dev                                udev        devtmpfs rw,nosuid,relatime,size=497280k,nr_inode
│ ├─/dev/pts                          devpts      devpts   rw,nosuid,noexec,relatime,gid=5,mode=620
│ ├─/dev/shm                          tmpfs       tmpfs    rw,nosuid,nodev
│ ├─/dev/mqueue                       mqueue      mqueue   rw,relatime
│ └─/dev/hugepages                    hugetlbfs   hugetlbf rw,relatime
├─/run                                tmpfs       tmpfs    rw,nosuid,noexec,relatime,size=101444k,m
│ ├─/run/lock                         tmpfs       tmpfs    rw,nosuid,nodev,noexec,relatime,size=512
│ ├─/run/user/1004                    tmpfs       tmpfs    rw,nosuid,nodev,relatime,size=101444k,mo
│ └─/run/user/126                     tmpfs       tmpfs    rw,nosuid,nodev,relatime,size=101444k,mo
├─/snap/core/5742                     /dev/loop0  squashfs ro,nodev,relatime
├─/snap/amazon-ssm-agent/784          /dev/loop1  squashfs ro,nodev,relatime
├─/snap/amazon-ssm-agent/930          /dev/loop2  squashfs ro,nodev,relatime
├─/snap/core/6405                     /dev/loop3  squashfs ro,nodev,relatime
├─/snap/amazon-ssm-agent/1068         /dev/loop4  squashfs ro,nodev,relatime
└─/var/lib/lxcfs                      lxcfs       fuse.lxc rw,nosuid,nodev,relatime,user_id=0,group
bob@ip-10-10-90-207:~/flag13$ ls /m
media/ mnt/   
bob@ip-10-10-90-207:~/flag13$ ls /mnt/
bob@ip-10-10-90-207:~/flag13$ ls
script1  script2
bob@ip-10-10-90-207:~/flag13$ ls /media/
f
bob@ip-10-10-90-207:~/flag13$ ls
script1  script2
bob@ip-10-10-90-207:~/flag13$ ls /media/f/l/a/g/1/6/is/cab4b7cae33c87794d82efa1e7f834e6/
```
## Read the 2345th line of the file that contains flag 19.
```console
alice@ip-10-10-90-207:~$ cat -n flag19 | grep 2345
```
## Display a File in Reverse on Linux
- `tac` reverse line
- ```cat file | rev``` reverse string

## kernel version
```uname -r```
