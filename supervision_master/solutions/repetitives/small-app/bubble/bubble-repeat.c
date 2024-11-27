/* Aim: Write a C program to sort array of random numbers using bubble sort and rand() function */

// Execution command: ./bubble 10000 2 10
// ./bubble {SIZE} {SLEEP} {REPEAT}

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
	sleep(10);
	int n,t,rep,r,i,slp;
	if (argc > 1)
  {
	
    n = atoi(argv[1]);
    t = atoi(argv[2]);
    rep = atoi(argv[3]);
    int a[n];
	printf("\n Enter size of array:- ");
	scanf("%d",&n);

	if (rep == 0)
	{
		while (true)
		{
			slp = rand()%t;
			printf("Sleeping for %d second.\n", slp);
			for (i = 0; i < slp; i++)
			{
				printf("%d ", i);
				sleep(1);
			}

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

		}
	}else
	{
		r = rep;
		while (r>=0)
		{
			slp = rand()%t;
			printf("Sleeping for %d second.\n", slp);
			for (i = 0; i < slp; i++)
			{
				printf("%d ", i);
				sleep(1);
			}

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
			r--;
		}
	}



	}
	printf("END ---\n");
    return (EXIT_SUCCESS);
}