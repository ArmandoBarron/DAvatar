CC:= gcc
LIBCC:= -c 
CFLAGS:= -g -Wall 
HILOS:= -lpthread
CRYPTO:= -lcrypto
MATH:= -lm
STD:= -std=gnu99
RM:= rm
LZ41:= -ILZ4-Libraries/lib 
LZ42:= -ILZ4-Libraries/programs 
LZ43:= -DXXH_NAMESPACE=LZ4_  
LZ44:= LZ4-Libraries/lib/lz4.o

all:  Master Slave GenerateSHA256 LZ4Compressor AESCode  

Master: Master.o Kulla-Libraries/Kulla.o 
	$(CC) $(CFLAGS) -o Master Master.o Kulla-Libraries/Kulla.o  $(HILOS) 
	$(RM) Master.o

Slave: Slave.o Kulla-Libraries/Kulla.o 
	$(CC) $(CFLAGS) -o Slave Slave.o Kulla-Libraries/Kulla.o 
	$(RM) Slave.o

GenerateSHA256: GenerateSHA256.o  Kulla-Libraries/Kulla.o 
	$(CC) $(CFLAGS) -o GenerateSHA256 GenerateSHA256.o  Kulla-Libraries/Kulla.o  $(MATH) $(CRYPTO)
	$(RM) GenerateSHA256.o

LZ4Compressor: LZ4Compressor.o Kulla-Libraries/Kulla.o 
	$(CC) $(CFLAGS) -o LZ4Compressor Kulla-Libraries/Kulla.o  LZ4Compressor.o $(LZ44) $(MATH)
	$(RM) LZ4Compressor.o

AESCode: AESCode.o Kulla-Libraries/Kulla.o 
	$(CC) $(CFLAGS) -o AESCode AESCode.o Kulla-Libraries/Kulla.o  $(MATH) $(CRYPTO)
	$(RM) AESCode.o

#Dependencias
LZ4Compressor.o: LZ4Compressor.c Kulla-Libraries/Kulla.o 
	$(CC) $(LIBCC) $(CFLAGS) $(LZ41) $(LZ42) $(LZ43) -Wcpp -o LZ4Compressor.o LZ4Compressor.c $(MATH) 


clean: 
	$(RM) Master
	$(RM) Slave
	$(RM) GenerateSHA256
	$(RM) LZ4Compressor
	$(RM) AESCode
