#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[]) {
   // printf("%d \n",argc);
   if (argc > 1)
   {
      // char string[50] = "Hello! We are learning about strtok";
      // Extract the first token
      char * token = strtok(argv[1], "-");
      // printf("  %s \n", token);
      // loop through the string to extract all other tokens
      while( token != NULL ) {
         printf( " %s\n", token ); //printing each token
         token = strtok(NULL, "-");
      }
   }
   
   return (EXIT_SUCCESS);
}