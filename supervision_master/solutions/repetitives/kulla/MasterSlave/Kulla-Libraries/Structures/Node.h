/**
 * @brief Node structure.
 * 
 * Node structure stores the data of files found in the file system.
 */
typedef struct node {
    char *parent;           /**< Directory path to the file.*/
    char *fileName;         /**< Name of the files in the directory.*/
    char *onlyName;         /**< Name of the files in the directory.*/
    long fileSize;          /**< Size of the file in bytes.*/
    struct node * next;     /**< Next element in the linked list.*/
} node_t;