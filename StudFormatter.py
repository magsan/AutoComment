import os, sys, csv

MainDB = None
mainHeaders = []

def extract_details(Forename, surname):

    global MainDB,mainHeaders
    SID = -1
    Email = None 

    for line in MainDB:
    
        vals = line.strip("\r\n").split(",")
        mainD = dict(zip(mainHeaders, vals))

        if(mainD['Surname'].find(surname)!= -1 and mainD['Forename'].find(Forename) != -1):
             SID = mainD['Student ID']
             Email = mainD['Email']
             break

    MainDB.seek(0)

    if(SID == -1):
       print(Forename + " "+ surname + "Not found cannot look up\n")

        
    return {'SID':SID, 'Email': Email}

def format_new_line(details):

    yield

def main():
   
    global MainDB,mainHeaders

    MainDB =  sys.argv[1]
    PairsDB = sys.argv[2]
    Output = sys.argv[3]

    marksRequired =[] 

    MainDB = open(MainDB, "r") 
    PairsDB = open(PairsDB, "r")
    newFile = open(Output, "w+")

    mainHeaders = MainDB.readline().strip("\r\n").split(",")
    PairsHeaders= PairsDB.readline().strip("\r\n").split(",")

    markNames = PairsHeaders[4:14]

    newFile.write("Name,SID,Email,Score,")

    for names in markNames:

        newFile.write(names + ",")

    newFile.write("\n")
    for line in PairsDB:

        vals = line.strip("\r\n").split(",")
        studD = dict(zip(PairsHeaders, vals))
        marks = dict(zip(markNames, vals[4:14])) 

        StudADetails = extract_details(studD['Forename'],studD['Surname'])

        toWriteA = studD['Forename'] +" "+ studD['Surname'] +","+ str(StudADetails['SID'])+","+StudADetails['Email']+","+str(studD['Score'])+","

        for mark in marks.values():
            toWriteA += str(mark)+ ","

        newFile.write(toWriteA+"\n")

        #If it is not null also do second student
        if(studD['Forename B'] != ''):
            StudBDetails = extract_details(studD['Forename B'],studD['Surname B'])
            toWriteB = studD['Forename B']+ " " + studD['Surname B'] +","+ str(StudBDetails['SID'])+","+str(StudBDetails['Email'])+","+str(studD['Score'])+","

            for mark in marks.values():
                toWriteB += str(mark)+ ","

            newFile.write(toWriteB+"\n")

    newFile.close()
    PairsDB.close()
    MainDB.close()    

main() 
