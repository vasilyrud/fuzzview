
#include "common.h"

static int Y() {
    printf("__FILE__: %s\n", __FILE__);
    return 123;
}

int ZA() {
    Y();
    return 222;
}
