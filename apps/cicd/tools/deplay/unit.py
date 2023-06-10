import unittest
import time
import os
import sys
import requests
from apps.cicd.tools.basice import *
from HTMLTestReportCN import HTMLTestRunner

#config


class Ut(object):
    def __init__(self):
        #配置文件
        self.LOG_FILE = '/home/alen/openSourceProject/tc/logs'
        self.ip = get_ip()
        self.setback_url = 'http://' +self.ip + ':9042/v1/unitsetBack/'
        self.startServer = appiumStart(4723)
        self.ti = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

    def run(self):
        self.dowloadApp()
        command = self.cmd(name)
        os.system(command)
        ret = self.startTest()
        command = 'killall scrcpy'
        os.system(command)
        self.setBack(ret)

    def startTest(self):
        try:
            LOG = self.LOG_FILE+ '/' + self.ti + '.html'
            report = 'http://'+self.ip+'/log/'+self.ti+'.html'
            reportMp4 = 'http://'+self.ip+'/log/'+self.ti+'.mp4'
            x = os.path.exists(self.LOG_FILE)
            if x == False:
                os.makedirs(self.LOG_FILE)
            unittestTest = unittest.defaultTestLoader.discover(start_dir=start_dir, pattern='test*.py')
            fp = open(LOG,'wb')
            runner = HTMLTestRunner(stream=fp, title=name,tester=run_by, description='用例执行情况')
            c = runner.run(unittestTest)
            all = c.testsRun
            success = c.success_count
            failure = c.failure_count
            fp.close()
        except Exception as e:
            print(str(e))
        return report, all, success, failure, reportMp4

    def setBack(self, startTest):
        report = startTest[0]
        all = startTest[1]
        success = startTest[2]
        failure = startTest[3]
        reportMp4 = startTest[4]
        try:
            callback_params = {'job_number':job_number, 'report':report, 'cases_sum':all,'cases_success':success,
                               'cases_failures':failure, 'run_result':'SUCCESS','job_name':name, 'reportMp4':reportMp4}
            sys.stdout.write('callback_params: %s\n' % (callback_params))
            req = requests.post(self.setback_url, params=callback_params)
            if req.status_code != 200:
                sys.stderr.write('UNITTEST SETBACK API ERROR:\n' % (req.status_code))
            else:
                sys.stdout.write('UNIT SETBACK SUCCESS\n')
        except Exception as e:
            callback_params = {'job_number': job_number, 'report': report, 'cases_sum': all, 'cases_success': success,
                               'cases_failures': failure, 'run_result': 'FAILURE', 'job_name': name, 'reportMp4': reportMp4}
            req = requests.post(self.setback_url, params=callback_params)
            sys.stdout.write('UNIT SETBACK SUCCESS\n'% (req.status_code))


    def dowloadApp(self):
        if job_type == '1':
            self.uninstallApp()
            try:
                headers = {'User-Agent':'xxxx'}
                file = requests.get(app_url, headers=headers, timeout=10)
                w = str(self.get_time())
                w = w.split('.')[0]
                filename = '/home/alen/tc/app/'+w+'.apk'
                with open(filename, 'wb') as apk:
                    apk.write(file.content)
                cmd = '/home/alen/Android/Sdk/platform-tools/adb -s 设备序列号 install' + filename
                os.system(cmd)
                time.sleep(10)
            except Exception as e:
                print(str(e))
        else:
            pass

    def uninstallApp(self):
        try:
            cmd = '/home/a;en/Android/Sdk/platform-tools/adb -s 设备序列号 uninstall com.taobao.aliAuction'
            os.system(cmd)
            time.sleep(2)
        except Exception as e:
            print(str(e))

    def get_time(self):
        return time.time()


    def cmd(self,name):
        if 'Online' in name:
            cmd = 'nohup scrcpy -m 800 -s 7HHHHHHHHHHH --no-display --record /home/alen/tc/log' + self.ti + '.mp4 &'
        else:
            cmd = 'nohup scrcpy -m 800 -s d5dddddddddd --no-display --record /home/alen/tc/log' + self.ti + '.mp4 &'
        return cmd

if __name__=='__main__':
    app_url = sys.argv[1]
    name = sys.argv[2]
    run_by = sys.argv[3]
    job_number = sys.argv[4]
    start_dir = sys.argv[5]
    job_type = sys.argv[6]
    d = Ut
    d.run()