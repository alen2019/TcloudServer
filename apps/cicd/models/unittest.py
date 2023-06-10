from datetime import datetime
from library.api.db import db

def to_json(inst, cls):
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst,c.name)
        if isinstance(v,datetime):
            d[c.name] = v.strftime('%Y-%m-%d %H:%M:%S')
        else:
            d[c.name] = v
    return d

class UnittestConfig(db.Model):
    __tablename__ = 'unittest_log'

    id = db.Column(db.Integer, primary_key=True)
    job_number = db.Column(db.Integer)  #执行任务编号
    job_name = db.Column(db.String(64)) #执行任务名称
    job_type = db.Column(db.Integer)    #执行任务类型 1=h5|2=app
    client_type = db.Column(db.Integer) #端类型 android|ios
    app_url = db.Column(db.String(256)) #app下载链接
    run_by = db.Column(db.String(16))   #执行人
    run_time = db.Column(db.DateTime)   #执行时间
    run_result = db.Column(db.String(16))   #执行状态 进行中|异常|结束
    report = db.Column(db.String(64))   #测试报告
    reportMp4 = db.Column(db.String(64))    #测试过程录屏
    cases_sum = db.Column(db.Integer)   #执行用例总数
    cases_success = db.Column(db.Integer)   #执行用例成功数
    cases_failures = db.Column(db.Integer)  #执行用例失败数
    active = db.Column(db.Integer, default=1)   #标签 1=正常|2=失效

    def __repr__(self):
        return '<unittest_log %s>' % self.id

    @property
    def serialize(self):
        return to_json(self, self.__class__)
