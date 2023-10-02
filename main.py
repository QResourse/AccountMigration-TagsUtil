import Config as Conf
import Lib.Functions as Func
import pandas as pd 
import xml.etree.ElementTree as Xet
from lxml import etree



# WriteFlag = True

SRC_BASE = Conf.SOURCE_base
REQUEST_URL = SRC_BASE + "/qps/rest/2.0/search/am/tag"
header = Func.getXmlHeader(Conf.SOURCE_USERNAME,Conf.TARGET_PASSWORD)
payload = {}


response = Func.postRequest(REQUEST_URL,payload,header)
if (response.ok != True):
      print("Failed to get response from API")
      exit()

with open(Conf.RESPONSEXML, "w") as f:
    f.write(response.text.encode("utf8").decode("ascii", "ignore"))
    f.close()

#This is an array with all the responses 
RESPONSE_FILEARRAY =  Func.pocessHostRequests(header,Conf.RESPONSEXML,REQUEST_URL)
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
  tagsArray = []
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



      ########################################################
      #### Writing the tags to new system