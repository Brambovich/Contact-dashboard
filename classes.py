from gemacsorting import importfromdatabase

class person:
    def __init__(self,name):
        self.name = name
        self.matchedpersons = dict()
    
    def addmatch(self, Encountername, timestamp, coughed):
        if Encountername in self.matchedpersons:
            if timestamp in self.matchedpersons[Encountername].matches:
                print("match already exists")
            else:
                self.matchedpersons[Encountername].matches[timestamp] = match(self.name,Encountername,timestamp, coughed)
        else:
            self.matchedpersons[Encountername] = matchedperson()
            self.matchedpersons[Encountername].matches[timestamp] = match(self.name,Encountername,timestamp, coughed)
        
class matchedperson:
    def __init__(self,):
        self.matches = dict()
       
class match:
    def __init__(self, name, matchedname, timestamp, coughed):
        self.name = name
        self.matchedname = matchedname
        self.timestamp = timestamp
        self.coughed = (coughed == "True")
        
        
def createclasses():

    matches = importfromdatabase()
    persons = dict()


    for name, matchedname, timestamp, coughed in matches:
        
        if name in persons:
            persons[name].addmatch(matchedname, timestamp, coughed)
        else:
            #print(name)
            
            persons[name] = person(name)
            persons[name].addmatch(matchedname,timestamp, coughed)
            #print(persons["Bram"])
            
        if matchedname in persons:
            persons[matchedname].addmatch(name, timestamp, coughed)
        else:
            #print(name)
            
            persons[matchedname] = person(matchedname)
            persons[matchedname].addmatch(name,timestamp, coughed)
            #print(persons["Bram"])
    return persons


if __name__ == '__main__':
    createclasses()