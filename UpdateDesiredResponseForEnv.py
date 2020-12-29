import DBHandler
from LogHandler import app_log
import RequestResponseHandler
import sys

#env = sys.argv[1]
env = 'SGIUT01'
#build_num = 'testCase'

try:
    db = DBHandler.db_connect()
except Exception,e:
    app_log.error("Unable to connect to DB: ")
    app_log.exception(e)
    raise
cursor = db.cursor()
try:
    results = DBHandler.selectTestCasesForEnv(cursor, env)
    app_log.info("Got  " + str())
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
    if response == '' or response is None:
        print "Unable to Update Desired Response for Test Case " + str(case_id) + " Response is empty"
    else:
        try:
            DBHandler.updateDesiredResponseForCase(db, cursor, case_id, response)
            print "Updated Desired Response for Test Case " + str(case_id)
        except Exception as e:
            print "Unable to Update Desired Response for Test Case " + str(case_id)
            app_log.error("Unable to update test case:   " + str(case_id))
            app_log.exception(e)



DBHandler.db_close(db)
