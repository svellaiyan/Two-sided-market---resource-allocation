import operator , sys

# function to get the maximum score in the vendor_score file


def getMaximumScore(fScoreVendoropen):
    scoreList = []
    for line in fScoreVendoropen:
        line = line.strip()
        line = line.split('\t')
        if len(line) != 2:
           print "There vendor input file is not formatted properly."
           sys.exit()         
        score = float(line[1])      
        scoreList.append(score)

    if len(scoreList) == 0:        
        print "The input Vendor score file is empty."
        sys.exit()        

    maxScore = max(scoreList)
    print maxScore
    return float(maxScore)

        

# Function of read the vendor_score file and create a dictionary of
# key:value vendor_ID:score


def getScoreVendorDict(fopen):
    resultDict = dict()
    for line in fopen:
        line = line.strip()
        ids = line.split('\t')
        if len(ids) != 2:
           print "There vendor input file is not formatted properly."
           sys.exit() 
        vendorID = ids[0]
        score = float(ids[1])
        resultDict[vendorID] = round((score * 100), 2)
    sorted_x = sorted(resultDict.items(),
                      key=operator.itemgetter(1), reverse=True)
    count = 0
    finalDict = dict()
    for eachval in sorted_x:
        count = count + 1
        if count <= 4:
            keyVal = eachval[0]
            valueVal = eachval[1]
            finalDict[keyVal] = valueVal
    return finalDict

# Function of read the jobpriority file and create a dictionary of
# key:value job_ID:arrival_Time


def getJobPriorityDict(fJobsOpen):
    resultDict = dict()
    for line in fJobsOpen:
        line = line.strip()
        ids = line.split('\t')
        if len(ids) != 2:
           print "There Job input file is not formatted properly."
           sys.exit()        
        jobID = ids[0]
        jobTime = ids[1]
        print jobID, jobTime
        resultDict[jobID] = jobTime
        
    if len(resultDict) == 0:
        print "The input Job priority file is empty."
        sys.exit()        
    
    return resultDict
    

# function to create a separate dictionary(key:value::VendorID:score)
# based of score priority


def getscoreSeparateDict(scoreTest):
    scoreA = dict()
    scoreB = dict()
    scoreC = dict()
    scoreD = dict()
    scoreSeparateList = dict()
    scoreTest = sorted(scoreTest.items(),
                       key=operator.itemgetter(1), reverse=True)
    dictLen = len(scoreTest)
    count = 0
    for eachScore in scoreTest:
        count = count + 1
        keyVal = eachScore[0]
        valueVal = eachScore[1]
        if count <= dictLen:
            if count == 1:
                scoreA[keyVal] = valueVal
                scoreSeparateList['A'] = scoreA
            elif count == 2:
                scoreB[keyVal] = valueVal
                scoreSeparateList['B'] = scoreB
            elif count == 3:
                scoreC[keyVal] = valueVal
                scoreSeparateList['C'] = scoreC
            elif count == 4:
                scoreD[keyVal] = valueVal
                scoreSeparateList['D'] = scoreD
            else:
                break
    print scoreSeparateList
    return scoreSeparateList
