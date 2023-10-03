
import Lib.Functions as Func
import xml.etree.ElementTree as Xet
from lxml import etree
import time
import os





def getTags(SRC_BASE,SOURCE_USERNAME,SOURCE_PASSWORD,RESPONSEXML):
    REQUEST_URL = SRC_BASE + "/qps/rest/2.0/search/am/tag"
    header = Func.getXmlHeader(SOURCE_USERNAME,SOURCE_PASSWORD)
    payload = {}

    response = Func.postRequest(REQUEST_URL,payload,header)
    if (response.ok != True):
        tree = Xet.ElementTree(Xet.fromstring(response.text))
        root = tree.getroot()
        errorDetails = root.find('responseErrorDetails')
        responseCode = root.find('responseCode')
        errorMessage = Func.tryToGetAttribute(errorDetails,'errorMessage')
        print("Failure: " +errorMessage)
        print("Error: " +str(responseCode.text))
    else:
        print("Success: "+"Posting to "+ REQUEST_URL)
        with open(RESPONSEXML, 'w', encoding="utf-8") as f:
            f.write(response.text)
            f.close()

    RESPONSE_FILEARRAY =  Func.pocessHostRequests(header,RESPONSEXML,REQUEST_URL)
    return RESPONSE_FILEARRAY

def processTagsResponse(RESPONSE_FILEARRAY):
    #processing the XML
    counter = 0
    for fileObj in RESPONSE_FILEARRAY:
        with open(fileObj, "r") as f:
            xml = f.read()
            f.close()
    parser = etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    root = etree.fromstring(xml.encode('utf-8'), parser=parser)
    data = root.find("data")
    tags = data.findall("Tag")
    for tag in tags:
        ServiceRequest = Xet.Element('ServiceRequest')
        Name = Func.tryToGetAttribute(tag,"name")
        Data = Xet.SubElement(ServiceRequest,"data")
        Tag =  Xet.SubElement(Data,"Tag")
        ruleText = tag.find('ruleText')
        ruleType = tag.find('ruleType')
        if((type(ruleText)!=None.__class__) and((type(ruleType)!=None.__class__))):
            ruleTextObj = Xet.SubElement(Tag,"ruleText")
            ruleTypeObj = Xet.SubElement(Tag,"ruleType")
            ruleTextObj.text = ruleText.text
            ruleTypeObj.text = ruleType.text
        ServiceRequestName = Xet.SubElement(Tag,"name")
        ServiceRequestName.text = Name
        ChildrenTags = tag.find("children")
        if (type(ChildrenTags)!=None.__class__):
            #service request build
            Children = Xet.SubElement(Tag,"children")
            list = Xet.SubElement(Children,"set")
            childTagList = ChildrenTags.find("list")
            childTags = childTagList.findall("TagSimple")
            print("child tag")
            for child in childTags:
                TagInner = Xet.SubElement(list,"Tag")
                TagInnerName = Xet.SubElement(TagInner,"name")
                CName = Func.tryToGetAttribute(child,"name")
                TagInnerName.text = CName 
                ChildRuleText = child.find('ruleText')
                ChildRuleType = child.find('ruleType')
                if((type(ChildRuleText)!=None.__class__) and ((type(ChildRuleType)!=None.__class__))):
                    ruleTextObj = Xet.SubElement(TagInner,"ruleText")
                    ruleTypeObj = Xet.SubElement(TagInner,"ruleType")
                    ruleTextObj.text = ChildRuleText.text
                    ruleTypeObj.text = ChildRuleType.text
                print(CName + " " + str(counter))
        else:
            print(Name + " " + str(counter))
        counter+=1
        tree = Xet.ElementTree(ServiceRequest)
        tree.write('XMLs\\Requests\\Request_'+str(counter)+'_'+".xml",encoding='UTF-8',xml_declaration=True)

def setTags(TGT_BASE,TARGET_USERNAME,TARGET_PASSWORD):
    REQUEST_URL = TGT_BASE + "/qps/rest/2.0/create/am/tag"
    header = Func.getXmlHeader(TARGET_USERNAME,TARGET_PASSWORD)
    path = "XMLs\\Requests\\"
    filesArray =[]
    for file in os.listdir(path):
        if file.endswith(".xml"):
            filesArray.append(file)
    errorArray =[]
    for file in filesArray:
        path = "XMLs\\Requests\\"+file
        with open(path, "r") as f:
            time.sleep(5)
            xml = f.read()
            f.close()
            response = Func.postRequest(REQUEST_URL,xml,header)
            newIndex = filesArray.index(file)
            if (response.ok != True):   
                tree = Xet.ElementTree(Xet.fromstring(response.text))
                root = tree.getroot()
                errorDetails = root.find('responseErrorDetails')
                responseCode = root.find('responseCode')
                errorMessage = Func.tryToGetAttribute(errorDetails,'errorMessage')
                print("Failure: " +errorMessage)
                print("Error: " +str(responseCode.text))
                errorArray.append(file)
            else:
                print("Success tag created")
            print("Path: " + path)
            filesArray.pop(newIndex)
    return {"errors" : errorArray,"Files" : filesArray }
