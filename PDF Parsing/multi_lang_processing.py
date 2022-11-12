import os
import pandas as pd
import string
from data import Citizen

DICT_GENDER = {0: "MALE", 1: "FEMALE", 2: "OTHER"}
Reverse_dict = {"MALE": 0, "FEMALE": 1, "OTHER": 2}

def parse_english(filename, output):
    with open(filename, "r") as txt_file:
        text = txt_file.read().splitlines()

    def compact(lst):
        return list(filter(None, lst))

    to_remove = ['\n','Photo is', 'Available']
    text = [elt for elt in text if elt not in to_remove]
    #text = [x for x in text if not isinstance(x, int)]
    text = compact(text)
    
    ls = string.punctuation
    ls.replace(':','')
    ls.replace("'",'')

    #print(text)

    temp_list = []
    citizen_list = []

    for ts in text:
        ts = ts.translate(str.maketrans('', '', ls))

    for i, ts in enumerate(text):
        if ts.startswith("Name:"):
            temp_list.append(i)

    #print((temp_list))

    i=0
    tmp_name = ''
    tmp_father = ''
    tmp_husband = ''
    tmp_other = ''
    tmp_age = 0
    tmp_gender = 0
    tmp_houseNo = ''
    flag=False
    while i<len(text):
        if flag:
            break
        if i<temp_list[0]:
            i+=1
            continue
        if i in temp_list:
            #print(i)
            if i != 0:
                try:
                    tmp_citizen = Citizen(tmp_name,tmp_father,tmp_husband,tmp_other,tmp_age,tmp_gender,tmp_houseNo,0)
                    citizen_list.append(tmp_citizen)
                except:
                    print("Cannot add ",i,"th citizen")
                    with open('problemFiles.txt', 'a') as f:
                        f.write("Cannot add ",i,"th citizen")
                tmp_name = ''
                tmp_father = ''
                tmp_husband = ''
                tmp_other = ''
                tmp_age = 0
                tmp_gender = 0
                tmp_houseNo = ''
            if text[i].startswith("Name: "):
                tmp_name = text[i].split("Name: ", 1)
                print("Name",tmp_name[1])
                tmp_name = tmp_name[1]
            i+=1
            while i not in temp_list:
                if text[i].startswith("Father's Name: "):
                    tmp_father = text[i].split("Father's Name: ", 1)
                    #print("Father",tmp_father)
                    tmp_father = tmp_father[1]
                elif text[i].startswith("Husband's Name: "):
                    tmp_husband = text[i].split("Husband's Name: ", 1)
                    #print("Husband",tmp_husband[1])
                    tmp_husband = tmp_husband[1]
                elif text[i].startswith("Other's Name: "):
                    tmp_other = text[i].split("Other's Name: ", 1)
                    #print("Other",tmp_other[1])
                    tmp_other = tmp_other[1]
                elif text[i].startswith("House Number: "):
                    tmp_houseNo = text[i].split("House Number: ", 1)
                    tmp_houseNo = tmp_houseNo[1]
                    #print("HouseNo ",tmp_houseNo)
                elif text[i].startswith("Age:"):
                    for ele in text[i]:
                        if ele == ':':
                            text[i] = text[i].replace(ele, "")
                    test_str = text[i].split()
                    tmp_age = test_str[1]
                    tmp_gender = Reverse_dict[test_str[3]]
                    #print("Age ",tmp_age)
                    #print("Gender ",tmp_gender)
                else:
                    if i==len(text)-1:
                        try:
                            tmp_citizen = Citizen(tmp_name,tmp_father,tmp_husband,tmp_other,tmp_age,tmp_gender,tmp_houseNo,0)
                            citizen_list.append(tmp_citizen)
                        except:
                            print("Cannot add ",i,"th citizen")
                            with open('problemFiles.txt', 'a') as f:
                                f.write("Cannot add ",i,"th citizen")
                        flag=True
                        break
                    i+=1
                    continue
                if flag:
                    break
                i+=1
                

    #print(text)
    #print(citizen_list)
    df = pd.DataFrame()
    df["Name"] = ""
    df["Father Name"] = ""
    df["Husband Name"] = ""
    df["Other Name"]=""
    df["Age"]=""
    df["Gender"]=""
    df["House No"]=""

    for citizen in citizen_list:
        if citizen.NAME == 0:
            continue
        df = df.append({'Name':citizen.NAME, 'Father Name':citizen.FATHER_NAME, 'Husband Name':citizen.HUSBAND_NAME,'Other Name':citizen.OTHER_NAME,'Age':citizen.AGE,'Gender':citizen.GENDER, 'House No':citizen.HOUSE}, ignore_index=True)

    master_df = df.to_csv(output,index=False)
    print(master_df)

parse_english('document-page0.pdftrans.txt','test2.csv')