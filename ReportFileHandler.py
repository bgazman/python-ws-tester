from string import Template
import datetime
import DBHandler
import Config
from LogHandler import app_log

initTemplate= Template("""<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="generator" content="SQL*Plus 11.2.0">
<title>Automatic Testing Report </title>  <style type='text/css'>         body { font-family:Tahoma; font-size:10px; }         h1   { color:red; }         td,th { border:1px solid #152614; }         th { padding:5px; text-align:center; background-color: #e0e0e0; }         td { padding:3px 5px 3px 5px; }         tr:hover { color:red; }         .table-theme1 th { background-color:#e0e0e0; }         .table-theme1 .column-header1 { background-color:#c0c0c0; }         .amdocs-logo1 { font-style:bold; font-size:15px; color:#ff9900; }         .amdocs-logo-sub1 { font-size:10px; color:#153e7e; }         ul { padding:0; }         li { display: inline-block; }           .right-align { text-align:right }          .left-align { text-align:left} td.SUCCESS{background-color:#66ff33;} td.FAILURE{background-color:#ff3300; table tr:nth-last-child(3) { font-weight: bold; background: #e0e0e0; }  </style>
</head>
<body>
<h1>Automatic Testing Report for Build Number : $build_num on Environment: $env</h1>
<body>
<p><h2>Environment = $env, Build No. = $build_num <br />
	Started @ $start_time, Finished @ $end_time
	<h2>
</p>
<table border='1' width='90%' align='center' summary='Script output'>
<tr>
<th scope="col">
System
</th>
<th scope="col">
Service Name
</th>
<th scope="col">
Operation Name
</th>
<th scope="col">
Case Number
</th>
<th scope="col">
DB Report ID
</th>
<th scope="col">
Build Number
</th>
<th scope="col">
Test Result
</th>
<th scope="col">
Diff
</th>
</tr>""")

finalHTML = """

</table>
</body>
</html>"""

BodyTemplate = Template("""<tr>
<td>
$system_name
</td>
<td>
$service_name
</td>
<td align="right">
$operation_name
</td>
<td align="right">
$case_id
</td>
<td align="right">
$report_id
</td>
<td align="right">
$build_num
</td>
<td class ="$result" align="right">
$result
</td>
<td align="right">
$diff
</td>
</tr>""")


sumTemplate = Template("""<tr><td colspan="8">SUMMARY: Pass-Rate=$rate%, Test-Cases Total=$total, Success=$success, Failure=$failure.</td></tr>""")

def generateFileName(build_num):
    fileName  =Config.app_home + '/Reports/'  + str(build_num)  + '.html'
    return fileName

def initializeHTMLFile(fileName,build_num,env,start_time,end_time):
    data = initTemplate.substitute(env=env, build_num=build_num, start_time=start_time, end_time=end_time)
    fileWrite(fileName,data)

def finalizeHTMLFile(fileName):
   fileAppend(fileName,finalHTML)

def fileWrite(fileName,data):
    file = fileName
    htmlFile = open(file, "w")
    htmlFile.write(data)

def fileAppend(fileName,data):
    file = fileName
    htmlFile = open(file, "a")
    htmlFile.write(data)



def generateReportBody(cursor,build_num):
    body = ''
    results = DBHandler.selectReportsForBuild(cursor,build_num)
    for row in results:
        report_id = row[0]
        system_name = row[1]
        service_name = row[2]
        operation_name = row[3]
        case_id = row[4]
        response = row[5]
        result = row[6]
        diff = row[7]
        build_num= row[8]
        #date = row[10]
        fileRow = BodyTemplate.substitute(system_name=system_name, service_name=service_name,
                                      operation_name=operation_name, case_id=case_id,
                                      result=result,report_id=report_id, build_num=build_num, diff=diff)
        body += fileRow
    return body

def generatReportSummary(cursor,build_num):
    results = DBHandler.selectReportSummaryForBuild(cursor,build_num)
    for row in results:
        total = row[0]
        success = row[1]
        failure = row[2]
        if success > 0:
            rate = success / float(total) * 100
        else:
            rate = 0

        summary = sumTemplate.substitute(rate=rate, total=total, success=success,
                                                       failure=failure)
    return summary



def generateReportFile(cursor,build_num,env,start_time,end_time):
    fileName = generateFileName(build_num)
    initializeHTMLFile(fileName, build_num, env, start_time, end_time)
    body = generateReportBody(cursor, build_num)
    summary = generatReportSummary(cursor, build_num)
    fileAppend(fileName, body)
    fileAppend(fileName, summary)
    finalizeHTMLFile(fileName)


    return fileName