/* Aim: Write a C program to sort array of random numbers using bubble sort and rand() function */
// Compile command: gcc -pthread -o bubble bubble.c
// Execution command: ./bubble 1000-10000-100000
// ./bubble {SIZE1-SIZE2-SIZE3} {SLEEP} {REPEAT}

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <unistd.h>
#include <string.h>
#include <pthread.h>
#define NUM_THREADS 3


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
void *PrintHello(void *threadid)
{
   long tid;
   tid = (long)threadid;
   printf("Hello World! It's me, thread #%ld!\n", tid);
   pthread_exit(NULL);
}

struct thread_data{
   int  thread_id;
   int  array_size;
};
struct thread_data thread_data_array[NUM_THREADS];

void *BubbleShort(void *threadarg)
{
	struct thread_data *my_data;
	int taskid,array_size;
	my_data = (struct thread_data *) threadarg;
	taskid = my_data->thread_id;
	array_size = my_data->array_size;
	int a[array_size];
	printf("Bubble short, thread #%d!, array_size %d\n", taskid, array_size);

   	// Passing starting address and size to generate array of random numbers
	generate_random(a,array_size); 
	// Displaying the random array
	printf("\n The random array: ");
	display_arr(a,array_size);
	bubble_short(a,array_size);
	// Displaying the sorted array.
	printf("\n The sorted array: ");
	display_arr(a,array_size);
	printf("\n \n");

	printf("Finish, thread #%d!, array_size %d\n", taskid, array_size);
	pthread_exit(NULL);
}



int main(int argc, char* argv[])
{
	if (argc > 1)
	{
		printf("BEGIN ---\n");
		sleep(1);

		pthread_t threads[NUM_THREADS];
		int t, taskids[NUM_THREADS];

		int n,i,rc[NUM_THREADS];
		// Extract the first token
		char * token = strtok(argv[1], "-");
		t=0;
		// loop through the string to extract all other tokens
		while( token != NULL ) {
			printf( "OPTION: %s\n", token ); //printing each token
			n = atoi(token);

			taskids[t] = t;
			thread_data_array[t].thread_id = t;
			thread_data_array[t].array_size = n;
			printf("Creating thread %d\n", t);
			// rc[t] = pthread_create(&threads[t], NULL, PrintHello, (void *)taskids[t]);
			rc[t] = pthread_create(&threads[t], NULL, BubbleShort, (void *)&thread_data_array[t]);
			if (rc[t]){
				printf("ERROR; return code from pthread_create() is %d\n", rc[t]);
				exit(-1);
			}

		 	token = strtok(NULL, "-");
			t++;
		}
		for (int i = 0; i < NUM_THREADS; i++)
		{
			(void) pthread_join(threads[i], NULL);
		}
		
		sleep(1);
		printf("END ---\n");
	}
	else
	{
		printf("No arguments: %d\n",argc);
	}
	
	return (EXIT_SUCCESS);
}
