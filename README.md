#Tag migration utilitiy 

##This code is used to get all the source account tags and create the XML service request payloads to create each tag. 

All your tags from the source account will be found under the ***\Requests*** folder.

All the payloads are located under ***XMLs\Requests***.

## Requirments

1. python 3.8+
2. [pip package manager](https://pip.pypa.io/en/stable/installation/)

### Install packages with pip: -r requirements.txt
pip install -r requirements.txt
### Edit config
Rename the file config.xml.sample to config.xml
Change the **BASE_URL** to the correct platfrom. See [platform-identification](https://www.qualys.com/platform-identification/)
Change the **USERNAME** and **PASSWORD** information


## Release Notes
1.0.0 - Innitial release;