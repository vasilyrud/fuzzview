CC = python3 $(FV_DIR)/fv-compiler.py

CFLAGS = -Wall
CFLAGS += -Wno-unused-variable
# CFLAGS += -fsanitize-coverage=edge,trace-pc-guard

LDFLAGS = -Wall
LDFLAGS += -Wno-unused-variable
# LDFLAGS += -fsanitize=address

BIN = bin
# SANCOV = $(FV_DIR)/rt/sancov.c

PROGS = include1 loops1 branches1
ALL_FILES = $(PROGS) common subA/common subB/common
ALL_FILES_BC = $(ALL_FILES:=.bc)

all: $(ALL_FILES_O) $(ALL_FILES_BC) $(PROGS)

%.bc: %.c
	$(CC) $(CFLAGS) -emit-llvm -c $< -o $@

%%/%.bc: %%/%.c
	$(CC) $(CFLAGS) -emit-llvm -c $< -o $@

include1: include1.bc
	# $(CC) $(LDFLAGS) $(SANCOV) $< common.bc subA/common.bc subB/common.bc -o $(BIN)/$@
	$(CC) $(LDFLAGS) $< common.bc subA/common.bc subB/common.bc -o $(BIN)/$@

loops1: loops1.bc
	$(CC) $(LDFLAGS) $< -o $(BIN)/$@

branches1: branches1.bc
	$(CC) $(LDFLAGS) $< -o $(BIN)/$@

clean:
	rm ./*.o 2>/dev/null || true
	rm ./*.bc 2>/dev/null || true
	rm ./*.bc-* 2>/dev/null || true
	rm ./*.bc.tmp 2>/dev/null || true
	rm ./*.cfg.json 2>/dev/null || true
	rm ./*.cfg.dot 2>/dev/null || true
	rm ./*.cfg.pdf 2>/dev/null || true
	rm ./*.cfg.png 2>/dev/null || true
	
	rm ./**/*.o 2>/dev/null || true
	rm ./**/*.bc 2>/dev/null || true
	rm ./**/*.bc-* 2>/dev/null || true
	rm ./**/*.bc.tmp 2>/dev/null || true
	rm ./**/*.cfg.json 2>/dev/null || true
	rm ./**/*.cfg.dot 2>/dev/null || true
	rm ./**/*.cfg.pdf 2>/dev/null || true
	rm ./**/*.cfg.png 2>/dev/null || true
	
	rm -r bin/* 2>/dev/null || true
