# Import the custom GPS serial communication class
from PyGSFGPSSerial import *

BLUETOOTH_MODULE_NAME = "GSFGPS_BT_0001"

# Initialize GPS module on COM6 port
gps = PyGSFGPSSerial(port='COM6')

# Attempt to establish serial connection
if gps.open():
    # Set DTR pin to True (0v) to use the USB port to communicate with the BT module (Rx/Tx)
    gps.set_dtr(True)

    # Switch from Data mode to Command mode using +++ sequence
    gps.enter_command_mode()
    # Send test AT command to verify command mode
    gps.send_at_command("AT")

    # Set the Data mode as default at startup
    gps.send_at_command("AT+UMSM={}".format(1))
    # Query Module Startup mode (0=Command, 1=Data)
    gps.send_at_command("AT+UMSM?")

    # Setup Bluetooth module name
    gps.send_at_command("AT+UBTLN={}".format(BLUETOOTH_MODULE_NAME))
    # Query Bluetooth module name
    gps.send_at_command("AT+UBTLN?")

    # Store the current configuration to the Bluetooth. Need the AT+CPWROFF command to write it in non-volatile memory
    gps.send_at_command("AT&W0")
    # Reboot the module and store the settings in non-volatile memory
    gps.send_at_command("AT+CPWROFF")

    # Send test AT command to verify command mode
    gps.send_at_command("AT")
    # Switch back to Data mode for normal GPS operation
    gps.enter_data_mode()

    # Set DTR pin to False (3.3V), default state. GPS data will go to BT module. USB is only in read mode, no TX
    gps.set_dtr(False)
    # Close serial port and release resources
    gps.close()
