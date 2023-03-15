#Author: Logan Gleason
#Parse nmap output to dataframe

import os
import pandas as pd
import xml.etree.ElementTree as xet

def portScan(target,ports): #Scan subnet using nmap bash rc
   os.system(f"sudo nmap -oX scan.xml -sC -sV {target} -p {ports}") #Scan using nmap

def parseXML(xmlFile):
    '''
    Parse xml file to xml element tree, then parse element tree to nested dictionaries
    and return those dictionaries
    Input: XML file
    Output: Python Nested Dictionary
    '''
    xtree = xet.parse(xmlFile) #Parse xml tree from file
    xroot = xtree.getroot() #Get root of xml ElementTree obj
    xdict = {}              #Init empty dict

    for node in xroot.iter():#Top down iterate through ElemenTree
        xdict[node.tag] = node.attrib#Set key to be node tag, and the value to be attrib dictionary

    return xdict

def flattenDictionary(nest):
    '''
    Take a nested dictionary of arbitraty depth and flatten the nested keys
    to a tuple chain.
    Input: Nested Dictionary object
    Output: Flattened Dictionary of tuple chains from nested keys
    '''
    out = {} #init return dict

    if isinstance(nest, dict): #if obj is dict
        for x in nest: #iterate through elements of dict
            flattened = flattenDictionary(nest[x]) #recur
            for key, value in flattened.items(): #iterate through key/value pairs
                key = list(key) #key to list
                key.insert(0, x) #insert parent key at 0
                out[tuple(key)] = value #tuple chain using key list and values
    else:
        out[()] = nest

    return out

def constructDataFrame(xml_file):
    '''
    Construct a DataFrame object using xml parser, and dictionary flattener.
    Input: xml file
    Output: Pandas DataFrame Object
    '''
    flattened_dict = flattenDictionary(parseXML(xml_file)) #Get flattened dictionary by calling functions
    df = pd.DataFrame.from_dict(flattened_dict, orient = 'index') #construct dataframe from dictionary
    df.index = pd.MultiIndex.from_tuples(df.index) #Set multiindexing for dictionary
    df = df.unstack(level=-1) #Flatten Dataframe
    df.columns = df.columns.map("{0[1]}".format) #Set format map for dataframe and add columns
    return df.dropna(how='all') #remove rows that contain no values

def __main__():
    target = input("Please enter subnet or subnet range to be scanned: ")
    ports = input("Please enter port range to be scanned: ")
    portScan(target,ports)
    df = constructDataFrame("scan.xml")
    df.to_excel("scan.xlsx")

    
if __name__ == "__main__":
    __main__()
