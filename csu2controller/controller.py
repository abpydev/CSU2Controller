"""
This module provides a python API to communicate with the 
following device : 

    -   Control and Supply Unit 2 (CSU2) of IFG Institute for 
    Scientific Instruments GmbH 

It is based on the manufacturer documentation dated to 2016-03-21
"""

# Built-in imports
import socket
from typing import Literal

class CSU2Controller:
    """This class is a controller for communication with the CSU2 unit"""

    def __init__(self, ip_address='192.168.1.3', port=23):
        self.ip_address = ip_address
        self.port = port
        self.socket = None

    def connect(self):
        """Connect to the CSU2 device."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip_address, self.port))
        print(f"Connected to CSU2 at {self.ip_address}:{self.port}")

    def disconnect(self):
        """Disconnect from the CSU2 device."""
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Disconnected from CSU2.")

    def send_command(self, command):
        """Send a command to the CSU2 device and return the response."""

        try : 
            # Send the command with a carriage return
            self.socket.sendall(f"${command}\r".encode('ascii'))

            # Receive the response
            response = self.socket.recv(1024).decode('ascii')
            return response

        except OSError as oserr: 
            raise ConnectionError("Not connected to the CSU2 device.") from oserr
        except AttributeError :
            raise ConnectionError("Not connected to the CSU2 device.")

    def query_ok(self):
        """Query system time since power-on."""
        response = self.send_command("OK")
        return response.strip('!OK').strip()

    def power_hv(self, state):
        """Power on/off the high voltage generator."""
        if state not in ['ON', 'NO', '+', '-']:
            raise ValueError("Invalid state. Use 'ON', 'NO', '+', or '-'.")
        response = self.send_command(f"HV {state}")
        return response.strip('!HV').strip()

    def skip_warmup(self):
        """Skip warm-up of the tube."""
        response = self.send_command("HVW-")
        return response.strip('!HVW-').strip()

    def set_last_used_time(self, timestamp):
        """Set the last time the tube was used."""
        response = self.send_command(f"HVWP {timestamp}")
        return response.strip('!HVWP').strip()

    def query_last_warmup_time(self):
        """Query last time the tube was warmed-up."""
        response = self.send_command("HVW?")
        return response.strip('!HVW?').strip()

    def set_hv_voltage(self, voltage):
        """Set the high voltage of the HV generator."""
        response = self.send_command(f"HVUP {voltage}")
        return response.strip('!HVUP').strip()

    def set_hv_current(self, current):
        """Set the anode current of the HV generator."""
        response = self.send_command(f"HVIP {current}")
        return response.strip('!HVIP').strip()

    def set_filament_current_limit(self, current_limit):
        """Set filament current limit (maximum) of HV generator

        (Controlled automatically after $HV+ and until first 
        use of this command)"""
        response = self.send_command(f"HVHP {current_limit}")
        return response.strip('!HVHP').strip()

    def query_actual_voltage(self):
        """Query actual voltage of HV generator"""
        response = self.send_command(f"HVU?")
        return response.strip('!HVU?').strip()

    def query_actual_anode_current(self):
        """Query actual anode current of HV generator"""
        response = self.send_command(f"HVI?")
        return response.strip('!HVI?').strip()

    def query_actual_filament_current(self):
        """Query actual filament current of HV generator"""
        response = self.send_command(f"HVH?")
        return response.strip('!HVH?').strip()

    def query_actual_state_hv(self):
        """Query actual state of HV generator"""
        response = self.send_command(f"HV??")
        return response.strip('!HV??').strip()

    def query_error_code(self):
        """Query error code"""
        response = self.send_command(f"HV?1")
        return response.strip('!HV?1').strip()

    def query_max_current(self):
        """Query maximum measured current of HV generator"""
        response = self.send_command(f"FH")
        return response.strip('!FH').strip()

    def query_max_voltage(self):
        """Query maximum measured voltage of HV generator"""
        response = self.send_command(f"FU")
        return response.strip('!FU').strip()

    def open_shutter(self, is_open: Literal['ON', 'NO', '+', '-']):
        """Open/Close the shutter"""
        response = self.send_command(f"XR {is_open}")
        return response.strip('!XR').strip()

    def query_shutter_state(self):
        """Query shutter state"""
        response = self.send_command(f"XR?")
        return response.strip('!XR').strip()

    def query_remote_mode(self):
        """Query remote mode"""
        response = self.send_command(f"RM?")
        return response.strip('!RM').strip()

    def query_selected_tube_index(self):
        """Query index of selected tube type"""
        response = self.send_command(f"TTI?")
        return response.strip('!TTI?').strip()

    def set_tube_type_by_index(self, index):
        """Set tube type by index"""
        response = self.send_command(f"TTIP {index}")
        return response.strip('!TTI?').strip()

    def query_number_of_tube_types(self):
        """Query number of known tube types"""
        response = self.send_command(f"TT#?")
        return response.strip('!TT#?').strip()

    def query_caption_of_tube_at_index(self, index):
        """Query caption of tube type at index ix"""
        response = self.send_command(f"TTLP {index}")
        return response.strip('!TTLP').strip()

    def program_string(self, position, string):
        """Program a string"""
        response = self.send_command(f"RKPP {position} {string}")
        return response.strip('!RKPP').strip()

    def read_string_from_pos(self, position):
        """Read string from position"""
        response = self.send_command(f"RKLP {position}")
        return response.strip('!RKLP').strip()

    def program_pair_of_words(self, position, value1, value2):
        """Program pair of words"""
        response = self.send_command(f"RKPB {position} {value1} {value2}")
        return response.strip('!RKPB').strip()

    def read_pair_of_words(self, position):
        """Read pair of words from position"""
        response = self.send_command(f"RKLB {position}")
        return response.strip('!RKLB').strip()

    def set_realtime_clock(self, cmd):
        """Set realtime clock

            cmd = time as YYYY-MM-DD-hh:mm:ss"""
        response = self.send_command(f"RKTP {cmd}")
        return response.strip('!RKTP').strip()

    def query_realtime_clock(self):
        """Query realtime clock"""
        response = self.send_command(f"RKOK")
        return response.strip('!RKOK').strip()

    def query_tube_temperature(self):
        """Query tube temperature"""
        response = self.send_command(f"RKR?")
        return response.strip('!RKR?').strip()

    def query_hv_gen_temperature(self):
        """Query temperature of HV generator (SIC)"""
        response = self.send_command(f"RKT?")
        return response.strip('!RKT?').strip()

    def query_led_board_temperature(self):
        """Query temperature of LED board (PT100)"""
        response = self.send_command(f"RKL?")
        return response.strip('!RKL?').strip()

    def query_shutter_board_temperature(self):
        """Query temperature of shutter board (PT100)"""
        response = self.send_command(f"RKS?")
        return response.strip('!RKS?').strip()

    def query_max_tube_temperature(self):
        """Query maximum tube temperature"""
        response = self.send_command(f"RKRX?")
        return response.strip('!RKRX?').strip()

    def query_min_tube_temperature(self):
        """Query minimum tube temperature"""
        response = self.send_command(f"RKRN?")
        return response.strip('!RKRN?').strip()

    def query_max_hv_gen_temperature(self):
        """Query maximum temperature of HV generator"""
        response = self.send_command(f"RKCX?")
        return response.strip('!RKCX?').strip()

    def query_min_hv_gen_temperature(self):
        """Query minimum temperature of HV generator"""
        response = self.send_command(f"RKCN?")
        return response.strip('!RKCN?').strip()

    def query_sn_and_secops(self):
        """Query serial numbers / seconds of operation"""
        response = self.send_command(f"RKID?")
        return response.strip('!RKID?').strip()

    def query_fw_version(self):
        """query fimware version"""
        response = self.send_command(f"XV")
        return response.strip('!XV').strip()

    def reset_programmed_parameters(self):
        """reset programmed parameters"""
        response = self.send_command(f"<<")
        return response.strip('!<<').strip()

    def query_param_version(self):
        """Query parameter version (number and type)"""
        response = self.send_command(f"R#0")
        return response.strip('!R#9999').strip()

class CSU2AnswerError(Exception):

    """Exception to handle error responses from the CSU2"""

    def __init__(self, command, answer) -> None:
        super().__init__()
        self.__answer = answer
        self.__command = command
        text = f'Command {self.__command} to CSU failed with answer : {self.__answer}'
        super().__init__(text)

    @property
    def command(self)
        return self.__command

    @property
    def answer(self)
        return self.__answer
