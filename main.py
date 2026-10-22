# Import the custom GPS serial communication class
from PyGSFGPSSerial import *

# User settings
COM_PORT = "COM3"
BLUETOOTH_MODULE_NAME = "GSF_GEO_BT_0001"
IS_THIS_A_GSF_GEO_NEW_GENERATION = False

# Using the following for the initial configuration. If you program the new GSF GEO
#   with IS_THIS_A_GSF_GEO_NEW_GENERATION = True, then the BT won't use RTS/CST. Then set USING_BT_RTS_CTS = False
USING_BT_RTS_CTS = True

############################################################################################
# CODE BEGIN BELOW, DO NOT EDIT THE LINES BELOW.
############################################################################################

# Initialize GPS module on COMx port
gps = PyGSFGPSSerial(port=COM_PORT,rtscts=USING_BT_RTS_CTS)

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

    # Send test AT command to verify everything is okay
    gps.send_at_command("AT")

    if IS_THIS_A_GSF_GEO_NEW_GENERATION:
        # Program the Bluetooth module at 115200 bauds, NO FLOW CONTROL
        # The 2nd parameter is flow control: 1=CTS/RTS (Default), 2=No Flow Control
        # The last parameter is to apply the change instantly or at the next reset: 0=Next reset, 1=Instantly
        gps.send_at_command("AT+UMRS={}".format("115200,2,8,1,1,0"))
        gps.send_at_command("AT+UMRS?")

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
