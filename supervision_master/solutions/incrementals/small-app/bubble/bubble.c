/* Aim: Write a C program to sort array of random numbers using bubble sort and rand() function */

// Execution command: ./bubble 1000-10000-100000
// ./bubble {SIZE1-SIZE2-SIZE3} {SLEEP} {REPEAT}

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <string.h>


// generate_random() function to generate array of random numbers
void generate_random(int *a,int n)
{
	int i;
	for(i=0;i<n;i++)
	a[i]=rand()%n;
}
void display_arr(int *a,int n)
{
	int i;
	for(i=0;i<n;i++)
		printf(" %d ",a[i]);
}
void bubble_short(int *a,int n)
{
	int i,j,temp;
	for(i=1;i<n;i++)
	{
		for(j=0;j<n-i;j++)
		{
			/* To sort in ascending order, change '<' to '>' to implement descending order sorting */
			if(a[j+1]<a[j]) 
			{
				temp=a[j];
				a[j]=a[j+1];
				a[j+1]=temp; 
			}
		}
	}
}
int main(int argc, char* argv[])
{
	printf("BEGIN ---\n");
	// printf("%d \n",argc);
	sleep(1);
	int n,i;
	if (argc > 1)
   {
		// Extract the first token
    	char * token = strtok(argv[1], "-");
    	// loop through the string to extract all other tokens
    	while( token != NULL ) {
        	printf( "OPTION: %s\n", token ); //printing each token
			n = atoi(token);
			int a[n];
			
			// Passing starting address and size to generate array of random numbers
			generate_random(a,n); 
			// Displaying the random array
			printf("\n The random array: ");
			display_arr(a,n);

			bubble_short(a,n);
		
			// Displaying the sorted array.
			printf("\n The sorted array: ");
			display_arr(a,n);
			printf("\n \n");

         	token = strtok(NULL, "-");
    	}
   }

	printf("END ---\n");
	sleep(1);
    return (EXIT_SUCCESS);
}
