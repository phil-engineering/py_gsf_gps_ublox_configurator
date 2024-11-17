import serial
from time import sleep
from typing import Optional, Union

WRITE_ECHO = True

class PyGSFGPSSerial:
    """
    A class to handle serial communication with GPS devices.

    Attributes:
        port (str): The COM port identifier
        baudrate (int): The communication speed
        rtscts (bool): Hardware flow control flag
        timeout (float): Read timeout in seconds
        serial_port (serial.Serial): Serial port object
    """

    def __init__(self, port: str = 'COM6',
                 baudrate: int = 115200,
                 rtscts: bool = True,
                 timeout: float = 1.0):
        """
        Initialize the GPS serial communication.

        Args:
            port (str): COM port identifier (default: 'COM6')
            baudrate (int): Communication speed (default: 115200)
            rtscts (bool): Hardware flow control flag (default: True)
            timeout (float): Read timeout in seconds (default: 1.0)
        """
        self.port = port
        self.baudrate = baudrate
        self.rtscts = rtscts
        self.timeout = timeout
        self.serial_port = None

    def open(self) -> bool:
        """
        Open the serial port connection.

        Returns:
            bool: True if port opened successfully, False otherwise
        """
        try:
            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                rtscts=self.rtscts,
                timeout=self.timeout
            )
            return self.serial_port.is_open
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            return False

    def close(self) -> None:
        """Close the serial port connection."""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()

    def read(self) -> Optional[str]:
        """
        Read data from the serial port until no more data is available.

        Returns:
            Optional[str]: The received data as a string, or None if read failed
        """
        if not self.serial_port or not self.serial_port.is_open:
            print("Serial port is not open")
            return None

        try:
            received_data = ""
            while True:
                data = self.serial_port.read(1)
                if data:
                    received_data += data.decode("utf-8")
                else:
                    break
            print("Receiving from uBlox: {}".format(received_data))
            return received_data
        except Exception as e:
            print(f"Error reading from serial port: {e}")
            return None

    def write(self, data: Union[str, bytes]) -> bool:
        """
        Write data to the serial port.

        Args:
            data (Union[str, bytes]): Data to write to the serial port

        Returns:
            bool: True if write was successful, False otherwise
        """
        if not self.serial_port or not self.serial_port.is_open:
            print("Serial port is not open")
            return False

        try:
            if WRITE_ECHO:
                print("Sending to uBlox: {}".format(data))
            if isinstance(data, str):
                data = data.encode()
            self.serial_port.write(data)
            return True
        except Exception as e:
            print(f"Error writing to serial port: {e}")
            return False

    def set_dtr(self, state: bool) -> bool:
        """
        Set the DTR pin state.

        Args:
            state (bool): True for 0V (DTR True), False for 3.3V (DTR False)

        Returns:
            bool: True if DTR was set successfully, False otherwise
        """
        if not self.serial_port or not self.serial_port.is_open:
            print("Serial port is not open")
            return False

        try:
            self.serial_port.setDTR(state)
            return True
        except Exception as e:
            print(f"Error setting DTR state: {e}")
            return False

    def enter_command_mode(self) -> bool:
        """
        Enter command mode by sending '+++' sequence.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.write('+++')
            sleep(2)  # Wait for command mode
            return True
        except Exception as e:
            print(f"Error entering command mode: {e}")
            return False

    def send_at_command(self, command: str) -> Optional[str]:
        """
        Send an AT command and return the response.

        Args:
            command (str): AT command to send

        Returns:
            Optional[str]: Response from the device or None if failed
        """
        if not command.endswith('\r\n'):
            command += '\r\n'

        if self.write(command):
            sleep(0.1)  # Wait for response
            return self.read()
        return None

    def exit_command_mode(self) -> bool:
        """
        Exit from AT command mode and return to data mode in the uBlox GPS module.

        This function:
        1. Sends the 'ATO' command to switch from command mode back to data mode
        2. Waits for the mode transition to complete
        3. Confirms the successful mode change

        Returns:
            bool: True if successfully switched to data mode, False if an error occurred
        """
        # Check if serial port is available and open
        if not self.serial_port or not self.serial_port.is_open:
            print("Serial port is not open")
            return False

        try:
            # Send 'ATO' (AT Online) command to switch back to data mode
            # This command tells the module to exit command mode and resume normal operation
            self.send_at_command("ATO")

            # Wait 500ms for the mode switch to complete
            # This delay is necessary to ensure the module has time to change modes
            sleep(0.5)

            # Notify user of successful mode change
            print("***** uBlox is now in Data mode *****")

            return True
        except Exception as e:
            # Log any errors that occur during the mode change
            print(f"Error setting DTR state: {e}")
            return False

    def exit_data_mode(self) -> bool:
        """
        Exit from data mode and enter AT command mode in the uBlox GPS module.

        This function:
        1. Sends the escape sequence '+++' to initiate command mode
        2. Waits for the mode transition
        3. Clears any pending data in the buffer
        4. Confirms the successful mode change

        Returns:
            bool: True if successfully switched to command mode, False if an error occurred
        """
        # Check if serial port is available and open
        if not self.serial_port or not self.serial_port.is_open:
            print("Serial port is not open")
            return False

        try:
            # Send '+++' escape sequence to enter command mode
            # This is a standard Hayes command set sequence to switch from data to command mode
            self.write("+++")

            # Wait 500ms for the escape sequence to be processed
            # This delay is crucial as the module needs time to recognize the escape sequence
            sleep(0.5)

            # Clear any pending data in the receive buffer
            # This ensures we start with a clean state in command mode
            self.read()

            # Additional 250ms wait to ensure stable command mode
            # This helps prevent any timing-related issues with subsequent commands
            sleep(0.25)

            # Notify user of successful mode change
            print("***** uBlox is now in Command mode *****")

            return True
        except Exception as e:
            # Log any errors that occur during the mode change
            print(f"Error setting DTR state: {e}")
            return False