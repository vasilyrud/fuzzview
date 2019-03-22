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

    // Test conditional branches
    if (a == 4) {
        // Test indirect function calls
        b();
    } else {
        B();
    }

    // Test switch statements
    switch (a) {
        case 7:
            C();
            break;
        default:
            // Test multiple calls per block
            D();
            D();
            break;
    }
}


int main() {
    A(6);

    return 0;
}
