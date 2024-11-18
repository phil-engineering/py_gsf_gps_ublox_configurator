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
    gps.enter_command_mode()
    # Send test AT command to verify command mode
    gps.send_at_command("AT")

    # Set the Data mode as default at startup
    gps.send_at_command("AT+UMSM={}".format(1))
    # Query Module Startup mode (0=Command, 1=Data)
    gps.send_at_command("AT+UMSM?")

    # Setup Bluetooth module name
    gps.send_at_command("AT+UBTLN={}".format("GSFGPS_BT_0001"))
    # Query Bluetooth module name
    gps.send_at_command("AT+UBTLN?")

    # Store the current configuration to the Bluetooth. Need the AT+CPWROFF command to write it in non-volatile memory
    gps.send_at_command("AT&W0")
    # Reboot the module and store the settings in non-volatile memeory
    gps.send_at_command("AT+CPWROFF")

    # Send test AT command to verify command mode
    gps.send_at_command("AT")
    # Switch back to Data mode for normal GPS operation
    gps.enter_data_mode()
    # Set DTR pin to False
    gps.set_dtr(True)
    # Close serial port and release resources
    gps.close()
