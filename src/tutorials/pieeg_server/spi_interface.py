"""
SPI Interface Module for PiEEG

Handles low-level SPI communication with ADS1299 chip.
"""

import logging
import time
import spidev
from RPi import GPIO
from typing import Optional, List

logger = logging.getLogger('device.pieeg.spi')

class SPIInterface:
    """Handles SPI communication with ADS1299 for PiEEG"""
    
    # ADS1299 Command definitions
    RESET = 0x06
    START = 0x08
    STOP = 0x0A
    RDATAC = 0x10
    SDATAC = 0x11
    WAKEUP = 0x02
    
    def __init__(self, spi_bus: int = 0, spi_device: int = 0, gpio_pin: int = 26):
        self.spi_bus = spi_bus
        self.spi_device = spi_device
        self.gpio_pin = gpio_pin
        
        self.spi = None
        self.is_initialized = False
        
        logger.info(f"SPI interface initialized for bus {spi_bus}, device {spi_device}")
    
    def initialize(self) -> bool:
        """Initialize SPI and GPIO interfaces"""
        try:
            # Initialize SPI
            logger.info("Initializing SPI interface...")
            self.spi = spidev.SpiDev()
            self.spi.open(self.spi_bus, self.spi_device)
            self.spi.max_speed_hz = 600000
            self.spi.lsbfirst = False
            self.spi.mode = 0b01
            self.spi.bits_per_word = 8
            logger.info("SPI interface initialized successfully")
            
            # Initialize GPIO using RPi.GPIO (like the working example)
            logger.info(f"Initializing GPIO pin {self.gpio_pin}...")
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.gpio_pin, GPIO.IN)
            logger.info("GPIO interface initialized successfully")
            
            self.is_initialized = True
            return True
            
        except Exception as e:
            logger.error(f"Error initializing SPI/GPIO: {e}")
            self.cleanup()
            return False
    
    def cleanup(self):
        """Cleanup SPI and GPIO resources"""
        try:
            logger.info("Cleaning up SPI and GPIO interfaces...")
            
            if self.spi:
                self.spi.close()
                self.spi = None
                logger.info("SPI interface closed")
            
            # RPi.GPIO cleanup
            GPIO.cleanup()
            logger.info("GPIO interface cleaned up")
                
            self.is_initialized = False
            
        except Exception as e:
            logger.error(f"Error during SPI/GPIO cleanup: {e}")
    
    def check_conflicts(self) -> bool:
        """Check if GPIO pin is already in use"""
        try:
            # Simple check - try to set up the pin
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.gpio_pin, GPIO.IN)
            GPIO.cleanup()
            return False  # No conflicts
        except Exception:
            return True  # Conflicts detected
    
    def send_command(self, command: int) -> bool:
        """Send command to ADS1299"""
        if not self.is_initialized or not self.spi:
            logger.error("SPI not initialized")
            return False
        
        try:
            send_data = [command]
            self.spi.xfer(send_data)
            logger.debug(f"Sent command: 0x{command:02X}")
            return True
        except Exception as e:
            logger.error(f"Error sending command 0x{command:02X}: {e}")
            return False
    
    def read_register(self, register: int) -> Optional[int]:
        """Read a single register from ADS1299"""
        if not self.is_initialized or not self.spi:
            logger.error("SPI not initialized")
            return None
        
        try:
            write_cmd = 0x20
            register_read = write_cmd | register
            data = [register_read, 0x00, register]  # Command, number of bytes-1, register
            result = self.spi.xfer(data)
            
            logger.debug(f"Read register 0x{register:02X}: 0x{result[2]:02X}")
            return result[2]
            
        except Exception as e:
            logger.error(f"Error reading register 0x{register:02X}: {e}")
            return None
    
    def write_register(self, register: int, value: int) -> bool:
        """Write a single register to ADS1299"""
        if not self.is_initialized or not self.spi:
            logger.error("SPI not initialized")
            return False
        
        try:
            write_cmd = 0x40
            register_write = write_cmd | register
            data = [register_write, 0x00, value]  # Command, number of bytes-1, data
            self.spi.xfer(data)
            
            logger.debug(f"Wrote register 0x{register:02X}: 0x{value:02X}")
            return True
            
        except Exception as e:
            logger.error(f"Error writing register 0x{register:02X}: {e}")
            return False
    
    def configure_ads1299(self, gain: int, enabled_channels: int, 
                          ref_enabled: bool = True, biasout_enabled: bool = True) -> bool:
        """Configure ADS1299 for data acquisition - following the working example exactly"""
        try:
            logger.info("Configuring ADS1299...")
            
            # Command sequence exactly like the working example
            self.send_command(self.WAKEUP)
            self.send_command(self.STOP)
            self.send_command(self.RESET)
            self.send_command(self.SDATAC)
            
            # Write registers exactly like the working example
            self.write_register(0x14, 0x80)  # GPIO
            self.write_register(0x01, 0x96)  # Config1
            self.write_register(0x02, 0xD4)  # Config2
            self.write_register(0x03, 0xE0)  # Config3 (changed from 0xFF to 0xE0)
            self.write_register(0x04, 0x00)
            self.write_register(0x0D, 0x00)
            self.write_register(0x0E, 0x00)
            self.write_register(0x0F, 0x00)
            self.write_register(0x10, 0x00)
            self.write_register(0x11, 0x00)
            self.write_register(0x15, 0x20)
            self.write_register(0x17, 0x00)
            
            # Configure channels with gain values (like example2)
            for ch in range(8):
                channel_config = gain if ch < enabled_channels else 0x80
                self.write_register(0x05 + ch, channel_config)
            
            # Start data acquisition like the working example
            self.send_command(self.RDATAC)
            self.send_command(self.START)
            
            # Add a small delay after START command (like the working example)
            time.sleep(0.1)
            
            logger.info("ADS1299 configuration completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error configuring ADS1299: {e}")
            return False
    
    def read_data_packet(self, num_channels: int = 8) -> Optional[List[int]]:
        """Read a complete data packet from ADS1299"""
        if not self.is_initialized or not self.spi:
            logger.error("SPI not initialized")
            return None
        
        try:
            # Set GPIO mode and setup pin (like the working example)
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(self.gpio_pin, GPIO.IN)
            
            # Wait for DRDY signal (data ready) using RPi.GPIO like the example
            GPIO.wait_for_edge(self.gpio_pin, GPIO.FALLING)
            
            # Data is ready, read the packet (27 bytes for 8 channels like the example)
            result = self.spi.readbytes(27)
            
            return result
            
        except Exception as e:
            logger.error(f"Error reading data packet: {e}")
            return None
    
    def parse_data_packet(self, packet: List[int], num_channels: int = 8) -> Optional[List[float]]:
        """Parse raw data packet into channel values"""
        if not packet or len(packet) < 27:
            logger.error("Invalid data packet")
            return None
        
        try:
            # Use the same voltage conversion as the working example
            data_test = 0x7FFFFF
            data_check = 0xFFFFFF
            result = [0] * 27
            
            # Parse each channel (8 channels, 3 bytes each, starting from byte 3)
            for a in range(3, 25, 3):
                voltage_1 = (packet[a] << 8) | packet[a + 1]
                voltage_1 = (voltage_1 << 8) | packet[a + 2]
                convert_voltage = voltage_1 | data_test
                
                if convert_voltage == data_check:
                    voltage_1_after_convert = (voltage_1 - 16777214)
                else:
                    voltage_1_after_convert = voltage_1
                
                channel_num = a // 3
                result[channel_num] = round(1000000 * 4.5 * (voltage_1_after_convert / 16777215), 2)
            
            # Return the 8 channel values (indices 1-8)
            return result[1:9]
            
        except Exception as e:
            logger.error(f"Error parsing data packet: {e}")
            return None
    
    def is_data_ready(self) -> bool:
        """Check if new data is ready to read"""
        try:
            # Set GPIO mode if not already set
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BOARD)
            
            # Setup the pin if not already set up
            GPIO.setup(self.gpio_pin, GPIO.IN)
            
            # DRDY goes low when data is ready
            return GPIO.input(self.gpio_pin) == GPIO.LOW
        except Exception as e:
            logger.error(f"Error checking data ready: {e}")
            return False