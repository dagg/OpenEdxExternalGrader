import BaseHTTPServer

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
import threading

import json
import os
import subprocess
import re
import time
import random

import gc

# Random file name generator
def randgen():
	return str(random.random()).split('.')[-1]+'_'+str('%.6f' % time.time()).split('.')[-1]

class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        pass

    def do_GET(self):
        pass

    def do_POST(self):
        body_len = int(self.headers.getheader('content-length', 0))
        body_content = self.rfile.read(body_len)
        problem_name, student_response = get_info(body_content)
        result = grade(problem_name, student_response)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(result)
        
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ This class allows to handle requests in separated threads.
        No further content needed, don't touch this. """


class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        body_len = int(self.headers.getheader('content-length', 0))
        body_content = self.rfile.read(body_len)
        problem_name, student_response = get_info(body_content)
        result = grade(problem_name, student_response)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(result)
        
def grade(problem_name, student_response):
    randfilename = randgen()

    # Create python file to be tested from student's submitted program
    program_name = "Program{0}_{1}.py".format(problem_name['problem_name'], randfilename)
    source_file = open(program_name, 'w')
    source_file.write(student_response)
    source_file.close()

    correct = True
    message = "Good job!!!"
    
    # Use pytest to test the student's submitted program with the help of the appropriate test runner 
    p = subprocess.Popen(["py.test", "{0}_test_runner.py".format(problem_name['problem_name']), program_name, "-v"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err  = p.communicate()

    # print "Out is: >>>\n{0}\n<<<".format(out)
    # print "Err is: >>>\n{0}\n<<<".format(err)
    
    if 'FAILED' in out or '= ERRORS =' in out:
        correct = False
        message = 'Test Failed'

    if err:
        correct = None
        message = 'There was a problem with the testing'

    result = {}
    result.update({"correct": correct, "msg": message,})
    result = process_result(result)
    
    #remove student's program from disk
    os.remove(program_name)
    
    #garbage collect
    gc.collect()
    return result
    
    
def process_result(result):
    correct = result["correct"]
    message = result["msg"]
    
    if not correct:
        score = None
    elif (correct == True):
        score = 1
    else:
        score = 0

    result = {}
    result.update({"correct": correct, "score": score, "msg": message })
    result = json.dumps(result)
    return result
     
def get_info(body_content):
    json_object = json.loads(body_content)
    json_object = json.loads(json_object["xqueue_body"])
    problem_name = json.loads(json_object["grader_payload"])
    student_response = json_object["student_response"]
    return problem_name, student_response


if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 1710), Handler)
    print 'Starting server on port 1710...'
    server.serve_forever()
    