# -*- coding: utf-8 -*-
"""
Spyder Editor

New XML parsing script

"""

# Libraries that are used in this script

import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree as et

# File location, change this as needed
os.chdir(r"C:\Users\hkopansk\OneDrive - Biogen\Documents\Python Data")

# Reads in the XML file
tree = et.parse('biib121.xml')
root = tree.getroot()

# Initial View (not really needed)
for i in root:
    print(i.tag, i.attrib)
    
# Lists to hold parsed values        
block_list = []
break_list = [] 
instruction_list = []       
parameter_list = []
parameter_value = []

# Parsing happens here
# Reads into each level of the XML file
# Changes here can break the code, use caution

for blocks in root.iter('Blocks'):
    for block in blocks.iter('Block'):
        for bInstrucs in block.iter('BlockInstructions'):
            for bInstruc in bInstrucs.iter('BlockInstruction'):
                for stratInstruc in bInstruc.iter('StrategyInstruction'):                  
                    for stratParam in stratInstruc.iter('StrategyParameter'):
                        instruction_list.append(stratInstruc.find('InstructionName').text)
                        block_list.append(block.find('BlockName').text)
                        break_list.append(bInstruc.find('BreakPointValue').text)
                        parameter_list.append(stratParam.find('ParameterName').text)
                        parameter_value.append(stratParam.find('ParameterValue').text)

# Combines information into data frame       
df_method = pd.DataFrame({"Blocks": block_list,
                           "Instruction": instruction_list,
                           "Break Points": break_list,
                           "Parameters" : parameter_list, 
                           "Values" : parameter_value})

# Push out data frame to csv file
# Rename file output as needed
df_method.to_csv('BIIB121_parameter_list.csv')


# Extra stuff
# Changing datatype in data frame column
df_method.loc[:,'Break Points'] = df_method.loc[:,'Break Points'].astype('double')

# Example of filtering all rows that contain a non zero break point and sending it to a new dataframe.
df_nonzero = df_method[df_method.loc[:,'Break Points'] != 0]

