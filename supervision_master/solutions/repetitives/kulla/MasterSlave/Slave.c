#include "stdlib.h"
#include "stdio.h"
#include <dirent.h>
#include "Kulla-Libraries/Kulla.h" 

long metadataSize = 500;

/**
 * @brief       It shows the right way to run the application 
 * @param      appName  The application name
 */
void printUsage(char * appName);

/**
 * @brief	Runs the pipeline
 * @param	dataSourcePath: the input filepath of the file that will be processed
 * @param	dataSinkPath: the output filepath where the results will be storaged"
 * @param 	workerId
 */ 
void runPipeline(char *dataSourcePath, char *dataSinkPath, int workerId);

void generateSHA256(int metadataId, long fileSize, int shmId);
void doCompression(int metadataId, long fileSize, int shmId);
void doCrypt(int metadataId, long fileSize, int shmId);

int main(int argc, char **argv){
	
	if(argc != 4) {
		printUsage(argv[0]);
		return EXIT_FAILURE;
	} else {
		struct timeval uno, dos;
    	gettimeofday(&uno, NULL);
		runPipeline(argv[1], argv[2], atoi(argv[3]));
    	gettimeofday(&dos, NULL);
		long m  = getMicroseconds(uno, dos);
		printf("worker pipeline ST(microsecond): %ld\n", m);
		return EXIT_SUCCESS;
	}
}

void printUsage(char * appName){	
	printf("%s\n%s %s\nWhere:\n%s\n%s\n", 
		"Error in the execution parameters, the correct usage is:",
		appName, "DataSourcePath DataSinkPath",
		"DataSourcePath = is the input filepath of the file that will be processed",
		"DataSinkPath= is the output filepath where the results will be storaged"
	);
	exit(EXIT_FAILURE);
}

void runPipeline(char *dataSourcePath, char *dataSinkPath, int workerId){

	struct timeval timerPipelineInit, timerPipelineEnd; //Response time of the pipeline
    struct timeval timerReadInit, timerReadEnd; //Time used for read the input file
    struct timeval timerWriteShmInit, timerWriteShmEnd; //Time used to allocate the input in shm
    struct timeval timerF1Init, timerF1End; //Response time of the first filter
    struct timeval timerReadShmF1Init, timerReadShmF1End; //Time used to recover metadata from shm
    struct timeval timerF2Init, timerF2End; //Response time of the second filter
	long microseconds = 0;

	char logPath[100];
	sprintf( logPath, "Logs/PipelineWorker%i.csv", workerId);
    struct LogFile FilterLogFile;
    char logContent[1024];

    char headLine[300];
    strcpy(headLine, "");
    if(!fileExists(logPath)){
        sprintf(
            headLine, 
            "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n",
			"Filter name",
            "datetime (Ymd_H:M:S)",
            "File name",
            "File size (b)",
            "ReadFile (microseconds)",
            "Local2Shm (microseconds)",
            "F1 RT (microseconds)",
            "Shm2local (microseconds)",
            "F2 RT (microseconds)",
            "Shm2localF2 (microseconds)",
			"F3 RT (microseconds)",
			"Shm2localF3 (microseconds)",
			"Write time (microseconds)",
			"Pipeline RT (microseconds)"
        );
    }

    FilterLogFile = openLog( logPath );
        
    if ( FilterLogFile.status ){
        writeLine(FilterLogFile, headLine);
        strcpy(headLine, "");
    } else {
        printf("\t\tpipeline-4filters Error: No se pudo abrir la bitacora\n");
        printf("Verificar que la ruta %s exista", logPath);
    }

	//Input
	char *fileContent;
	long fileSize;

	//Shm segments for the input data
	struct shmSegment shmInput; 
	char	*shmReadedContent;

	//Shm segment of metadata F1 (SHA256)
	struct shmSegment MetadataF1;
	char	*metadataContentF1;
	struct contenidoMsjMetadata contenidoMsjF1;

	//Shm segment of metadata F2 (LZ4)
	struct shmSegment MetadataF2;
	char	*metadataContentF2;
	struct contenidoMsjMetadata contenidoMsjF2;

	//Shm segment of metadata F3 (AES)
	struct shmSegment MetadataF3;
	char	*metadataContentF3;
	struct contenidoMsjMetadata contenidoMsjF3;

	gettimeofday(&timerPipelineInit, NULL);

	char logMessage[256];
	char logName[256];
	sprintf(logName, "Logs/Worker_%i.log", workerId);
	
		sprintf(logMessage, "echo 'Reading the file %s' >> %s",  dataSourcePath, logName);
		system(logMessage);
		gettimeofday(&timerReadInit, NULL);
			fileSize = getFileSize(dataSourcePath);
			fileContent = readFile(dataSourcePath);
		gettimeofday(&timerReadEnd, NULL);
		microseconds = getMicroseconds(timerReadInit, timerReadEnd);   
		sprintf(logContent, "pipeline, %s, %s, %ld, %ld",getCurrentDateTime(), dataSourcePath, fileSize, microseconds);

		//Copy local content to shmsegment
		sprintf(logMessage, "echo 'Copying the local content to shmsegment %s' >> %s",  dataSourcePath, logName);
		system(logMessage);
		gettimeofday(&timerWriteShmInit, NULL);
			shmInput = generateShmKeyAndOpenShmSegment(fileSize); 
			shmReadedContent = attach_segment(shmInput.shmId);
			copyFromLocalToShm(shmReadedContent, fileContent, fileSize);		
		gettimeofday(&timerWriteShmEnd, NULL);
		microseconds = getMicroseconds(timerWriteShmInit, timerWriteShmEnd);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);
			free(fileContent);

		//SHA256
		sprintf(logMessage, "echo 'Executing sha256: %s' >> %s",  dataSourcePath, logName);
		system(logMessage);
		gettimeofday(&timerF1Init, NULL);
			MetadataF1 = generateShmKeyAndOpenShmSegment(metadataSize);
			generateSHA256(MetadataF1.shmId, fileSize, shmInput.shmId);
		gettimeofday(&timerF1End, NULL);
		microseconds = getMicroseconds(timerF1Init, timerF1End);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);

		//Read data from shm and share with the next filter
		sprintf(logMessage, "echo 'Recovering the sha256 metadata from shmsegment: %s' >> %s",  dataSourcePath, logName);
		system(logMessage);

		gettimeofday(&timerReadShmF1Init, NULL);
			metadataContentF1 = attach_segment(MetadataF1.shmId);
			contenidoMsjF1 = recuperarElementosMsj(metadataContentF1);
		gettimeofday(&timerReadShmF1End, NULL);
		microseconds = getMicroseconds(timerReadShmF1Init, timerReadShmF1End);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);

		//LZ4Process
		sprintf(logMessage, "echo 'Executing LZ4: %s' >> %s",  dataSourcePath, logName);
		system(logMessage);
		gettimeofday(&timerF1Init, NULL);
			MetadataF2 = generateShmKeyAndOpenShmSegment(metadataSize);
			doCompression(MetadataF2.shmId, contenidoMsjF1.tamanioDelArchivo, contenidoMsjF1.keyMC);
		gettimeofday(&timerF1End, NULL);
		microseconds = getMicroseconds(timerF1Init, timerF1End);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);

		//Read data from shm and share with the next filter
		sprintf(logMessage, "echo 'Recovering the LZ4 metadata from shmsegment: %s' >> %s",  dataSourcePath, logName);
		system(logMessage);
		gettimeofday(&timerReadShmF1Init, NULL);
			metadataContentF2 = attach_segment(MetadataF2.shmId);
			contenidoMsjF2 = recuperarElementosMsj(metadataContentF2);
		gettimeofday(&timerReadShmF1End, NULL);
		microseconds = getMicroseconds(timerReadShmF1Init, timerReadShmF1End);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);

		//AESEncrypt		
		sprintf(logMessage, "echo 'Executing AES: %s' >> %s",  dataSourcePath, logName);
		system(logMessage);
		gettimeofday(&timerF1Init, NULL);
			MetadataF3 = generateShmKeyAndOpenShmSegment(metadataSize);
			doCrypt(MetadataF3.shmId, contenidoMsjF2.tamanioDelArchivo, contenidoMsjF2.keyMC);
		gettimeofday(&timerF1End, NULL);
		microseconds = getMicroseconds(timerF1Init, timerF1End);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);

		//Read data from shm and share with the next filter
		sprintf(logMessage, "echo 'Recovering the AES metadata from shmsegment: %s' >> %s",  dataSourcePath, logName);
		system(logMessage);
		gettimeofday(&timerReadShmF1Init, NULL);
			metadataContentF3 = attach_segment(MetadataF3.shmId);
			contenidoMsjF3 = recuperarElementosMsj(metadataContentF3);
		gettimeofday(&timerReadShmF1End, NULL);
		microseconds = getMicroseconds(timerReadShmF1Init, timerReadShmF1End);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);
		
		sprintf(logMessage, "echo 'Writring the result: %s' >> %s",  dataSinkPath, logName);
		system(logMessage);
		gettimeofday(&timerF2Init, NULL);
			char *outputData = attach_segment(contenidoMsjF3.keyMC);
			writeFile(outputData,contenidoMsjF3.tamanioDelArchivo, dataSinkPath);
		gettimeofday(&timerF2End, NULL);
		microseconds = getMicroseconds(timerF2Init, timerF2End);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);

		//free(outputData);
		clean_segment(shmReadedContent, shmInput.shmId);
		clean_segment(metadataContentF1, MetadataF1.shmId);
		clean_segment(metadataContentF2, MetadataF2.shmId);
		clean_segment(metadataContentF3, MetadataF3.shmId);
		clean_segment(outputData, contenidoMsjF3.keyMC);
	
	gettimeofday(&timerPipelineEnd, NULL);
	microseconds = getMicroseconds(timerPipelineInit, timerPipelineEnd);       
	sprintf(logContent, "%s, %ld\n", logContent, microseconds);

	sprintf(logMessage, "echo '%s Response time (microseconds): %ld' >> %s",  dataSourcePath, microseconds, logName);
	system(logMessage);

	//Comprobando el estado de apertura de la bitacora
	if(FilterLogFile.status == 1){     //Esta abierta
		//Se escribe el registro a la bitacora
		//printf("Pipeline: %s", logContent);
		writeLine(FilterLogFile, logContent); 
		strcpy(logContent, "");
	} else { //No se encuentra abierta
		//Se muestra el contenido en la pantalla
		printf("Linea de la bitacora:\n%s",logContent);
	}

}

void doCompression(int metadataId, long fileSize, int shmId){

	long 	commandSize;
	char 	*baseCommand, *filterCommand;
	baseCommand = "./LZ4Compressor %i %ld %i";
	commandSize = strlen(baseCommand) + sizeof(metadataId) + sizeof(shmId) + sizeof(fileSize);	
	filterCommand = malloc((commandSize)*sizeof(char));
	sprintf( filterCommand, baseCommand, metadataId, fileSize, shmId );
	system(filterCommand);

}

void doCrypt(int metadataId, long fileSize, int shmId){

	long	commandSize;
	char	*baseCommand, *filterCommand;
	baseCommand = "./AESCode %i %ld %i";
	commandSize = strlen(baseCommand) + sizeof(metadataId) + sizeof(shmId) + sizeof(fileSize);
	filterCommand = malloc((commandSize)*sizeof(char));
	sprintf( filterCommand, baseCommand, metadataId, fileSize, shmId );
	system(filterCommand);

}

void generateSHA256(int metadataId, long fileSize, int shmId){

	long    commandSize;
	char 	*baseCommand, *filterCommand;
	baseCommand = "./GenerateSHA256 %i %ld %i";
	commandSize = strlen(baseCommand) + sizeof(metadataId) + sizeof(shmId) + sizeof(fileSize);
	filterCommand = malloc((commandSize)*sizeof(char));
	sprintf( filterCommand, baseCommand, metadataId, fileSize, shmId );
	system(filterCommand);

}