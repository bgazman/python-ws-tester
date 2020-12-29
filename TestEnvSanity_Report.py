import DBHandler
from LogHandler import app_log
import RequestResponseHandler
import ReportFileHandler
import datetime
import sys

env = sys.argv[1]
build_num = sys.argv[2]
#env = 'SGIUT01'
#build_num = 'manual_16'
start_time = datetime.datetime.now()
try:
    db = DBHandler.db_connect()
except Exception,e:
    app_log.error("Unable to connect to DB: ")
    app_log.exception(e)
    raise
cursor = db.cursor()
try:
    results = DBHandler.selectTestCasesForEnv(cursor, env)
except Exception,e:
    app_log.error('Error :')
    app_log.exception(e)
    raise

for row in results:
    case_id = row[0]
    system_id = row[1]
    service_name = row[2]
    operation_name = row[3]
    uri = row[4]
    request_body = row[5]
    desired_response = row[6]
    system_name = row[7]
    system_host = row[8]
    system_port = row[9]
    version = row[10]
    ignoreArray = row[11]

    app_log.info('Handling Test Case With ID : ' + str(case_id ))
    response = RequestResponseHandler.handleRequest(system_host, system_port, uri, request_body, operation_name)
    diff = RequestResponseHandler.handleResponse(response, desired_response, ignoreArray)

    if diff is None or diff == 'No Expected Response' or diff == '':
        status = 'SUCCESS'
    else:
        status = 'FAILURE'

    try:
        DBHandler.insertReport(db, cursor, system_name, service_name, operation_name, case_id, response, status,
                               diff, build_num)
    except Exception, e:
        app_log.error('Insert Error:')
        app_log.exception(e)

end_time = datetime.datetime.now()
try:
    reportFile = ReportFileHandler.generateReportFile(cursor, build_num, env, start_time, end_time)
    # print 'Generated Build Test report:  ' + reportFile
    DBHandler.db_close(db)
    print open(reportFile).read()
except Exception as e:
    app_log.error("Error Generating report file: ")
    app_log.exception(e)

    print "Unable to generete repoty for Build Number: " + build_num  + " See LOG"


