#!/usr/bin/python
# -*- coding: UTF-8 -*-
import jenkins
import datetime

def singleton(cls):
    """
    单例模式
    """
    _instance = {}
    def inner(*args, **kw):
        jenkins_master = kw.get('jenkins_master')
        if not jenkins_master:
            jenkins_master = args[0]
        if jenkins_master not in _instance:
            _instance[jenkins_master] = cls(*args, **kw)
        return _instance[jenkins_master]
    return inner

@singleton
class Job(object):
    """
    jenkins操作类
    """
    def __init__(self, jenkins_master, login_user, login_password, jenkins_job=None):
        self.jenkins_master = jenkins_master
        self.jenkins_job = jenkins_job
        self.login_user = login_user
        self.login_password = login_password
        self.jenkins_object = None

    def getObject(self):
        """
        登陆jenkins
        """
        if not self.jenkins_object:
            self.jenkins_object = jenkins.Jenkins(self.jenkins_master, self.login_user, self.login_password)
        return self.jenkins_object

    def getJobName(self, job_name=None):
        return self.getObject().get_job_name(job_name)


    def getBuildInfo(self,job_name,buildnumber):
        return self.getObject().get_build_info(job_name, buildnumber)

    def getBuildConsoleOutput(self,job_name=None,buildnumber=None):
        if job_name is None:
            job_name = self.jenkins_job
        if buildnumber is None:
            buildnumber = self.get_job_info(job_name)
        return self.getObject().get_build_console_output(job_name, buildnumber)

    def getInfo(self, job_name):
        return self.getObject().get_job_info(job_name)['lastCompletedBuild']['number']

    def startUnittest(self, client_type=None, app_url=None, name=None, run_by=None, job_number=None, start_sh=None, start_dir=None, job_type=None):
        """
        调度jenkins任务
        client_type = jenkisn任务名
        """
        token = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')
        if 'appium' in client_type:
            parameters = {'app_url':app_url, 'name':name, 'run_by':run_by, 'job_number':job_number, 'start_sh':start_sh, 'start_dir':start_dir, 'job_type':job_type}
            return self.getObject().build_job(client_type,parameters=parameters, token=token)
        else:
            return client_type
if __name__=='__main__':
        server = Job(jenkins_master='http://localhost:8080', login_user='root', login_password='123.com').getObject()
        print(server.get_jobs())