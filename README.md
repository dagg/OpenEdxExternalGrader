# OpenEdxExternalGrader
Simple External Grader for Python Problems in OpenEDX platform

After a lot of searching and disappointment from lack of documentation I have managed to find a solution to the External Grader problem in OpenEDX platform.

After my post here: 
https://groups.google.com/d/msg/edx-code/-xMxjjg6uv8/nSHvkBn0HAAJ

I created the grader I have posted here for anyone who needs something similar, to have...
I need to thank the person that created the Java Grader here: https://github.com/huynq55/java-grader
since most of the code I got from him with some changes that fit my case.

Note: I didn't manage to make it work on Birch release, but with the newest release (dogwood) it seems to work well so far.

The process to setup an external grader in OpenEDX (dogwood named release) goes as following:

First create a new course (or a new problem inside a course) similar to the one I have here.
You can download the file "course.0hhL51.tar.gz", import it in your OpenEDX platform and see how the problems are set up.

You can also download directly the "PP1_Problem_Sample.xml" file, which is the "Blank Advanced Problem's" XML to create a sample Python problem to be graded with our external grader.

XQueue configuration:
Edit the "/edx/app/xqueue/xqueue.env.json" file to look like this:
```
{
    "LOCAL_LOGLEVEL": "INFO",
    "LOGGING_ENV": "sandbox",

    "LOG_DIR": "/edx/var/log/xqueue",

    "RABBIT_HOST": "localhost",
    "S3_BUCKET": "sandbox-bucket",
    "S3_PATH_PREFIX": "sandbox-xqueue",
    "SYSLOG_SERVER": "localhost",
    "XQUEUES": {
        "certificates": null,

        "py-queue": "http://localhost:1710",
        "open-ended": null,
        "open-ended-message": null,

        "test-pull": null
    },
    "XQUEUE_WORKERS_PER_QUEUE": 12
}
```
The "py-queue": "http://localhost:1710" line is the most important here, as the xqueue will look for the grader at the port 1710 (you can use any port you like of course as long as you use the same to initialize the HTTPServer in the PythonGrader.py program). Also, "py-queue" is the queue name used in each problem's xml to declare which queue to follow (you can see it in here: "PP1_Problem_Sample.xml").

After editing the "/edx/app/xqueue/xqueue.env.json" file, you need to restart the xqueue server using the following command:
```
sudo /edx/bin/supervisorctl restart xqueue:
```
This didn't quite work for me though and I had to restart the whole server for some reason (or all the running services, it's the same), and then it seemd to work correctly.

Then, go to the directory in your server where you have cloned my grader files from here and run:
```
$ python PythonGrader.py
```

This will start the grader's HTTPServer which accepts the user's input, creates a unique file with the answer, runs the appropriate unit test (using Pytest) to check if the problem is correct, and responds back to the xqueue (and then to OpenEDX) with an answer, either correct or not, for grading the student's response.

You must leave the PythonGrader.py running, else the grader will stop.

Some of the PythonGrader.py code is from https://github.com/huynq55/java-grader I mentioned above but I had to change it due to some problems:
The JavaGrader created a single file with the student's answers (no matter what the problem or the student was) and so, if 2 students tried to answer at the same time at different (or the same) problems, the grader was confusing the results (since it tested the code from the same file for all students).
For that reason, I create a different file for each time each student answers, with a random filename, and then run a test for this particular file for its validity and correctness.
After the file is read and the result is ready to be sent back to the platform, I delete the file so it will not take up too much space on disk.

That's all for now, I hope this was helpful and if someone has a better idea on how to make this work more efficiently I will be glad to see it, or answer any questions you might have.
