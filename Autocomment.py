import os, sys, csv, datetime
from time import gmtime, strftime

Criteria = {}

def SelectSentence(ColName, ColValue):

    """For Each Criteria we need to select what to say based on the col value"""
    global Criteria
    Sentence = ''

    if(ColName.find("Email") != -1 or ColName.find("Name") != -1 or ColName.find("SID") != -1 or ColName.find("CName") != -1 or ColName.find("Score") != -1):
        return  None

#    print("Col name is"+str(ColName) + " Value is "+ str(ColValue))

    for x in range(len(Criteria['Head'])-1) :

        if(int(ColValue) ==  int(Criteria['Head'][x])):
            return Criteria[ColName][x]
            break
        if(int(ColValue) <  int(Criteria['Head'][x+1])):
            return Criteria[ColName][x]
            break


    return Criteria[ColName][len(Criteria['Head'])-1]


def HandleStudent(row):

    """For Each student we need to get a line for each criteria as defined in the CSV"""

    Name = row['Name']
    Email = row['Email']
    SID = row['SID']
    Mark = row['Score']
    Comments = ''
    sinceCR = 80

   # print(str(row))
    
    for k,v in row.iteritems():

        Output = SelectSentence(k,v) 
        if(Output != None):
            sinceCR -= len(Output)
            Comments += "  "+Output+"."
            if(sinceCR < 0):
                Comments += "\n"
                sinceCR = 80

    print("\n\nName: "+Name+"\t SID:"+SID)

    fileName = str(Name+str(SID)+".mail")
    stud = open(fileName,"w+")


    stud.write("date:"+strftime("%Y-%m-%d %H:%M:%S", gmtime())+"\n")
    stud.write("to: "+Email+"\n")
    stud.write("subject: Coursework feedback \n")
    stud.write("from: auto@roach.cs.nott.ac.uk\n\n")
    stud.write(str(Name)+", your mark for the coursework was: "+Mark+" \n\r")
    stud.write("A report follows:\n\n\r")

    stud.write(Comments)

    stud.flush()
    stud.close()
    
    #should use Popen but not on marian so using os.system instead
#    os.system("/usr/sbin/sendmail -t < "+ str(fileName))
#    os.stdout.write("Email for "+str(Name)+" written and sent to "+str(Email))
    print("Email for "+str(Name)+" written and sent to "+str(Email))


    return Comments


def GenerateSelectionMatrix(StudFile):

    """Generate a table with the possible sentences mapped to the criteria"""
    global Criteria
    sfile = open(StudFile, "r");
    
    read = csv.DictReader(sfile)
    Criteria['Head'] = read.next().keys()
 #   print(str(Criteria['Head']))
    for x in range(len(Criteria['Head'])):
        if(Criteria['Head'][x].find("CName") != -1):
            del(Criteria['Head'][x])
            break

    sfile.close()

    sfile = open(StudFile, "r");

    read = csv.DictReader(sfile)
    for line in read:
        Name = line['CName']
        del(line['CName'])
        Criteria[Name] = line.values() 

 #   print("Criteria is"+str(Criteria))

def main():

 
    if(len(sys.argv) < 2):
	print("<Sentence File> <StudentFile>\n")
        sys.exit(-1)

    SentenceFile = sys.argv[1]
    StudentFile = sys.argv[2]
    ifile = open(StudentFile, "rb")
    
    GenerateSelectionMatrix(SentenceFile)

    reader = csv.DictReader(ifile)

    for row in reader:

        Result = HandleStudent(row)
#        print("Result is"+str(Result))

    ifile.close()


main()
