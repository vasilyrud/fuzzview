# A modern version of clang is needed
# to build the examples.
CC = clang

CFLAGS = -O0 -Wall -g
# CFLAGS += -fsanitize-coverage=edge,trace-pc-guard
CFLAGS += -Wno-nullability-completeness
CFLAGS += -Wno-unused-variable
CFLAGS += -Xclang
CFLAGS += -load
CFLAGS += -Xclang
CFLAGS += ../pass/build/fvpass/libFvPass.so

LDFLAGS = -O0 -Wall -g
# LDFLAGS += -fsanitize=address
LDFLAGS += -Wno-nullability-completeness
LDFLAGS += -Wno-unused-variable

BIN = bin
SANCOV = ../rt/sancov.c

PROGS = simple_1
ALL_FILES = $(PROGS) common subA/common subB/common
ALL_FILES_BC = $(ALL_FILES:=.bc)

all: $(ALL_FILES_O) $(ALL_FILES_BC) $(PROGS)

%.bc: %.c
	$(CC) $(CFLAGS) -emit-llvm -c $< -o $@

%%/%.bc: %%/%.c
	$(CC) $(CFLAGS) -emit-llvm -c $< -o $@

simple_1: simple_1.bc
	$(CC) $(LDFLAGS) $< common.bc subA/common.bc subB/common.bc -o $(BIN)/$@

clean:
	rm ./*.o || true
	rm ./*.bc || true
	
	rm ./**/*.o || true
	rm ./**/*.bc || true
	
	rm -r bin/* || true
