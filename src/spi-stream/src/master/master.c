//-----------------------------------------------------------------------------
// Kateryna Voitiuk (kvoitiuk@ucsc.edu)
// Braingeneers
// master.c
// Description: Implementation file for master spi controller
//-----------------------------------------------------------------------------


#include "../protocol.h"



int main(int argc, char *argv[]) {

  if (!bcm2835_init())  {
    printf("bcm2835_init failed; running as root??\n");
    exit(1);
  }

  if (!bcm2835_spi_begin()) {
    printf("bcm2835_spi_begin failed; running as root??\n");
    exit(1);
  }

  //Init SPI interface settings
  bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);      // default
  bcm2835_spi_setDataMode(BCM2835_SPI_MODE0);                   // default
  bcm2835_spi_setClockDivider(BCM2835_SPI_CLOCK_DIVIDER_65536); // default
  bcm2835_spi_chipSelect(BCM2835_SPI_CS0);                      // default
  bcm2835_spi_setChipSelectPolarity(BCM2835_SPI_CS0, LOW);      // default

  // Send a byte to slave and simultaneously read a byte back from slave
  uint8_t send_data, read_data;
  send_data = 0x23;
  read_data = bcm2835_spi_transfer(send_data);

  printf("Sent to SPI: 0x%02X. Read from SPI: 0x%02X.\n", send_data, read_data);

  //exit
  bcm2835_spi_end();
  bcm2835_close();
  return 0;

}
