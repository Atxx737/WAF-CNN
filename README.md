# This code include files
1. dictionaryGenerate.py: This is main file of program. It will filter all of payload in dataset, write to payload.txt and create full dictionany with Bag of Word model to json file
2. anomalousTrafficTest.txt: This is dataset file to train. I download it from https://www.isi.csic.es/dataset/
3. dictionary-backup.json: this is backup of dictionary file. Before make some change in main dictionary, program will wirte a backup version to this file. Sometime program may be corrupt and I don't want to lost data in dictionary.
4. template.txt: this file is require template for dictionary.json before first run.
5. dictionary.json: main dictionary. It is result of program
6. payload.txt: it is generated by program. It is all of payload I collect from dataset urls.
7. README.md: this file. It introduce for repository and how to run it.
8. Requiment.txt: require for import package. Run ```pip install -r requirements.txt``` in python 3.10.0 or later to install all of package I import in program

# How to run this code
  1. Pre-process
Just follow after steps to create dictionary
- Install ```python 3```
- Clear all of data in `dictionary.json`
- Copy all of data from `dictionary-template.json` to `dictionary.json`
- Run this command: 
    ```
    python dictionaryGenerate.py
    ```
    or in linux
    ```
    python3 dictionaryGenerate.py
    ```
After we set label for request
- Copy all of data from `template.txt` to `filter_payload.json`
- Run this command:
   ```
   python filtePayload.py
   ```
  All data will be store at filter_payload.json
  
Finally, we will convert http request into matrix by run the command
    ```
    python createArray.py
    ```
All picture will be store at folder Picture which 2 sub is Normal and Anomaly

  2. CNN module
 - Run jupyter file `cnn-module.ipynb`
  
***Note that***
- `chmod +x dictionaryGenerate.py` if you run this program in linux
- If you corrupt this program while it is still running *(e.g Ctr + C)* and you want to run it again, please follow step by step above. The payloadFrequency in dictionary not exactly if any problem come to while program is running. So, becaful because python run very slow.
