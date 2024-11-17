# Import the custom GPS serial communication class
from PyGSFGPSSerial import *
from time import sleep

# Initialize GPS module on COM6 port
gps = PyGSFGPSSerial(port='COM6')

# Attempt to establish serial connection
if gps.open():
    # Set DTR pin to False
    gps.set_dtr(False)

    # Switch from Data mode to Command mode using +++ sequence
    gps.exit_data_mode()

    # Wait for mode transition to complete
    sleep(0.5)
    # Send test AT command to verify command mode
    gps.send_at_command("AT")

    # Switch back to Data mode for normal GPS operation
    gps.exit_command_mode()

    # Close serial port and release resources
    gps.close()