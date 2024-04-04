#Dict containing all sensor conversion data

# Define Parameters
# define encoder sensor parameters
delta_t = 0.1 # inverse of the encoder sample rate configured in DAQami
tick_count = 2048 # number of ticks in one revolution
revs_per_tick = 1 / tick_count # revolutions per tick
gear_ratio = 3


def convert_temp(raw_temp): #Output in degrees C
    measured_temp = round(abs(raw_temp) * 100 - 273.15) # conversion equation: 
    return measured_temp

def convert_voltage(raw_voltage):
    measured_voltage = round(3.125 * (abs(raw_voltage) / 250) * 1000 - 12.5, 2) # conversion equation: 3.125[V/mA] * (V_sensed / R) * 10^3 - 12.5V = Voltage[V]
    return measured_voltage
    
def convert_current(raw_current):
    measured_current = round((3.125 * (abs(raw_current) / 250) * 1000 - 12.5), 2) # conversion equation: 3.125[A/mA] * (V_sensed[V] / R[ohms]) * 10^3 - 12.5[A] = Amperage[A]
    return measured_current

def convert_torque(raw_torque):
    measured_torque = (round(abs(raw_torque) * 10 / gear_ratio, 2)) # conversion equation: (V_sensed[V] * 10[Nm/V]) = Torque[Nm]
    return measured_torque




