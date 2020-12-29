import DBHandler
from LogHandler import app_log
import RequestResponseHandler
import sys

#case_id = sys.argv[1]
case_id = '57'
build_num = 'testCase'

try:
    db = DBHandler.db_connect()
except Exception,e:
    app_log.error("Unable to connect to DB: ")
    app_log.exception(e)
    raise
cursor = db.cursor()
try:
    results = DBHandler.selectTestCase(cursor, case_id)
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


    response = RequestResponseHandler.handleRequest(system_host, system_port, uri, request_body, operation_name)


    diff = RequestResponseHandler.handleResponse(response, desired_response, ignoreArray)

    if diff is None or diff == 'No_Request_Body' or diff == '':
        status = 'SUCCESS'
    else:
        status = 'FAILURE'

    try:
        DBHandler.insertReport(db, cursor, system_name, service_name, operation_name, case_id, response, status,
                               diff, build_num)
    except Exception, e:
        app_log.error('Insert Error:')
        app_log.exception(e)


report_id = cursor.lastrowid
DBHandler.db_close(db)

if report_id == 0:
    print 'Error : Report not inserted to DB'
else:
    print 'Test Executed. Generate Report: ' + str(report_id) + ' see DB'
