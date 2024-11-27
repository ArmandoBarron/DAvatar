#include "lz4.h"    
#include <stdio.h>  
#include <string.h> 
#include <stdlib.h> 
#include <sys/time.h> 
#include "Kulla-Libraries/Kulla.h" 


/**
 * @brief 	It shows the right way to run the application 
 * @param 	appName  The application name
 */
void printUsage(char * appName);

/**
 * @brief 	Applies the LZ4 compression proccess to the data allocated
 * in the shared memory segment and storage the results in a new shared 
 * memory segment.
 *
 * @param[in]  metadataShmid  The metadata shmid that must be used to save 
 * the id of the compressed content with the size of the content.
 * @param[in]  contentSize 	The content size: The size of the content
 * storaged in the shared memory
 * @param[in]  shmid	The shared memory identifier: Is the identifier that must be
 * used to read the data storaged in the shared memory.
 */
void doCompression(int metadataShmid, long contentSize, int shmId);

/**
 * @brief      Invokes the LZ4 Comrpession process
 *
 * @param[in]  argc  The argc: Number of input parameters
 * @param      argv  The argv: Value of the input parameters
 *
 * @return     Exit status
 */
int main(int argc, char *argv[]) {

	if (argc != 4)	{
		printUsage(argv[0]);
	}

	doCompression(atoi(argv[1]), atol(argv[2]), atoi(argv[3]));
	return 0;
}

/**
 * @brief 	It shows the right way to run the application 
 * @param 	appName  The application name
 */
void printUsage(char * appName){
	printf("%s\n%s %s\nWhere:\n%s\n%s\n%s\n", 
		"Error in the execution parameters, the correct usage is:",
		appName, "metadataShmid contentSize shmId",
		"metadataShmidfileSize = id for shared memory for the metadata",
		"contentSize = size of the content storaged in the shared memory",
		"shmId = id that must be used to read the content storaged in shared memory"
	);
	exit(EXIT_FAILURE);
	return;
}

/**
 * @brief 	Applies the LZ4 compression proccess to the data allocated
 * in the shared memory segment and storage the results in a new shared 
 * memory segment.
 *
 * @param[in]  metadataShmid  The metadata shmid that must be used to save 
 * the id of the compressed content with the size of the content.
 * @param[in]  contentSize 	The content size: The size of the content
 * storaged in the shared memory
 * @param[in]  shmid	The shared memory identifier: Is the identifier that must be
 * used to read the data storaged in the shared memory.
 */
void doCompression(int metadataShmid, long contentSize, int shmId){

	struct timeval timerActualFilterInit, timerActualFilterEnd;
    struct timeval timerReadInit, timerReadEnd;
    struct timeval timerFilterInit, timerFilterEnd;
    struct timeval timerWriteInit, timerWriteEnd;

	char *logPath = "Logs/LZ4Compression.csv";   
    struct LogFile FilterLogFile;
    char logContent[1024];
    long microseconds = 0;

    char headLine[300];
    strcpy(headLine, "");
    if(!fileExists(logPath)){
        sprintf(
            headLine, 
            "%s, %s, %s, %s, %s, %s, %s \n",
            "FilterName",  
            "datetime (Ymd_H:M:S)",
            "FileSize (b)",
            "Read shm Time (microseconds)",
            "Service time (microseconds)",
            "Write shm time (microseconds)",
            "Response time (microseconds)"
        );
    }

    FilterLogFile = openLog( logPath );
        
    if ( FilterLogFile.status == 1 ){
        writeLine(FilterLogFile, headLine);
        strcpy(headLine, "");
    } else {
        printf("\t\tError: No se pudo abrir la bitacora\n");
        printf("Verificar que la ruta %s exista", logPath);
    }	

    gettimeofday(&timerActualFilterInit, NULL);

        sprintf(logContent, "LZ4Compressor, %s, %ld", getCurrentDateTime(), contentSize);

		//Variable declaration
		char *inputData; // Data retrieved from the shared memory
		char sharedMsj[255]; //Message to be shared with the previous filter
		int response = 0; //Response of the lz4 process
		size_t max_dst_file_size; //Maximum size of compressed content
		size_t compressed_data_file_size;//Real compressed content size
		char *compressedContent;//Compressed content
		char errorMessage[140];
		struct shmSegment structShmCompressed; //Data of shared memory output
		char *shmCompressenContent; //Shared memory output

		gettimeofday(&timerReadInit, NULL);
			//The local variable is linked to the content stored in shared memory 
			inputData = attach_segment(shmId); 
		gettimeofday(&timerReadEnd, NULL);
		microseconds = getMicroseconds(timerReadInit, timerReadEnd);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);
	
		gettimeofday(&timerFilterInit, NULL);
			//Ontain the maximum size of compressed content
			max_dst_file_size = LZ4_compressBound(contentSize); 
			compressedContent = malloc(max_dst_file_size); //Reserve memory 
			
			if (compressedContent == NULL) //Verify if the memory was reserved
			run_screaming(
				"Failed to allocate memory for *compressed_data.", 500
			);
			
			response = LZ4_compress_default(
				inputData, compressedContent, contentSize, max_dst_file_size
			);
			
			if (response < 0){
				sprintf(
					errorMessage, "%s%s",
					"A negative result from LZ4_compress_default indicates ",
					"a failure trying to compress the data."
				);
				run_screaming(errorMessage, response);
			}
			if (response == 0){
				sprintf(
					errorMessage, "%s%s",
					"A result of 0 means compression worked, but was stopped ",
					"because the destination buffer couldn't hold all the information."
				);
				run_screaming(errorMessage, 1);
			}

			
			compressed_data_file_size = response;
			compressedContent = (char *)realloc( compressedContent,compressed_data_file_size );

			if (compressedContent == NULL)
			run_screaming("Failed to re-alloc memory for compressed_data.", 1);

		gettimeofday(&timerFilterEnd, NULL);
		microseconds = getMicroseconds(timerFilterInit, timerFilterEnd);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);

		//Elimination of shared memory segment is approved
		clean_segment( inputData, shmId );

		gettimeofday(&timerWriteInit, NULL);

			/* The shared memory segment is generated with the size required 
			* for the compressed content */
			structShmCompressed = generateShmKeyAndOpenShmSegment(compressed_data_file_size
			);

			//Linking the local variable to the shared memory segment
			shmCompressenContent = attach_segment(
				structShmCompressed.shmId
			);
					
			/* Copying the value of the local variable to the linked variable 
			* to the shared memory segment */
			copyFromLocalToShm (
				shmCompressenContent, compressedContent, 
				compressed_data_file_size
			);

		gettimeofday(&timerWriteEnd, NULL);
		microseconds = getMicroseconds(timerWriteInit, timerWriteEnd);       
		sprintf(logContent, "%s, %ld", logContent, microseconds);	
			
		//Colocando datos en la mc de mensajes
		sprintf( sharedMsj, "%ld %i", compressed_data_file_size, structShmCompressed.shmId );
		//Obteniendo puntero de la metadata compartida
		char * shm_localPointer = attach_segment(metadataShmid);
		//Copiando la metadata
		copyFromLocalToShm( shm_localPointer, sharedMsj, 500 );
		//Liberando la memoria
		free(compressedContent);

    gettimeofday(&timerActualFilterEnd, NULL);

	microseconds = getMicroseconds(timerActualFilterInit, timerActualFilterEnd);       
    sprintf(logContent, "%s, %ld\n", logContent, microseconds);

    if(FilterLogFile.status == 1){     
        writeLine(FilterLogFile, logContent);                  
        closeLog(FilterLogFile);
    } else { 
        printf("Linea de la bitacora:\n%s",logContent);
    }

}