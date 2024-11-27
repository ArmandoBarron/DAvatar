// file main.c
#include <stdio.h> // for printf()
#include <stdlib.h> // for atoi())
#include "fib.h" // for fib()

int main(int argc, char* argv[]) {
    int n = atoi(argv[1]);
    printf("%f", fib(n));
}