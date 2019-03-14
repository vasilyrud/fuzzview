#include <stdio.h>
#include <string.h>
#include <stdarg.h>
#include <errno.h>
#include <stdlib.h>
#include <unistd.h>


int B() {
    return 11;
}


int C() {
    return 12;
}


int D() {
    return 13;
}


void A(int a) {
    int (*b)(void) = &B;

    if (a == 4) {
        b();
    } else {
        B();
    }

    switch (a) {
        case 7:
            C();
            break;
        default:
            D();
            D();
            break;
    }
}


int main() {
    A(6);

    return 0;
}
