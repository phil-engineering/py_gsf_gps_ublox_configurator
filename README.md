# uBlox NINA-B1 Serial Communication Program

A Python utility for managing serial communication with uBlox Bluetooth module, providing functionality for mode switching and basic AT command interactions.

## Description

This program provides a simple interface for:
- Establishing serial connections with uBlox Bluetooth module
- Switching between Command and Data modes
- Sending AT commands
- Managing DTR pin states (hardware specific)

## Prerequisites

### Hardware Requirements
- uBlox NINA-B1 Bluetooth module module

### Software Requirements
- Python 3.x
- PySerial library
```bash
pip install pyserial
```

## Project Structure

```
.
├── PyGSFGPSSerial.py    # Main serial communication class
└── main.py              # Example implementation script
```

## Installation

1. Clone the repository or download the source files
2. Install required dependencies:
   ```bash
   pip install pyserial
   ```

## Usage

### Basic Implementation
```python
from PyGSFGPSSerial import *
from time import sleep

# Initialize GPS module
gps = PyGSFGPSSerial(port='COM6')

# Open connection and perform operations
if gps.open():
    gps.set_dtr(False)           # Set DTR to 3.3V
    gps.exit_data_mode()         # Enter command mode
    sleep(0.5)                   # Wait for transition
    gps.send_at_command("AT")    # Send test command
    gps.exit_command_mode()      # Return to data mode
    gps.close()                  # Close connection
```

### Configuration Options

Default serial port settings:
- Baud Rate: 115200
- Hardware Flow Control: Enabled (rtscts=True)
- DTR pin is hardware specific and allow to switch between USB Tx or GPS Tx

## License

[MIT](https://choosealicense.com/licenses/mit/)