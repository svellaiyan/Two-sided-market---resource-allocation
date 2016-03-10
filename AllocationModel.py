# Optimization model to allocate jobs for a pool of vendors based on score
# and job priority

from gurobipy import *  # Import the gurobi python optimizer
# import pyhton file WK_Final_1 as a: This file contains all the small
# modules to solve the model
import WK_FileOperations as a
import math  # To import all the mathematical functions like ceiling up a decimal number
import time  # To call time.sleep when the vendors are not yet signed in
# Open the input and output files

# Open the file which contains job_ID and job_arrival_time in read mode
fJobsOpener = raw_input(
    'Please enter the job file name: ')
#fJobsOpen = open(curFldr + '\\' + fJobsOpener, 'r')
fJobsOpen = open(fJobsOpener, 'r')

# Open the file which contains Vendor_ID and Vendor_score in read mode

fScoreVendoropener = raw_input(
    'Please enter the vendor file name: ')
#fScoreVendoropen = open(curFldr + '\\' + fScoreVendoropener, 'r')
fScoreVendoropen = open(fScoreVendoropener, 'r')

# Open the output file in write mode
fileWriter = open('WK_output.txt', 'w')

# Create a linear programming model variable
m = Model("mip1")

# maxScore contains maximum score in the vendor list. If the maxScore is less than 0.85
# then the system waits for '2' mins and fetches all new and old vendors
# in the list for job allocation
maxScore = a.getMaximumScore(fScoreVendoropen)
if maxScore <= 0.85:
    print 'sleeping'
    time.sleep(120)
    print 'done'
# close to file before fetching new entries in the vendor score file
fScoreVendoropen.close()

# read all the job details from the file and store it in a
# key(jobID)-value(arrivalTime) pair dictionary
jobPriorityDict = a.getJobPriorityDict(fJobsOpen)

# = open(curFldr+'\\'+fScoreVendoropener,'r') # Read the updated vendor score text file after 2 mins of wait time
# Read the updated vendor score text file after 2 mins of wait time
fScoreVendorOpenUpdated = open(fScoreVendoropener, 'r')
# read all the Vendor details from the file and store it in a
# key(vendorID)-value(score) pair dictionary
vendorScoreDict = a.getScoreVendorDict(fScoreVendorOpenUpdated)

# set the job priority by subtracting job arrival time from 1700(5:00PM
# maximum time)
for eachJob in jobPriorityDict:
    jobPriorityDict[eachJob] = 1700 - int(jobPriorityDict[eachJob])

# function to get the linear expression:  sum of all jobs for each vendor,
#   where scoreDict contains key value pair of vendor and score based on the priority
#       and jobPriorityDict passes all jobs to calcuate the linear expression.


def getLinearExpression(scoreDict, jobPriorityDict):
    finalLhs = 0
    for eachVendor in scoreDict:
        sumojJpV = []
        addVal = []
        for eachJob in jobPriorityDict:
            sumojJpV.append(flow[(eachJob, eachVendor)])
            addVal.append(1)
        lhs = LinExpr(addVal, sumojJpV)
        finalLhs = finalLhs + (1 * lhs)
    return finalLhs

# Initiate each decision variable as a dictionary(key: jobId and VendorID,
# value: binary decision variable) and add it to the model
flow = dict()  # contains key value pair of decision variables
for i in jobPriorityDict:
    for j in vendorScoreDict:
        flow[(i, j)] = m.addVar(vtype=GRB.BINARY, name='flow_%s_%s' % (i, j))

# Update the model after each model entry
m.update()

# Add Constraint for each job (Sum of jobs for each vendor should be equal
# to 1)
for i in jobPriorityDict:
    VpJ = []
    addValVpJ = []
    for j in vendorScoreDict:
        VpJ.append(flow[(i, j)])
        addValVpJ.append(1)
    lhsVpJ = LinExpr(addValVpJ, VpJ)
    m.addConstr(lhsVpJ, GRB.EQUAL, 1.0)

# Update the model after each constraint entry
m.update()

# Get the scoreSeparateDict which gives separate
# dictionary(key:value::VendorID:score) based of score priority
scoreSeparateDict = a.getscoreSeparateDict(vendorScoreDict)

# Add constraint for each vendor in the scoreSeparateDict.
#    Constraint: Total jobs assigned for each vendor should be less than or equal to the calculated maximum number of jobs for that particular vendor
# If the calculated number of jobs is a decimal value then we are using
# math.ceil() for ceiling up the decimal value to the next integer
for eachScoreList in scoreSeparateDict:
    scoreDict = dict()
    scoreDict = scoreSeparateDict[eachScoreList]
    finalLhs = getLinearExpression(scoreDict, jobPriorityDict)
    if len(scoreSeparateDict) == 4:
        if eachScoreList == 'A':
            valueForJobs = math.ceil(len(jobPriorityDict) * 0.6)
            m.addConstr(finalLhs, GRB.LESS_EQUAL, valueForJobs)
            print valueForJobs, eachScoreList
        elif eachScoreList == 'B':
            valueForJobs = math.ceil(len(jobPriorityDict) * 0.2)
            m.addConstr(finalLhs, GRB.LESS_EQUAL, valueForJobs)
            print valueForJobs, eachScoreList
        elif eachScoreList == 'C':
            valueForJobs = math.ceil(len(jobPriorityDict) * 0.15)
            m.addConstr(finalLhs, GRB.LESS_EQUAL, valueForJobs)
            print valueForJobs, eachScoreList
        else:
            valueForJobs = math.ceil(len(jobPriorityDict) * 0.05)
            m.addConstr(finalLhs, GRB.LESS_EQUAL, valueForJobs)
            print valueForJobs, eachScoreList
    elif len(scoreSeparateDict) == 3:
        if eachScoreList == 'A':
            valueForJobs = math.ceil(len(jobPriorityDict) * 0.7)
            m.addConstr(finalLhs, GRB.LESS_EQUAL, valueForJobs)
        elif eachScoreList == 'B':
            valueForJobs = math.ceil(len(jobPriorityDict) * 0.2)
            m.addConstr(finalLhs, GRB.LESS_EQUAL, valueForJobs)
        else:
            valueForJobs = math.ceil(len(jobPriorityDict) * 0.1)
            m.addConstr(finalLhs, GRB.LESS_EQUAL, valueForJobs)
    elif len(scoreSeparateDict) == 2:
        if eachScoreList == 'A':
            valueForJobs = math.ceil(len(jobPriorityDict) * 0.8)
            m.addConstr(finalLhs, GRB.LESS_EQUAL, valueForJobs)
        else:
            valueForJobs = math.ceil(len(jobPriorityDict) * 0.2)
            m.addConstr(finalLhs, GRB.LESS_EQUAL, valueForJobs)
    else:
        valueForJobs = math.ceil(len(jobPriorityDict) * 1)
        m.addConstr(finalLhs, GRB.LESS_EQUAL, valueForJobs)

# Update the model after each constraint entry
m.update()

# Constraint to calculate jobs assgined to all vendors should be equal to
# total number of jobs in the jobPriorityDict
finalConstr = 0
for i in vendorScoreDict:
    sumojJpV = []
    addVal = []
    for j in jobPriorityDict:
        sumojJpV.append(flow[(j, i)])
        addVal.append(1)
    finalConstrlhs = LinExpr(addVal, sumojJpV)
    finalConstr = finalConstr + (1 * finalConstrlhs)
m.addConstr(finalConstr, GRB.EQUAL, len(jobPriorityDict))

# Update the model after each constraint entry
m.update()

# Create objective linear expression: To maximize the sumproduct of vendor
# score, total joobs for that particular vendor and job priority of the
# assigned job for the same vendor
jobsperVendor = dict()
objective = 0
for i in vendorScoreDict:
    jobsperVendor[i] = 0
    job_score = 0
    for j in jobPriorityDict:
        jobsperVendor[i] = jobsperVendor[i] + flow[(j, i)]
        job_score = job_score + jobPriorityDict[j] * flow[(j, i)]
    objective = objective + (vendorScoreDict[i] * job_score)
m.setObjective(objective, GRB.MAXIMIZE)

# Update the model after each constraint entry
m.update()

# Optimize the model
m.optimize()

# Output file which contains Vendor ID, assigned Job ID and arrival time
# of the job
average = 0
vendor_hist_list = []
fileWriter.write("Vendor_ID" + '\t' + "Job_ID" + '\t' + "Arrival_Time" + '\n')
for i in jobPriorityDict:
    for j in vendorScoreDict:
        vendor_count = 0
        condition = str(flow[i, j])
        print (condition[(condition.rfind(' ')):(condition.rfind(')'))])
        if float(condition[(condition.rfind(' ')):(condition.rfind(')'))]) == 1.0:
            average = average + \
                (vendorScoreDict[
                 j] * float(condition[(condition.rfind(' ')):(condition.rfind(')'))]))
            vendor_hist_list.append(j)
            fileWriter.write(str(j) + '     ' + '\t' + str(i) +
                             '\t' + str(1700 - jobPriorityDict[i]) + '\n')
fileWriter.write('\n')

# Output total jobs assigned to each vendor in the vendor_score file
fileWriter.write("Vendor_ID" + '\t' + "Count" + '\n')
for i in vendorScoreDict:
    vendor_count = 0
    for j in jobPriorityDict:
        condition = str(flow[j, i])
        print (condition[(condition.rfind(' ')):(condition.rfind(')'))])
        if float(condition[(condition.rfind(' ')):(condition.rfind(')'))]) == 1.0:
            vendor_count = vendor_count + \
                float(
                    (condition[(condition.rfind(' ')):(condition.rfind(')'))]))
    fileWriter.write(str(i) + '     ' + '\t' + str(vendor_count) + '\n')
fileWriter.write('\n')

# Output the average score of all vendors after the jobs are assigned
fileWriter.write('Average vendor score: ' +
                 str(average / len(jobPriorityDict)))

# Close all the files
fileWriter.close()
fScoreVendorOpenUpdated.close()
fJobsOpen.close()
