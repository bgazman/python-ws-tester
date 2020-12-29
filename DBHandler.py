import Config
import MySQLdb
from LogHandler import app_log


###################################### SQL Statements   ########################################
sqlInsertReport = """INSERT
           INTO
           `reports`(`system_name`,`service_name`, `operation_name`, `case_id`, `response`, `result`,`diff`,`build_num`)
           VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"""
# execute SQL query using execute() method.

sqlSelectTestCasesForEnv = """SELECT test_cases.id,test_cases.system_id,test_cases.service_name,test_cases.operation_name,test_cases.uri,test_cases.request_body,test_cases.desired_response,systems.name,systems.host,systems.port,test_cases.version,test_cases.response_ignore from test_cases,systems where
systems.id = test_cases.system_id and systems.env =  %s"""

sqlSelectTestCase = """SELECT test_cases.id,test_cases.system_id,test_cases.service_name,test_cases.operation_name,test_cases.uri,test_cases.request_body,test_cases.desired_response,systems.name,systems.host,systems.port,test_cases.version,test_cases.response_ignore from test_cases,systems where
systems.id = test_cases.system_id  and test_cases.id= %s"""

sqlSelectReportsForBuild = """SELECT * FROM REPORTS WHERE build_num = %s"""

sqlSelectReportSummaryForBuild = """select
    (select count(*) from reports where build_num = %s) as total,
    (select count(*) from reports where build_num = %s and result = 'SUCCESS') as success ,
    (select count(*) from reports where build_num = %s and  result = 'FAILURE') as failure """




sqlUpdateDesiredResponseForCase= """UPDATE `test_cases` SET `desired_response`=%s WHERE `id`=%s;"""


######################################  SQL Statements   ######################################## db, cursor, system_name, service_name, operation_name, str(id), content, status, diff, BuildNum

def insertReport(db,cursor,system_name,service_name,operation_name,case_id,content,status,diff,buildNum):
    try:
        if Config.os == 'WIN':
            cursor.execute(sqlInsertReport, [system_name, service_name, operation_name, str(case_id),
                                            content, status, diff, buildNum])
        else:
            cursor.execute(sqlInsertReport, (system_name, service_name, operation_name, str(case_id),
                                            content, status, diff, buildNum))
        db.commit()
        app_log.info("Inserted report " + str(cursor.lastrowid))
    except Exception,e:
                db.rollback()
                error = "Unable to Insert result for  " + service_name + " Operation Name: " + operation_name + ",caseId: " + str(case_id) + ": "
                app_log.error(error + str(e))
                raise


def updateDesiredResponseForCase(db,cursor,case_id,desired_response):
    try:
        if Config.os == 'WIN':
            cursor.execute(sqlUpdateDesiredResponseForCase, [desired_response,case_id])
        else:
            cursor.execute(sqlUpdateDesiredResponseForCase, (desired_response,case_id))
        db.commit()
        app_log.info("Updated Test Case : " + str(case_id))
    except Exception as e:
        db.rollback()
        raise




def selectTestCase(cursor,case_id):
    try:
        if Config.os == 'WIN':
            cursor.execute(sqlSelectTestCase, [case_id])
        else:
            cursor.execute(sqlSelectTestCase, (case_id))
        results = cursor.fetchall()
        app_log.info("Got " + str(len(results)) + " cases from DB for caseId: " + str(case_id))
        return results
    except Exception, e:
        error = "Error: unable to fecth data from DB for caseId : " + str(case_id)
        app_log.error(error + str(e))
        raise


def selectReportsForBuild(cursor,build_num):
    try:
        if Config.os == 'WIN':
            cursor.execute(sqlSelectReportsForBuild, [build_num])
        else:
            cursor.execute(sqlSelectReportsForBuild, (build_num))
        results = cursor.fetchall()
        app_log.info("Got " + str(len(results)) + " reports from DB for Build Number: " + str(build_num))
        return results
    except Exception, e:
        error = "Error: unable to fecth data from DB for Build Number: " + str(build_num)
        app_log.error(error + str(e))
        raise


def selectReportSummaryForBuild(cursor,build_num):
    try:
        if Config.os == 'WIN':
            cursor.execute(sqlSelectReportSummaryForBuild, [build_num,build_num,build_num])
        else:
            cursor.execute(sqlSelectReportSummaryForBuild, (build_num,build_num,build_num))
        results = cursor.fetchall()
        app_log.info("Got report summary from DB for  Build Number: " + str(build_num))
        return results
    except Exception, e:
        error = "Error: unable to fecth report summary from DB for Build Number:  " + str(build_num) + " "
        app_log.error(error + str(e))
        raise


def selectTestCasesForEnv(cursor,env):
    try:
        if Config.os == 'WIN':
            cursor.execute(sqlSelectTestCasesForEnv, [env])
        else:
            cursor.execute(sqlSelectTestCasesForEnv, (env))
        results = cursor.fetchall()
        app_log.info("Got" + str(len(results)) + "cases from DB for env: " + str(env))
        return results
    except Exception, e:
        error = "Error: unable to fecth data from DB for env : " + str(id)
        app_log.error(error + str(e))
        raise


def db_connect():
    try:
        return MySQLdb.connect(
        host=Config.dbHost,
        user=Config.dbUser,
        passwd=Config.dbPassword,
        db=Config.dbName,
        port=Config.dbPort)
    except Exception, e:
        error = "Unable to connect to DB: "
        app_log.error(error + str(e))
        raise


def db_close(dbConn):
    try:
        dbConn.close()
    except Exception,e:
        app_log('Unable To close db Connection: ' + str(e))


