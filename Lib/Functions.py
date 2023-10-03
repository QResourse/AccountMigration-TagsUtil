import requests
import xml.etree.ElementTree as Xet
from lxml import etree
import base64
from datetime import timedelta, date
import os as _os
import pandas as pd 
import shutil as SU

#collecting data from XML 
def tryToGetAttribute(Object,inputString):
    try:
        output = Object.find(inputString).text
    except:
        output = {"Null"}
    return output

#collecting data from XML 
def tryToGetObj(Object,inputString):
    try:
        output = Object.find(inputString)
    except:
        output = {"Null"}
    return output


#used to get the access token
def getToken(USERNAME,PASSWORD):
    AuthStringRaw = USERNAME+":"+PASSWORD
    base64_bytes = AuthStringRaw.encode("ascii")
    authtoken = base64.b64encode(base64_bytes)
    base64_authtoken = authtoken.decode("ascii")
    return base64_authtoken

##Override - Delete - remove the False=True option
def getXmlHeader(USERNAME={},PASSWORD={}):
    headers = {
    "Content-Type": "application/xml",
    "Accept": "application/xml",
    "X-Requested-With": "QualysPostman",
    "Authorization": "Basic "+getToken(USERNAME,PASSWORD)
    }
    return headers


#Used to get the header of the request
def getHeader(USERNAME,PASSWORD):
    headers = {
    "X-Requested-With": "QualysPostman",
    "Authorization": "Basic "+getToken(USERNAME,PASSWORD)
    }
    return headers


#Used to Post requests
def postRequest(URL,payload,headers,files=[]):
    print("POSTING to "+ URL)
    try:
        response = requests.request("POST", URL, headers=headers, data=payload, files=files)
    except:
        print("Failed to send request to API")
        return str(response.status_code)
    else:
        return  response


def getRequest(URL,payload,headers,files=[]):
    print("POSTING to "+ URL)
    try:
        response = requests.request("GET", URL, headers=headers, data=payload, files=files)
    except:
        print("Failed to send request to API")
    else:
        return  response



def deleteTempFiles(files):
    for file in files:
        if _os.path.exists(file):
            _os.remove(file)



def checkForMoreRecordsBool(RESPONSEXML):
    with open(RESPONSEXML, "r") as f:
        xml = f.read()
        f.close()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    recordCount = root.find("count")
    if (type(recordCount)!=None.__class__):
            return root.find("hasMoreRecords").text

    

def checkForMoreHostRecords(RESPONSEXML):
    with open(RESPONSEXML, "r") as f:
        xml = f.read()
        f.close()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    recordCount = root.find("count")
    if (type(recordCount)!=None.__class__):
        recordCountText = root.find("count").text
        if(int(recordCountText) > 0):  
            Data = root.find("lastId")
            return str(Data.text)
    else:
        return str(0)



def pocessHostRequests(header,RESPONSEXML,URL):
    RESPONSE_FILEARRAY = []
    index = 1
    print(str(index))
    while(checkForMoreRecordsBool(RESPONSEXML)=='true'):
        if (index == 1):
            filename = "Response_" + str(index)+".xml"
            newFile =_os.path.join("Requests",filename)
            SU.copyfile(RESPONSEXML, newFile)
            RESPONSE_FILEARRAY.append(newFile)
            index+=1
        lastId = checkForMoreHostRecords(RESPONSEXML)
        payload = "<ServiceRequest>\r\n    <filters>\r\n        <Criteria field=\"id\" operator=\"GREATER\">"+str(lastId)+"</Criteria>\r\n    </filters>\r\n</ServiceRequest>"
        response = postRequest(URL,payload,header)
        if(response.status_code == 200):
            with open(RESPONSEXML, "w") as f:
                f.write(response.text.encode("utf8").decode("ascii", "ignore"))
                f.close()
            filename = "Response_" + str(index)+".xml"
            newFile =_os.path.join("Requests",filename)
            SU.copyfile(RESPONSEXML, newFile)
            RESPONSE_FILEARRAY.append(newFile)
            if(checkForMoreRecordsBool(RESPONSEXML)):
                index+=1
            else:
                break
    print(RESPONSE_FILEARRAY)
    return RESPONSE_FILEARRAY