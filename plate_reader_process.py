
# coding: utf-8

# In[1]:

"""
Python script for producing R-dataframe from plate reader's raw txt files.
With Python 3 style.

Pipeline(combined with R script):
Raw data -> This python script -> R script -> plot

by Yue Zhao

"""

# loading packages
import os 
import re


# Modify this block below before using the script
# The default condition use 3*5 wells in the 96 well plate for each time point
# list_dilution_5 is for a 2*9 wells test
#####################################################################################
out_od600 = open('output_od600.txt', "w")                                           # 
out_spec = open('output_spec.txt', "w")                                             # 
out_od600.write("od600\ttime\tdilution\n")                                          #
out_spec.write("obsorb\tod\ttime\tdilution\n")                                      #  
list_dilution_1 = ["1:1", "1:2", "1:5", "1:10", "1:20"]                             #
list_dilution_2 = ["1:1", "1:2", "1:5", "1:10", "1:20"] * 3                         #
dict_hour = {"4":1, "6":2,"8":3,"10":4,"12":5,"14":6,"17":7,"19":8, "21":9, "2":1,  #
             "5":2, "7":3, "9":4, "11":5, "13":6, "16":7, "18":8, "20":9 }          #
list_dilution_3 = ["1:1"] * 3 + ["1:2"] * 3 + ["1:5"] * 3                           #
list_dilution_4 = ["1:10"] * 3 + ["1:20"] * 3                                       #
list_dilution_5 = list_dilution_3 + list_dilution_4                                 #
#####################################################################################



# Modify the code below based on your needs
for fn in os.listdir('./data_0802/p_test/'):
    print("processing:",fn)
    path_fn = "./data_0802/p_test/"+fn
    f = open(path_fn, "r")
    id_plate = 0
    for line in f:
        matchObj = re.match("([ABCDEFGH])\t*[0-9]", line)
        searchObj = re.search("Plate\s([0-9]+)", line)
        if searchObj:
            id_plate = searchObj.group(1)
            print("id_plate:", id_plate)
            
            
        ###################################################################################################    
        # this if block is added as we have a weird 2*9 wells    
        if id_plate == "21":
            if matchObj:
                od = re.findall("[0-9]\.[0-9]*", line)
                if matchObj.group(1) == "G":
                    for i in range(0,9):
                        out_od600.write(od[i]+"\t"+str(dict_hour[id_plate])+"\t"+list_dilution_3[i]+"\n")
                    continue              
                if matchObj.group(1) == "H":
                    for i in range(0,6):
                        out_od600.write(od[i]+"\t"+str(dict_hour[id_plate])+"\t"+list_dilution_4[i]+"\n")
                    continue              
            matchObj_spec = re.match("([0-9]+)\t*", line)
            if matchObj_spec:
                spec_od = matchObj_spec.group(1)
                spec = re.findall("[0-9]\.[0-9]*|OVRFLW", line)
                for i in range(0,15):
                    out_spec.write(spec[i]+"\t"+spec_od+"\t"+str(dict_hour[id_plate])+"\t"+list_dilution_5[i]+"\n")   
                continue
            continue
        #################################################################################################
         # this if block is added as we have 1*3 and 3*1 wells
        if id_plate == "20":
            if matchObj:
                od = re.findall("[0-9]\.[0-9]*", line)
                for i in range(0,3):
                    out_od600.write(od[i]+"\t"+str(dict_hour[id_plate])+"\t1:1(before)\t\n")
                continue 
            matchObj_spec = re.match("([0-9]+)\t*", line)
            if matchObj_spec:
                spec_od = matchObj_spec.group(1)
                spec = re.findall("[0-9]\.[0-9]*|OVRFLW", line)
                for i in range(0,3):
                    out_spec.write(spec[i]+"\t"+spec_od+"\t"+str(dict_hour[id_plate])+"\t1:1(before)\t\n")            
                continue
            continue
        if id_plate in ["2", "5", "7", "9", "11", "13", "16", "18"]:
            if matchObj:
                od = re.findall("[0-9]\.[0-9]*", line)
                out_od600.write(od[0]+"\t"+str(dict_hour[id_plate])+"\t1:1(before)\t\n")
            matchObj_spec = re.match("([0-9]+)\t*", line)
            if matchObj_spec:
                spec_od = matchObj_spec.group(1)
                spec = re.findall("[0-9]\.[0-9]*|OVRFLW", line)
                for i in range(0,3):
                    out_spec.write(spec[i]+"\t"+spec_od+"\t"+str(dict_hour[id_plate])+"\t1:1(before)\t\n")            
                continue                  
            continue
        
       
        ###################################################################################################
        
        
        
        if matchObj:
            od = re.findall("[0-9]\.[0-9]*", line)
            for i in range(0,5):
                out_od600.write(od[i]+"\t"+str(dict_hour[id_plate])+"\t"+list_dilution_1[i]+"\n")
            continue                 
        matchObj_spec = re.match("([0-9]+)\t*", line)
        if matchObj_spec:
            spec_od = matchObj_spec.group(1)
            spec = re.findall("[0-9]\.[0-9]*|OVRFLW", line)
            for i in range(0,15):
                out_spec.write(spec[i]+"\t"+spec_od+"\t"+str(dict_hour[id_plate])+"\t"+list_dilution_2[i]+"\n")
         
        
        
    f.close()
out_od600.close()
out_spec.close()


# In[ ]:



