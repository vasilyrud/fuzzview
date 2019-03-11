#include <stdint.h>
#include <stdio.h>
#include <sanitizer/coverage_interface.h>

#define __FV_CUR_FUNC 0
#define __FV_DESCRIPTION_BUF_SIZE 1024

static uint64_t __fv_num_blocks;

extern void __sanitizer_cov_trace_pc_guard_init(uint32_t *start, uint32_t *stop) {

    // Initialize only once.
    if (start == stop || *start) return;

    printf("INIT: start addr: %p, stop addr: %p\n", start, stop);

    uint64_t counter = 1;
    
    for (uint32_t *iter = start; iter < stop; iter++) {
        *iter = counter++;
    }

    __fv_num_blocks = counter - 1;

    printf("INIT: # of blocks: %llu\n", __fv_num_blocks);
}

extern void __sanitizer_cov_trace_pc_guard(uint32_t *guard) {

    void *ret_pc = __builtin_return_address(__FV_CUR_FUNC);

    char pc_description[__FV_DESCRIPTION_BUF_SIZE];
    __sanitizer_symbolize_pc(ret_pc, "%p %F %L", pc_description, sizeof(pc_description));

    printf("guard addr: %p, guard value: %u, PC description: %s\n", guard, *guard, pc_description);


}
