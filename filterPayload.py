#package

from cProfile import label
import linecache
import json

#Define env

DATASET_FILE='normalTraffic.txt'
FULL_PAYLOAD_FILE='payload.txt'

PAYLOAD_FILE='filter_payloay.json'

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


def checkPayloadIsExist(payload):
    payload_file = open(PAYLOAD_FILE, 'r')
    p_data = json.loads(payload_file.read())
    for key in p_data["filterPayload"]:
        if key["data"] == payload:
            return True
    return False

#Set label for payload; is attack = 1, not attack = 0
def setLabel(item):
    anomaly_detect = ["Set-cookie", "SCRIPT","alert","EXEC","cmd","CMD","--","waitfor+delay","OR+1%3D1","%27+OR+%271%27%3D%271"
                "sessionid","document.location","passwd","etc","SELECT","WHERE","FROM","DROP","DELETE",
                  "scrIPT","SCRipt","include+file","javascript","%221%22%3D%221","%27+AND+%271%27%3D%271",
                  "AND+1%3D1","USERS","%27INJECTED_PARAM","AND+1%3D1","background","javascript","%252B",
                  "%22%3E%3C%21--%23EXEC+cmd%3D%22dir+%22--%3E%3C","%27OR%27a%3D%27a","%2540%253CSCRipt%253Ealert%2528",
                  "%2529%253C%252FscrIPT%253E","%22%3E%3C%21--%23EXEC+cmd%3D%22dir+%22--%3E%3C","%3C%21--%23include+file%3D%22","%22+--%3E"
                  "%40%3CSCRipt%3E","%2522%2Bstyle%253D%2522background%253Aurl%2528javascript%253Aalert%2528%2527","%3C%21--%23EXEC+cmd%3D%22ls+%2F%22--%3E"
                ]
    
    if(len(item) <= 4):
        if(item.startswith("%")):
            label=1
        else:
            label = 0
    else:
        for i in anomaly_detect:
            # if item.find(i) > 0:
            # if search(i,item):
            # if item.count(i) ==1:
            if i in item:
            # if any(x in item for x in anomaly_detect):
                label = 1
                break
            else:
                label = 0
    return label

def appendData(append_data):
    payload_file = open(PAYLOAD_FILE, 'r')
    p_data = json.loads(payload_file.read())

    # backup_dict = json.dumps(p_data, indent = 4)
    # with open(DICTIONARY_BACKUP, "w") as outfile:
    #     outfile.write(backup_dict)

    with open(PAYLOAD_FILE,'r+') as file:
        p_data = json.load(file)
        p_data["filterPayload"].append(append_data)
        file.seek(0)
        json.dump(p_data, file,indent = 4)
    payload_file.close()
    
def f_filterPayload():
    payload_data = open(FULL_PAYLOAD_FILE, 'r')
    for line in payload_data:
        line = line.split('&')
        for item in line:
            item = item.strip('\n')
            if checkPayloadIsExist(item) == True:
                continue
            else:            
                payload_file = open(PAYLOAD_FILE, 'r')
                p_data = json.loads(payload_file.read())
                
                payload_len = len(p_data['filterPayload'])
                maxid = p_data['filterPayload'][payload_len-1]['dataID']+1
                label = setLabel(item)
                data = {
                        "dataID": maxid,
                        "data": item,
                        "label": label
                    }
                appendData(data)
                payload_file.close()

def main():
    cleanDataSet(DATASET_FILE)
    f_filterPayload()
                
main()
                
