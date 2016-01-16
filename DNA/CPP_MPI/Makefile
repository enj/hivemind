EXEC = preprocessing
all: $(EXEC) 
CC = mpic++

CXXFLAGS += -O0 -g -c -DCXXCODE
LDFLAGS = preprocessing.o pipeline.o config.o

PRINT_COMMANDS=n
ifeq ($(PRINT_COMMANDS),y)
CXXFLAGS += -DPRINT_COMMANDS
endif

$(EXEC) : preprocessing.o pipeline.o config.o Makefile pipeline.h preprocessing.h config.h
	$(CC) $(LDFLAGS) -o preprocessing

preprocessing.o : preprocessing.cxx preprocessing.h Makefile
	$(CC) $(CXXFLAGS) preprocessing.cxx -o preprocessing.o

pipeline.o : pipeline.cxx pipeline.h Makefile
	$(CC) $(CXXFLAGS) pipeline.cxx -o pipeline.o

config.o : config.cxx config.h Makefile
	$(CC) $(CXXFLAGS) config.cxx -o config.o


clean:
	rm *o preprocessing
