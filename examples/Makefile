# Some modern version of clang is mandatory
# for building the examples.
CC = clang

CFLAGS = -O0 -Wall -g
CFLAGS += -Wno-nullability-completeness
CFLAGS += -Wno-unused-variable

BIN = bin

PROGS = simple_1
ALL_FILES = $(PROGS) common
ALL_FILES_BC = $(ALL_FILES:=.bc)

all: $(ALL_FILES_O) $(ALL_FILES_BC) $(PROGS)

%.bc: %.c
	$(CC) $(CFLAGS) -emit-llvm -c $< -o $@

simple_1: simple_1.bc
	$(CC) $(CFLAGS) $< common.bc -o $(BIN)/$@

clean:
	rm *.o || true
	rm *.bc || true
	rm -r bin/* || true
