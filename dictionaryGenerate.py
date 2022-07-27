#package

import linecache
import json

from filterPayload import *

#Define env
# DATASET_FILE='anomalousTrafficTest.txt'
# DATASET_FILE='normalTrafficTest.txt'
DATASET_FILE='normalTrafficTraining.txt'
DICTIONARY_FILE='dictionary.json'
DICTIONARY_BACKUP='dictionary-backup.json'
FULL_PAYLOAD_FILE='payload.txt'

# Filter payload from dataset
def cleanDataSet(dataFile):
    dataSet = open(dataFile, 'r')
    payload_file = open(FULL_PAYLOAD_FILE, 'w')
    lineIndex = 1
    for line in dataSet:
        if line.startswith("GET"):
            lineIndex +=1
            line = line.split(' ')
            try:
                payload_formated= line[1].split('?')
                try:
                    payload_file.write(payload_formated[1]+'\n')
                except IndexError:
                    pass
            except IndexError:
                pass
        elif line.startswith("POST"):
            postData = linecache.getline(dataFile, lineIndex + 14)
            payload_file.write(postData)
            lineIndex +=1
        else:
            lineIndex += 1
    dataSet.close()
    payload_file.close()


# Check payload is exist in dictionary
def checkPayloadIsExist(payload):
    dict_file = open(DICTIONARY_FILE, 'r')
    dict_data = json.loads(dict_file.read())
    for key in dict_data["dictionary"]:
        if key["payload"] == payload:
            return True
    return False

# Plus frequency existed in dictionary
def plusFrequency(payload_need_plus):
    dict_file = open(DICTIONARY_FILE, 'r')
    dict_data = json.loads(dict_file.read())

    backup_dict = json.dumps(dict_data, indent = 4)
    with open(DICTIONARY_BACKUP, "w") as outfile:
        outfile.write(backup_dict)

    for i, item in enumerate(dict_data['dictionary']):
        if (item['payload'] == payload_need_plus):
            item['dictionaryFrequency'] = item['dictionaryFrequency']+1
            new_dictitonary = json.dumps(dict_data, indent = 4)
            with open(DICTIONARY_FILE, "w") as outfile:
                outfile.write(new_dictitonary)
    dict_file.close()

# Append new payload if it not exist
def appendDictionary(append_data):
    dict_file = open(DICTIONARY_FILE, 'r')
    dict_data = json.loads(dict_file.read())

    backup_dict = json.dumps(dict_data, indent = 4)
    with open(DICTIONARY_BACKUP, "w") as outfile:
        outfile.write(backup_dict)

    with open(DICTIONARY_FILE,'r+') as file:
        dict_data = json.load(file)
        dict_data["dictionary"].append(append_data)
        file.seek(0)
        json.dump(dict_data, file,indent = 4)
    dict_file.close()

# Create Dicitonary Function    
def createDictionary():
    payload_data = open(FULL_PAYLOAD_FILE, 'r')
    for line in payload_data:
        line = line.split('&')
        for item in line:
            item = item.strip('\n')
            if checkPayloadIsExist(item) == True:
                plusFrequency(item)
            else:
                dict_file = open(DICTIONARY_FILE, 'r')
                dict_data = json.loads(dict_file.read())
                dict_len = len(dict_data['dictionary'])
                maxid = dict_data['dictionary'][dict_len-1]['dictionaryID']+1
                data = {
                        "dictionaryID": maxid,
                        "payload": item,
                        "dictionaryFrequency": 1
                    }
                appendDictionary(data)
                dict_file.close()

#Main function
def main():
    cleanDataSet(DATASET_FILE)
    createDictionary()
    f_filterPayload()
    
main()