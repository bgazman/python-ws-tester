from werkzeug.wrappers import Request, Response
import subprocess
import Config

@Request.application
def application(request):
    print 'got request'
    try:
        function = request.args.get('function', 'default')
        print function
        if function == 'testEnvSanity':
            print 'got request'
            env = request.args.get('env', 'default')
            build_num = request.args.get('build_num', 'default')
            print env
            print build_num
            if env is None or build_num is None or env == '' or build_num == '':
                return Response(
                        htmlHeader + '<h1>Incorrect Usage</h1><h2>host:port?function=functionName&param1=x&param2=y</h2>' + htmlFooter)
            else:
                cmd = 'python TestEnvSanity_Report.py ' + env + ' ' + build_num
                print cmd
                execCmd = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
                diff = execCmd.stdout.read()
                print diff
                return Response(diff)


        elif function is None or function == 'default':
            return Response(
                htmlHeader + '<h1>Incorrect Usage</h1><h2>host:port?function=functionName&param1=x&param2=y</h2>' + htmlFooter)
        else:
            return Response('Unavailable function')
    except Exception,e:
        print e
        return Response(htmlHeader +'<h1>Error Occured</h1><p>' + str(e) + '</p>' + htmlFooter)




htmlHeader = """<html><body>"""
htmlFooter = """</body></html>"""

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('borisga01', 4000, application)

def testEnvSanity(request):
    print 'got request'
    env = request.args.get('env','default')
    print env
    build_num = request.args.get('build_num', 'default')
    print build_num
    cmd = 'python TestEnvSanity.py ' + env + ' ' + build_num
    print cmd
    execCmd = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    diff = execCmd.stdout.read()
    print diff
    return Response()