import contextlib
import urllib2
from LogHandler import app_log
import DiffHandler
import XMLHandler
import Config


def combineURL(system_host,system_port,uri):
    url = "http://" + system_host + ":" + str(system_port) + uri
    return url

def generateRequest(url,request_body,operation_name):
    headers = {'Content-Type': 'text/xml;charset=UTF-8',
               'SOAPAction': operation_name}
    request = urllib2.Request(url, request_body, headers)

    return request

def httpRequest(url,request):
    try:
        response = urllib2.urlopen(request, timeout=Config.requestTimeout)
        content = response.read()

    except (urllib2.HTTPError, urllib2.URLError,Exception) as e:
        if str(e) == "HTTP Error 500: Server Error":
            content = e.read()
        else:
            app_log.error("reuqest to: " + url + " Failed: " + str(e))
            content = None

    return content

def handleRequest(system_host,system_port,uri,request_body,operation_name):
    app_log.info("Executing Request " )
    try:
        url = combineURL(system_host, system_port, uri)
        request = generateRequest(url,request_body,operation_name)
        response = httpRequest(url,request)
    except Exception,e:
        app_log.error('Error executing request: ')
        app_log.exception(e)
    return response

def handleResponse(response,desired_response,ignore_array):

    if response == '' or response is None:
        diff = 'Missing response. See Log'
    elif desired_response == '' or desired_response is None:
        diff = 'No Expected Response'
    else:
        try:
            app_log.info("Formatting XML and generating diff")
            resString = XMLHandler.format_xml(response, ignore_array)
            desiredResString = XMLHandler.format_xml(desired_response, ignore_array)
            diff = DiffHandler.diff(resString, desiredResString)
        except Exception, e:
            app_log.error("error handling response: ")
            app_log.exception(e)
            diff = "Diff error. See LOG"

    return diff




