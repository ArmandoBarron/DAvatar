#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>   
#include <libgen.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/time.h> 
#include <sys/ipc.h>
#include <dirent.h>
#include "Kulla-Libraries/Kulla.h"

/**
 * Structures declaration
 * You can add aditional attributes to the threads
 * */
struct thread_data {
	int workerId;
	char **listNames;
	char *sourcePath;
	char *sinkPath;
	int numberOfFiles;
	int numberOfWorkers;
};


/**
 * @brief Function that invokes a worker
 * @details Each thread invokes a socket client that
 * comunicates with one worker to do the solicitated 
 * work
 * 
 * @param threadarg Struct with the thread data
 */
void *sendWork2Worker(void *threadarg){

	struct thread_data *my_data;
	my_data = (struct thread_data *) threadarg;
	char logMessage[256];
	char logName[256];
	sprintf(logName, "Logs/Worker_%i.log", my_data->workerId);
	sprintf(logMessage, "echo 'Worker :%i'  >> %s",  my_data->workerId, logName);
	system(logMessage);
	/* Cambia este hilo por el balanceador de carga*/
	// Repartir los archivos
		int myFiles = my_data->numberOfFiles/my_data->numberOfWorkers;
		int residue = my_data->numberOfFiles%my_data->numberOfWorkers;

		if (residue != 0) {
			//Se debe de estimar los archivos que le tocan
			if(residue > my_data->workerId) {
				myFiles++;
			} 
		}

		int filePosition;
		int finalPosition;

		if(my_data->workerId == 0) {
			filePosition = 0;
			finalPosition = filePosition + myFiles-1;
		}else {	 	
			if (residue > 0 && residue > my_data->workerId) {
				filePosition = myFiles * my_data->workerId;
				finalPosition = filePosition + myFiles -1;
			} else {
				filePosition = myFiles * my_data->workerId + residue;
				finalPosition = filePosition + myFiles-1;
			}
		}
	// Repartir los archivos

	sprintf(
		logMessage, "echo 'Files %i, Residue %i, initial %i, final %i' >> %s", 
		myFiles, residue, filePosition, finalPosition, logName
	);
	system(logMessage);
	
	char commandWorker[1024];
	strcpy(commandWorker, "");
	for(int i = filePosition; i <= finalPosition; i++){
		//printf("%i-%s\n", my_data->workerId, my_data->listNames[i]);
		sprintf(
			commandWorker, "./Slave '%s/%s' '%s/%s' %i",
			my_data->sourcePath, my_data->listNames[i], 
			my_data->sinkPath, generateNewNameDate(my_data->listNames[i]), my_data->workerId 
		);	
		sprintf(logMessage, "echo '%s' >> %s", commandWorker, logName);
		system(logMessage);
		system(commandWorker);
	}
	
	pthread_exit(NULL);
	
}

void printusage(char *app){
	printf("Error in the execution parameters\n");
	printf("Correct execution example\n");
	printf("%s sourcePath sinkPath numberOfSlaves\n", app );
}



/**
 * Main function that invokes the other methods
 * */
int main(int argc, char *argv[]) {

	if(argc != 4) { //The number of parameters entered is verified
		printusage(argv[0]);
		return -1;
	} 

	struct timeval timerActualFilterInit, timerActualFilterEnd;
	struct timeval timerReadInit, timerReadEnd;
	struct timeval timerResponseTimeNextFilterInit, timerResponseTimeNextFilterEnd;
	int milliseconds = 0;
	struct LogFile AccessLayerLog;
	char *logPath = "Logs/Master.csv";	
	char logContent[255];

	char headLine[300];
	strcpy(headLine, "");
	if(!fileExists(logPath)){
		sprintf(
			headLine, 
			"%s, %s, %s, %s, %s, %s",
			"SourcePath","Workers", "Slaves", "ListingFilesTime", "WorkersTime", "ResposeTime\n"
		);
	}

	//Se abre el archivo
	AccessLayerLog = openLog( logPath );
	if ( AccessLayerLog.status == 1 ){
		writeLine(AccessLayerLog, headLine);		
		strcpy(headLine, "");
	} else {
		printf("\t\tSalidaMC2R Error: No se pudo abrir la bitacora\n");
		printf("Verificar que la ruta %s exista", logPath);
	}


	gettimeofday(&timerActualFilterInit, NULL);

		//Input parameters
		char *sourcePath = argv[1];
		char *sinkPath = argv[2];
		int numberOfWorkers = atoi(argv[3]); //Number of workers to invoke
		//int numberOfSlaves = atoi(argv[3]);
		//char * pathConfigurationServers = argv[4];
		DIR *sourceFolder = opendir(sourcePath);
		struct dirent *dir; 
		int numberOfFiles = 0;

		sprintf(logContent, "%s, %i, ", sourcePath, numberOfWorkers);
		gettimeofday(&timerReadInit, NULL);

			if(!sourceFolder){
				printf("The source folder %s doesn't exist\n", sourcePath);
				return -1;
			} 

			printf("The source folder exist. ");
			while((dir=readdir(sourceFolder))!=NULL) {
				if(dir->d_name[0] != '.') {
					numberOfFiles++;
				}
			}
			printf("Are %i files inside\n", numberOfFiles);
			closedir(sourceFolder);

			char **listNames;
			listNames =  malloc(sizeof (char*) * numberOfFiles);
			sourceFolder = opendir(sourcePath);

			int counter = 0;
			while((dir=readdir(sourceFolder))!=NULL) {
				if(dir->d_name[0] != '.') {
					listNames[counter] = malloc((255) * sizeof(char));
					//sprintf(listNames[counter], "%s%s", sourcePath, dir->d_name);
					sprintf(listNames[counter], "%s", dir->d_name);
					counter++;
				}
			}
			closedir(sourceFolder);
		gettimeofday(&timerReadEnd, NULL);
		milliseconds = getMilliseconds(timerReadInit, timerReadEnd);
		sprintf(logContent, "%s%i, ", logContent, milliseconds);

		gettimeofday(&timerResponseTimeNextFilterInit, NULL);
			struct thread_data myThreadData[numberOfWorkers]; //Parametros hilos
			pthread_t threads[numberOfWorkers]; //hilos

			int worker = 0;
			for (worker = 0; worker < numberOfWorkers; ++worker) {
				//Shared memory segments are created for metadata
				myThreadData[worker].workerId = worker;
				myThreadData[worker].listNames = malloc(sizeof (char*) * numberOfFiles);
				myThreadData[worker].numberOfWorkers = numberOfWorkers;
				myThreadData[worker].numberOfFiles = numberOfFiles;
				myThreadData[worker].sourcePath = sourcePath;
				myThreadData[worker].sinkPath = sinkPath;
				
				for(int i = 0; i < numberOfFiles; i++) {
					myThreadData[worker].listNames[i] = listNames[i];
				}

			}
						
			int rc;
			//Se crean los hilos
			for (worker = 0; worker < numberOfWorkers; worker++ ) {				
				//Creando el hilo
				rc = pthread_create ( 
					&threads[worker], NULL, sendWork2Worker, 
					(void *) &myThreadData[worker]
				);			
				if (rc) {
					printf (
						"\tMaster ERROR; return code from pthread_create() is %d\n", rc
					);
					exit(-1);
				}		
			}
			
			/* block until all threads complete */
			for (worker = 0; worker< numberOfWorkers; ++worker) {
				pthread_join(threads[worker], NULL);
			}
		gettimeofday(&timerResponseTimeNextFilterEnd, NULL);
		milliseconds = getMilliseconds(
			timerResponseTimeNextFilterInit, timerResponseTimeNextFilterEnd);
		sprintf(logContent, "%s%i, ", logContent, milliseconds);

	gettimeofday(&timerActualFilterEnd, NULL);
	milliseconds = getMilliseconds(timerActualFilterInit, timerActualFilterEnd);
	sprintf(logContent, "%s%i\n ", logContent, milliseconds);

	if(AccessLayerLog.status == 1){ 	//Esta abierta
		//Se escribe el registro a la bitacora
		writeLine(AccessLayerLog, logContent);					
		closeLog(AccessLayerLog);
	} else { //No se encuentra abierta
		//Se muestra el contenido en la pantalla
		printf("Linea de la bitacora:\n%s",logContent);
	}
	printf("All workers finished their jobs in %ims\n", milliseconds);
	return 1;
}
