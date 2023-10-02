import pandas as pd 
import Lib.Functions as Func
import os

df = pd.read_xml('config.xml')
configList = df.iloc[0].to_list()
SOURCE_base = configList[0]
SOURCE_USERNAME = configList[1]
SOURCE_PASSWORD = configList[2]

TARGET_base = configList[3]
TARGET_USERNAME = configList[4]
TARGET_PASSWORD  = configList[5]
###Change the environment POD

RESPONSEXML = os.path.join("Requests","Response.xml")
