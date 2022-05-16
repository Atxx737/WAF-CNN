import linecache
import json
# def lineIsPostData(line):
DATASET_FILE='anomalousTrafficTest.txt'
DICTIONARY_FILE='dictionary.json'
CLEANED_DATASET_FILE='cleanedDataset.txt'
FULL_PAYLOAD_FILE='payload.txt'
def cleanDataSet(dataFile):
    dataSet = open(dataFile, 'r')
    cleanedDataset = open(CLEANED_DATASET_FILE, 'w')
    lineIndex = 1
    for line in dataSet:
        if line.startswith("GET"):
            cleanedDataset.write(line)
            lineIndex +=1
        elif line.startswith("POST"):
            postData = linecache.getline(dataFile, lineIndex + 14)
            cleanedDataset.write(line[:-10]+"?" +postData)
            lineIndex +=1
        else:
            lineIndex += 1
    dataSet.close()
    cleanedDataset.close

def write_json(new_data, filename, keyApend):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data[keyApend].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

def checkPayloadIsExist(payload, dic_file):
    dictionary = json.load(dic_file)
    for key in dictionary["dictionary"][0]:
        if key["payload"] == payload:
            return true
        else:
            return false
def splitString(requestLink,charSplit):
    temp_pay = requestLink.split(charSplit)
    return temp_pay
    # createDictionary(CLEANED_DATASET_FILE)
    
def getFullPayload():
    cleanDataSet(DATASET_FILE)
    dataSet = open(CLEANED_DATASET_FILE, 'r')
    for line in dataSet:
        temp_formater = splitString(line,'?')
        payload_formated=''
        try:
            payload_formated=temp_formater[1]
            if (payload_formated.endswith("HTTP/1.1\n")):
                payload_formated = payload_formated[:-10]
        except IndexError:
            pass
        payloadFile = open(FULL_PAYLOAD_FILE, 'a')
        payloadFile.write(payload_formated)
        payloadFile.close()
    dataSet.close()

# def createDictionary(fpayload):
#     dictionary = json.load(DICTIONARY_FILE)
#     dataSet = open(CLEANED_DATASET_FILE, 'r')
#     for line in dataSet:
#         payload = getFullPayload(line)

#     for payload in dictionary["dictionary"][0]:
#         if payload["payload"]
#     appendData = {"dictionaryID": "1",
#         "payload": "example",
#         "dictionaryFrequency": 100
#     }
#     write_json(appendData,DICTIONARY_FILE,'dictionary')
#     dataSet.close()


#Main function
def main():
    cleanDataSet(DATASET_FILE)
    getFullPayload()
    # createDictionary(CLEANED_DATASET_FILE)

    
main()
# dataSet = open(CLEANED_DATASET_FILE, 'r')
# for line in dataSet:
#     payload = getFullPayload(line)
#     temp_formater = splitString(line,'?')
#     payload_formated=''
#     try:
#         payload_formated=temp_formater[1]
#         if (payload_formated.endswith("HTTP/1.1\n")):
#             payload_formated = payload_formated[:-10]
#         print(payload_formated)
#     except IndexError:
#         pass

# dataSet.close()