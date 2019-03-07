#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>

#include "common.h"


int B() {
    write(1, NULL, 0);

    return 11;
}


int C() {
    B();

    return 12;
}

int D() {
    write(1, NULL, 0);

    return 13;
}


int A(int a) {
    int (*b)(void) = &B;

    if (a == 4) {
        write(1, NULL, 0);
    } else if (a == 5) {
        write(1, NULL, 0);
    } else if (a == 6) {
        b();
    } else if (a == 7) {
        b();
    } else {
        D();
    }

    return 10;
}


int main() {
    int (*c)(void) = &C;
    int (*d)(void) = &D;

    A(6);
    Z();

    return 0;
}
