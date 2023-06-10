from flask_restplus import reqparse, fields
from apps.cicd.restplus import api

unittestRunSerizlizers = api.model('unittestRun',{
    'job_name': fields.String(description='任务名称'),
    'gitLabName': fields.String(description='测试代码仓库链接'),
    'job_type': fields.Integer(description='任务类型'),
    'client_type': fields.String(description='端类型'),
    'app_url': fields.String(description='app下载链接'),
    'run_by': fields.String(description='执行人'),
})


unittestSetbackArguments = reqparse.RequestParser()
unittestSetbackArguments.add_argument('report', type=str, reqparse=False, help='测试报告')
unittestSetbackArguments.add_argument('run_result', type=str, reqparse=False, help='执行状态')
unittestSetbackArguments.add_argument('job_name', type=str, reqparse=False, help='任务名')
unittestSetbackArguments.add_argument('job_number', type=int, reqparse=False, help='任务序列号')
unittestSetbackArguments.add_argument('cases_sum', type=int, reqparse=False, help='用例总数')
unittestSetbackArguments.add_argument('cases_success', type=int, reqparse=False, help='用例成功数')
unittestSetbackArguments.add_argument('cases_failures', type=int, reqparse=False, help='用例失败数')
unittestSetbackArguments.add_argument('reportMp4', type=str, reqparse=False, help='录屏链接')
