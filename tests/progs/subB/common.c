
#include "common.h"

static int Y() {
    printf("__FILE__: %s\n", __FILE__);
    return 456;
}

int ZB() {
    Y();
    return 333;
}
