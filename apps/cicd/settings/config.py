try:
    from public_config import *
except ImportError:
    pass

PORT = 9042
SERVICE_NAME = 'cicd'

#jenkins
LOGIN_USER= 'root'
LOGIN_PASSWORD= '123.com'
JENKINS_MASTER = 'http://127.0.0.1:8080/jenkins'
APPIUM_START_SH = f'/usr/local/bin/python3 /home/alen/tc/autotest/app_run.py'
APPIUM_START_DIR = f'/usr/alen/tc/testCase/appiumDemo'
H5_START_SH = f'/usr/local/bin/python3 /home/alen/tc/autotest/h5_run.py'
H5_START_DIR = f'/usr/alen/tc/testCase/h5Demo'