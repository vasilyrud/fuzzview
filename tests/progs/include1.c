#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>

#include "common.h"
#include "subA/common.h"
#include "subB/common.h"


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

    switch (a) {
        case 1:
            C();
            break;
        case 2:
            D();
            break;
        default:
            write(1, NULL, 0);
            break;
    }

    return 10;
}


void foo(int *a) {
    if (a)
        *a = 0;
}


int main() {
    int (*c)(void) = &C;
    int (*d)(void) = &D;

    A(6);
    Z();
    ZA();
    ZB();

    foo(NULL);

    return 0;
}
