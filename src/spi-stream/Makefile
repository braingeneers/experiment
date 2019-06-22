CFLAGS = -Wall -Isrc -lpthread
PI_CFLAGS = -lbcm2835 #-lwiringPi 
CC = g++ -std=c++17

MASTER_SRC=$(wildcard src/master/*.c) # /src/protocol.h)
SLAVE_SRC=$(wildcard src/slave/*.c) #/src/protocol.h)

all: spi-master spi-slave


#Linux board Controller (Stimulation/Recording, Data Buffering, Analysis)
spi-master: $(MASTERY_SRC)
	$(CC) -o $@ $^ $(CFLAGS) $(PI_CFLAGS)

#Emulation of Intan headstage for debug/testing
spi-slave: $(MASTER_SRC)
	$(CC) -o $@ $^ $(CFLAGS) $(PI_CFLAGS)

clean:
	@rm spi-master spi-slave
