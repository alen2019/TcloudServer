from flask import current_app
from apps.cicd.settings.config import *
from apps.cicd.tools.basice import *
from apps.cicd.tools.jenkins import Job
from apps.cicd.models.unittest import UnittestConfig
from library.api.db import db

class UnittestRunBusiness(object):
    @classmethod
    def unittestRun(cls, data):
        job_name = data.get('job_name')
        job_type = data.get('job_type')
        client_type = data.get('client_type')
        app_url = data.get('app_url')
        run_by = data.get('run_by')
        gitLabName = data.get('gitLabName')
        job_number = get_number()
        if job_type == 2:
            app_url = 'https://www.baidu.com'
        if app_url is None or job_name is None:
            return {'code':1000, 'message':'请检查必填字段', 'result':''}
        try:
            server = Job(jenkins_master=JENKINS_MASTER, login_user=LOGIN_USER, login_password=LOGIN_PASSWORD)
            if client_type == 'android':
                start_sh = APPIUM_START_SH
                client_type = 'appium'
                start_dir = '测试服务器jenkisn工程目录' + gitLabName
            else:
                return {'code':1000, 'message':'配置不存在，请联系管理员', 'result':''}
            server.startUnittest(client_type=client_type, app_url=app_url, name=job_name, run_by=run_by,
                                 job_number=job_number, start_sh=start_sh, start_dir=start_dir, job_type=job_type)
            try:
                m = UnittestConfig(
                    job_number=job_number,
                    job_name=job_name,
                    job_type=job_type,
                    client_type=client_type,
                    app_url=app_url,
                    run_by=run_by,
                    run_result='BUILDING',
                    run_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                )
                db.session.add(m)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return {'code': 1000, 'message': '保存数据失败', 'result': str(e)}
            return {'code': 0, 'message': '启动成功', 'result': 'BUILDING'}
        except Exception as e:
            current_app.logger.error(e)
            return {'code': 1000, 'message': '启动失败', 'result': str(e)}

    @classmethod
    def setback(cls,data):
        job_name = data.get('job_name')
        job_number = data.get('job_number')
        report = data.get('report')
        reportMp4 = data.get('reportMp4')
        cases_sum = data.get('cases_sum')
        cases_success = data.get('cases_success')
        cases_failures = data.get('cases_failures')
        run_result = data.get('run_result')
        the_cb = UnittestConfig.query.order_by(db.desc(UnittestConfig.id)).filter(UnittestConfig.job_number== job_number).first()
        try:
            the_cb.report = report,
            the_cb.reportMp4 = reportMp4,
            the_cb.cases_sum = cases_sum,
            the_cb.cases_success = cases_success,
            the_cb.cases_failures = cases_failures,
            the_cb.run_result = run_result
            db.session.add(the_cb)
            db.session.flush()
            db.session.commit()
            ret = the_cb.serialize
            return {'code': 0, 'message': 'success', 'result': ret}
        except Exception as e:
            db.session.rollback()
            return {'code': 1000, 'message': '保存数据库失败，请联系管理员', 'result': str(e)}