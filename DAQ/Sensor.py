#!/usr/bin/env python
#  -*- coding: utf-8 -*-


#This is for looking at single port testing on the DAQ HAT

"""
    MCC 128 Functions Demonstrated:
        mcc128.a_in_read
        mcc128.a_in_mode_write
        mcc128.a_in_range_write

    Purpose:
        Read a single data value for each channel in a loop.

    Description:
        This example demonstrates acquiring data using a software timed loop
        to read a single value from each selected channel on each iteration
        of the loop.
"""
from __future__ import print_function
from time import sleep
from sys import stdout
from daqhats import mcc128, OptionFlags, HatIDs, HatError, AnalogInputMode, \
    AnalogInputRange
from daqhats_utils import select_hat_device, enum_mask_to_string, \
    input_mode_to_string, input_range_to_string
import csv
from Sensor_Conversion import *

# Constants
chan0 = []
chan1 = []
chan2 = []
chan3 = []
chan4 = []
chan5 = []
header = ['Torque (Nm)', 'Temp1 (V)', 'Voltage', 'Current', 'Temp2 (V)', 'Water Sensor']

def run():
    """
    This function is executed automatically when the module is run directly.
    """
    options = OptionFlags.DEFAULT
    low_chan = 0
    high_chan = 5
    input_mode = AnalogInputMode.SE
    input_range = AnalogInputRange.BIP_10V


    mcc_128_num_channels = mcc128.info().NUM_AI_CHANNELS[input_mode]
    sample_interval = 0.25  # Seconds

    # Ensure low_chan and high_chan are valid.
    if low_chan < 0 or low_chan >= mcc_128_num_channels:
        error_message = ('Error: Invalid low_chan selection - must be '
                            '0 - {0:d}'.format(mcc_128_num_channels - 1))
        raise Exception(error_message)
    if high_chan < 0 or high_chan >= mcc_128_num_channels:
        error_message = ('Error: Invalid high_chan selection - must be '
                            '0 - {0:d}'.format(mcc_128_num_channels - 1))
        raise Exception(error_message)
    if low_chan > high_chan:
        error_message = ('Error: Invalid channels - high_chan must be '
                            'greater than or equal to low_chan')
        raise Exception(error_message)

    # Get an instance of the selected hat device object.
    address = select_hat_device(HatIDs.MCC_128)
    hat = mcc128(address)

    hat.a_in_mode_write(input_mode)
    hat.a_in_range_write(input_range)

    print('\nMCC 128 single data value read example')
    print('    Functions demonstrated:')
    print('         mcc128.a_in_read')
    print('         mcc128.a_in_mode_write')
    print('         mcc128.a_in_range_write')
    print('    Input mode: ', input_mode_to_string(input_mode))
    print('    Input range: ', input_range_to_string(input_range))
    print('    Channels: {0:d} - {1:d}'.format(low_chan, high_chan))


    # Display the header row for the data table.
    # print('\n  Samples/Channel', end='')
    # for chan in range(low_chan, high_chan + 1):
    #     print('     Channel', chan, end='')
    # print('')

    samples_per_channel = 0
    while samples_per_channel<10:
        # Display the updated samples per channel count
        samples_per_channel += 1
        #print('\r{:17}'.format(samples_per_channel), end='')

        # Read a single value from each selected channel.
        for chan in range(low_chan, high_chan + 1):
            value = hat.a_in_read(chan, options)
            if chan == 0: #Torque - This is CH0H on DAQ
                chan0.append(convert_torque(value)) 
            elif chan == 1: #Temp 1 - This is CH1H on DAQ
                chan1.append(convert_temp(value))
                print(value)
            elif chan == 2: #Voltage - This is CH2H on DAQ
                chan2.append(convert_voltage(value))
            elif chan == 3: # Current - This is CH3H on DAQ
                chan3.append(convert_current(value))
            elif chan == 4: # Temp 2 - This is CH0L on DAQ
                chan4.append(convert_voltage(value)) 
            elif chan == 5: # Water Sensor - This is CH1L on DAQ
                chan5.append(value)


            #print('{:12.5} V'.format(value), end='')
            #print(chan0)
            #print(chan1)

        stdout.flush()

        # Wait the specified interval between reads.
        sleep(sample_interval)

def create_csv_file(filename, headers, *data):
    """
    Creates a CSV file with given filename, headers, and data.
    
    Args:
        filename (str): Name of the CSV file to be created.
        headers (list): List containing headers for the CSV file.
        *data: Variable length argument containing arrays of data.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        # Zip data arrays together to iterate over them simultaneously
        for row in zip(*data):
            writer.writerow(row)

run()

create_csv_file('output.csv', header, chan0, chan1, chan2, chan3, chan4, chan5)