EXEC = preprocessing
#CONFIG = ccis4301#config
CONFIG = config
all: $(EXEC) 
CC = mpicxx

CXXFLAGS += -O0 -g -c -DCXXCODE
LDFLAGS = preprocessing.o pipeline.o $(CONFIG).o

PRINT_COMMANDS=n
ifeq ($(PRINT_COMMANDS),y)
CXXFLAGS += -DPRINT_COMMANDS
endif

$(EXEC) : preprocessing.o pipeline.o $(CONFIG).o Makefile pipeline.h preprocessing.h $(CONFIG).h
	$(CC) $(LDFLAGS) -o preprocessing

preprocessing.o : preprocessing.cxx preprocessing.h Makefile
	$(CC) $(CXXFLAGS) preprocessing.cxx -o preprocessing.o

pipeline.o : pipeline.cxx pipeline.h Makefile
	$(CC) $(CXXFLAGS) pipeline.cxx -o pipeline.o

$(CONFIG).o : $(CONFIG).cxx $(CONFIG).h Makefile
	$(CC) $(CXXFLAGS) $(CONFIG).cxx -o $(CONFIG).o


clean:
	rm *o preprocessing
