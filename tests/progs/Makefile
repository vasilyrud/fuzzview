CC = $(LLVM_HOME)/bin/clang

CFLAGS = -O0 -Wall -g
# CFLAGS += -fsanitize-coverage=edge,trace-pc-guard
CFLAGS += -Wno-nullability-completeness
CFLAGS += -Wno-unused-variable
CFLAGS += -Xclang
CFLAGS += -load
CFLAGS += -Xclang
CFLAGS += $(FUZZVIEW_DIR)/pass/build/fvpass/libFvPass.so

LDFLAGS = -O0 -Wall -g
# LDFLAGS += -fsanitize=address
LDFLAGS += -Wno-nullability-completeness
LDFLAGS += -Wno-unused-variable

BIN = bin
# SANCOV = $(FUZZVIEW_DIR)/rt/sancov.c

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
	rm ./*.o || true
	rm ./*.bc || true
	rm ./*.cfg.json || true
	rm ./*.cfg.dot || true
	rm ./*.cfg.pdf || true
	
	rm ./**/*.o || true
	rm ./**/*.bc || true
	rm ./**/*.cfg.json || true
	rm ./**/*.cfg.dot || true
	rm ./**/*.cfg.pdf || true
	
	rm -r bin/* || true
