#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>


int A() {
    return 10;
}


int B() {
    return 11;
}


int C() {
    return 12;
}


int D() {
    return 13;
}


int main() {

    // Test nested SCCs
    while (1) {
        A();
        while (1) {
            if (B()) break;
        }
        if (C()) break;
    }

    // Test two back edges to start
    z:
    if (A()) {
        if (B()) {
            goto z;
        } else {
            if (C()) {
                goto z;
            }
        }
    }

    // Test irreducible SCC
    if (A()) {
        x:
        if (B()) {
            goto y;
        }
    } else {
        y:
        if (C()) {
            goto x;
        }
    }

    return 0;
}
