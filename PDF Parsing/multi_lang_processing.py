
import pandas as pd
import string
from data import Citizen

import warnings
import os

absol_path = os.path.abspath(os.getcwd())
warnings.filterwarnings("ignore")

DICT_GENDER = {0: "MALE", 1: "FEMALE", 2: "OTHER"}
Reverse_dict = {"MALE": 0, "FEMALE": 1, "OTHER": 2}

#print(absol_path)

#filename should be present in the same directory, output csv is generated in same directory
def parse_english(filename, output):
    filename = absol_path + "/" + filename
    output = absol_path + "/" + output
    with open(filename, "r") as txt_file:
        text = txt_file.read().splitlines()

    def compact(lst):
        return list(filter(None, lst))

    to_remove = ['\n','Photo is', 'Available']
    text = [elt for elt in text if elt not in to_remove]
    #text = [x for x in text if not isinstance(x, int)]
    text = compact(text)
    
    ls = string.punctuation
    ls = ls.replace(':','')
    ls = ls.replace("'",'')


    #print(ls)
    #print(text)

    temp_list = []
    citizen_list = []

    for i,ts in enumerate(text):
        text[i] = text[i].translate(str.maketrans('', '', ls))
        text[i] = text[i].strip()
        text[i] = text[i].upper()
        text[i] = " ".join(text[i].split())

    #print(text)
    for i, ts in enumerate(text):
        if ts.startswith("NAME:"):
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
                    #i+=1
                    with open('problemFiles.txt', 'a') as f:
                        f.write("Cannot add ",i,"th citizen")
                tmp_name = ''
                tmp_father = ''
                tmp_husband = ''
                tmp_other = ''
                tmp_age = 0
                tmp_gender = 0
                tmp_houseNo = ''
            if text[i].startswith("NAME: "):
                try:
                    tmp_name = text[i].split("NAME: ", 1)
                    #print(tmp_name[1])
                    tmp_name = tmp_name[1]
                except:
                    print("Bt in NAME of ", i)
            i+=1
            while i not in temp_list:
                if text[i].startswith("FATHER'S NAME: "):
                    try:
                        #print(text[i])
                        tmp_father = text[i].split("FATHER'S NAME: ", 1)
                        #print("Father",tmp_father)
                        tmp_father = tmp_father[1]
                    except:
                        print("Bt in FATHER'S NAME of ", i)
                elif text[i].startswith("HUSBAND'S NAME: "):
                    try:
                        tmp_husband = text[i].split("HUSBAND'S NAME: ", 1)
                        #print("Husband",tmp_husband[1])
                        tmp_husband = tmp_husband[1]
                    except:
                        print("Bt in HUSBAND'S NAME of ", i)
                elif text[i].startswith("OTHER'S NAME: "):
                    try:
                        tmp_other = text[i].split("OTHER'S NAME: ", 1)
                        tmp_other = tmp_other[1]
                    except:
                        print("Bt in OTHER'S NAME of ", i)

                elif text[i].startswith("HOUSE NUMBER: "):
                    try:
                        tmp_houseNo = text[i].split("HOUSE NUMBER: ", 1)
                        tmp_houseNo = tmp_houseNo[1]
                        #print("HouseNo ",tmp_houseNo)
                    except:
                        print("Bt in HOUSE NUMBER of ", i)
                elif text[i].startswith("AGE:"):
                    try:
                        #print(text[i])
                        for ele in text[i]:
                            if ele == ':':
                                text[i] = text[i].replace(ele, "")
                        #print(text[i])
                        test_str = text[i].split()
                        tmp_age = test_str[1]
                        sex = test_str[-1]
                        if sex=='MEN':
                            sex='MALE'
                        if sex=='WOMEN':
                            sex='FEMALE'
                        if sex!='MALE' and sex!='FEMALE':
                            sex='OTHER'
                        tmp_gender = Reverse_dict[sex]
                        #print("Age ",tmp_age)
                        #print("Gender ",tmp_gender)
                    except:
                        print("Bt in AGE and GENDER of ", i)
                
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
    #print(master_df)

parse_english('document-page1.pdftrans.txt','test3.csv')