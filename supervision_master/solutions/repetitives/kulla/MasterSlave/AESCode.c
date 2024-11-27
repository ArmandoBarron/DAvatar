#include <libgen.h>
#include <unistd.h>
#include <string.h> 
#include "Kulla-Libraries/Kulla.h" // For read files and SHM
#include "AES-Libraries/aes.h"
#include <sys/time.h> 

/**
 * @brief 	It shows the right way to run the application 
 * @param 	appName  The application name
 */
void printUsage(char * appName);

/**
 * @brief 	Applies the AES crypt proccess to the data allocated
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
 * @brief      Invokes the AES crypt process
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
 * @brief 	Applies the AES Encrypt proccess to the data allocated
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


    //Usadas para medir el tiempo de servicio de esta aplicacion
    struct timeval timerActualFilterInit, timerActualFilterEnd;
    struct timeval timerReadInit, timerReadEnd;
    struct timeval timerFilterInit, timerFilterEnd;
    struct timeval timerWriteInit, timerWriteEnd;

    char *logPath = "Logs/AESEncrypt.csv";   
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
            "Read Time (microseconds)",
            "AES Time (microseconds)",
            "Write time (microseconds)",
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


        sprintf(logContent, "AesCode, %s, %ld", getCurrentDateTime(), contentSize);
        char idContent[10]; 
        int keyDataLen;
        unsigned char *keyData;
        EVP_CIPHER_CTX *encrypt;
        unsigned char *cipherContent;
        unsigned int salt[] = {12345, 54321};
        sprintf(idContent, "%i", 100);
        keyData = (unsigned char *)idContent;
        keyDataLen = strlen(idContent);
        
        //Variable declaration
        char *inputData; // Data retrieved from the shared memory
        char sharedMsj[255]; //Message to be shared with the previous filter
        struct shmSegment structShmAes; //Data of shared memory output
        char *shmAesContent; //Shared memory output
        int fileSize = (int)contentSize;

        gettimeofday(&timerReadInit, NULL);
            inputData = attach_segment(shmId); //The local variable is linked to the content stored in shared memory 
        gettimeofday(&timerReadEnd, NULL);
        microseconds = getMicroseconds(timerReadInit, timerReadEnd);       
        sprintf(logContent, "%s, %ld", logContent, microseconds);

        gettimeofday(&timerFilterInit, NULL);
            encrypt = EVP_CIPHER_CTX_new();
            if (encrypt == NULL) exit(1);

            if (initEncryptAES(keyData, keyDataLen, (unsigned char *)&salt, encrypt)) {
                printf("Couldn't initialize AES cipher\n");
                exit(1);
            }
            cipherContent = encryptAES(encrypt, (unsigned char *)inputData, &fileSize);
        gettimeofday(&timerFilterEnd, NULL);
        microseconds = getMicroseconds(timerFilterInit, timerFilterEnd);       
        sprintf(logContent, "%s, %ld", logContent, microseconds);
    
        gettimeofday(&timerWriteInit, NULL);
            structShmAes = generateShmKeyAndOpenShmSegment(fileSize);
            shmAesContent = attach_segment( structShmAes.shmId ); 
            copyFromLocalToShm ( shmAesContent, (char *)cipherContent, fileSize );	
        gettimeofday(&timerWriteEnd, NULL);
        microseconds = getMicroseconds(timerWriteInit, timerWriteEnd);       
        sprintf(logContent, "%s, %ld", logContent, microseconds);
        
        //Colocando datos en la mc de mensajes
        sprintf( sharedMsj, "%i %i", fileSize, structShmAes.shmId );
        char * shm_localPointer = attach_segment(metadataShmid);
        copyFromLocalToShm( shm_localPointer, sharedMsj, 500 );
        free(cipherContent);
    gettimeofday(&timerActualFilterEnd, NULL);
		clean_segment(inputData, shmId); //Borrarlos datos de entrada
    microseconds = getMicroseconds(timerActualFilterInit, timerActualFilterEnd);       
    sprintf(logContent, "%s, %ld\n", logContent, microseconds);

    //Comprobando el estado de apertura de la bitacora
    if(FilterLogFile.status == 1){   
        writeLine(FilterLogFile, logContent);                  
        closeLog(FilterLogFile);
    } else { 
        printf("Linea de la bitacora:\n%s",logContent);
    }

}