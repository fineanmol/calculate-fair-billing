import sys,os
from datetime import datetime
filename = sys.argv[1]

file1 = open(filename,"r")
data = file1.read()
clean_list=[]
usernames = []
start_time = ""
end_time = ""
output={}
total_sessions=0


def RawDataClean(data):
    data_split = data.split("\n")
    for i in data_split:
        isThreeVal = i.split(" ")
        session_time= isThreeVal[0]
        try:
            datetime.strptime(session_time, "%H:%M:%S")
            if(len(isThreeVal)==3 and isThreeVal[1].isalnum() and (isThreeVal[2].lower() =='start' or isThreeVal[2].lower() =='end' )):
                clean_list.append(isThreeVal)
        except ValueError:
            continue

def filterUsernames(clean_list):
    for i in clean_list:
        if(i[1] not in usernames):
            usernames.append(i[1])
            output[i[1]]=0


def CalculateTime(start_time,end_time):
    # convert time string to datetime
    t1 = datetime.strptime(start_time, "%H:%M:%S")
    t2 = datetime.strptime(end_time, "%H:%M:%S")


    # get difference
    delta = t2 - t1
    #total_time+=delta.total_seconds()

    # time difference in seconds
    #print(f"Time difference is {delta.total_seconds()} seconds\n")
    return delta.total_seconds()

RawDataClean(data)
filterUsernames(clean_list)
global_start=clean_list[0][0]
global_end=clean_list[-1][0]
session_count={}



for i in usernames:
    stack=[]
    session_local_count=0
    
    for j in clean_list:
        if(j[1] == i):
            if(j[2].lower()=="start"):
                stack.append(f"start {j[0]}")
                session_local_count+=1
                
            if(j[2].lower()=="end"):
                end_time =j[0]
                start_time=global_start
                if(len(stack) > 0):
                    start_time = stack.pop().split(" ")[1]              
                    
                else:
                    session_local_count+=1

                session_time = CalculateTime(start_time,end_time)
                output[i]=output[i]+session_time

    session_count[i]= session_local_count
    
        


#output
for username in usernames:
    print(f"{username} {session_count[username]} {int(output[username])}")





