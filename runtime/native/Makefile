CC=gcc
CFLAGS=-Wall -O3

all: aayu-runtime

aayu-runtime: main.o loader.o vm.o
	$(CC) $(CFLAGS) -o aayu-runtime main.o loader.o vm.o

main.o: main.c
	$(CC) $(CFLAGS) -c main.c

loader.o: loader.c loader.h
	$(CC) $(CFLAGS) -c loader.c

vm.o: vm.c vm.h
	$(CC) $(CFLAGS) -c vm.c

clean:
	rm -f *.o aayu-runtime aayu-runtime.exe
