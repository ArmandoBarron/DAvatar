#include <stdio.h>
#include <libgen.h>
#include <unistd.h>
#include <string.h> 
#include <openssl/sha.h>
#include <sys/time.h> 
#include "Kulla-Libraries/Kulla.h"

/**
 * @brief 	It shows the right way to run the application 
 * @param 	appName  The application name
 */
void printUsage(char * appName);

/**
 * @brief 	Applies the sha256 hash proccess to the data allocated
 * in the shared memory segment and storage the results in a new shared 
 * memory segment.
 *
 * @param[in]  metadataShmid  The metadata shmid that must be used to save 
 * the id of the crypted content with the size of the content.
 * @param[in]  contentSize 	The content size: The size of the content
 * storaged in the shared memory
 * @param[in]  shmid	The shared memory identifier: Is the identifier that must be
 * used to read the data storaged in the shared memory.
 */
void doProcess(int metadataShmid, long contentSize, int shmId);



/**
 * Realiza la codificación de un archivo
 * @param  argc número de parámetros ingresados
 * @param  argv Valores de los parámetros ingresados
 * @return      1 si la aplicación se ejecito correctamente, -1 de lo contrario
 */
int main(int argc, char *argv[]) {

    if(argc != 4) {
        printUsage(argv[0]);
    }
    doProcess(atoi(argv[1]), atol(argv[2]), atoi(argv[3]));
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
 * @brief 	Applies the sha256 hash proccess to the data allocated
 * in the shared memory segment and storage the results in a new shared 
 * memory segment.
 *
 * @param[in]  metadataShmid  The metadata shmid that must be used to save 
 * the id of the crypted content with the size of the content.
 * @param[in]  contentSize 	The content size: The size of the content
 * storaged in the shared memory
 * @param[in]  shmid	The shared memory identifier: Is the identifier that must be
 * used to read the data storaged in the shared memory.
 */
void doProcess(int metadataShmid, long contentSize, int shmId){
    struct timeval timerActualFilterInit, timerActualFilterEnd;
    struct timeval timerReadInit, timerReadEnd;
    struct timeval timerFilterInit, timerFilterEnd;
    struct timeval timerWriteInit, timerWriteEnd;


    gettimeofday(&timerActualFilterInit, NULL);

        char *logPath = "Logs/SHA-256Generate.csv";   
        struct LogFile FilterLogFile;
        char logContent[1024];
        long microseconds = 0;
        SHA256_CTX sha;
        unsigned char digest[SHA256_DIGEST_LENGTH];
        int shaStrLen = SHA256_DIGEST_LENGTH * 2 + 1;
        char shaString[shaStrLen];

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
                "Service SHA256 time (microseconds)",
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


        sprintf(logContent, "Sha256Generate, %s, %ld", getCurrentDateTime(), contentSize);
        char *inputData;
        char *resultantContent;
        long resultantSize;
        char sharedMsj[255]; //Message to be shared with the previous filter
        struct shmSegment structShmFilter; //Data of shared memory output
        char *shmFiterContent; //Shared memory output

        gettimeofday(&timerReadInit, NULL);
            inputData = attach_segment(shmId);
        gettimeofday(&timerReadEnd, NULL);
        microseconds = getMicroseconds(timerReadInit, timerReadEnd);       
        sprintf(logContent, "%s, %ld", logContent, microseconds);

        gettimeofday(&timerFilterInit, NULL);
            SHA256_Init(&sha);
            SHA256_Update(&sha, inputData, contentSize);
            SHA256_Final(digest, &sha);
            for (int i = 0; i < SHA256_DIGEST_LENGTH; i++)
                sprintf(&shaString[ i * 2 ], "%02x", (unsigned int)digest[i]);

            resultantSize = contentSize + shaStrLen;
            resultantContent = (char *) malloc(sizeof(char)*resultantSize);
            memcpy(resultantContent, inputData, contentSize);
            memcpy(resultantContent+contentSize, shaString, shaStrLen);
        gettimeofday(&timerFilterEnd, NULL);
        microseconds = getMicroseconds(timerFilterInit, timerFilterEnd);       
        sprintf(logContent, "%s, %ld", logContent, microseconds);
    
        gettimeofday(&timerWriteInit, NULL);
            structShmFilter = generateShmKeyAndOpenShmSegment(resultantSize);
            shmFiterContent = attach_segment( structShmFilter.shmId );        
            copyFromLocalToShm ( shmFiterContent, resultantContent, resultantSize );	
        gettimeofday(&timerWriteEnd, NULL);
        microseconds = getMicroseconds(timerWriteInit, timerWriteEnd);       
        sprintf(logContent, "%s, %ld", logContent, microseconds);
        
        sprintf( sharedMsj, "%ld %i", resultantSize, structShmFilter.shmId );
        char * shm_localPointer = attach_segment(metadataShmid);
        copyFromLocalToShm( shm_localPointer, sharedMsj, 500 );
        free(resultantContent);
    gettimeofday(&timerActualFilterEnd, NULL);

		clean_segment(inputData, shmId); //Borrarlos datos de entrada

    microseconds = getMicroseconds(timerActualFilterInit, timerActualFilterEnd);       
    sprintf(logContent, "%s, %ld\n", logContent, microseconds);

    if(FilterLogFile.status == 1){
        writeLine(FilterLogFile, logContent);                  
        closeLog(FilterLogFile);
    } else { 
        printf("Linea de la bitacora:\n%s",logContent);
    }
}