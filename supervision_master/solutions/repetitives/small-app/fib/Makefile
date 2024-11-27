# file Makefile

CC=clang
CFLAGS=-Wall

fib: main.o fib.o
	$(CC) $(CFLAGS) -o fib main.o fib.o

main.o: main.c fib.h
	$(CC) $(CFAGS) -c main.c

fib.o: fib.c
	$(CC) $(CFLAGS) -c fib.c

clean:
	rm -f *.o
