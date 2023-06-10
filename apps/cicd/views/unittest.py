from library.api.tBlueprint import tblueprint
from flask_restplus import Resource
from apps.cicd.restplus import api
from flask import request,jsonify
from apps.cicd.business.unittest import UnittestRunBusiness
from apps.cicd.validations.unittest import unittestRunSerizlizers, unittestSetbackArguments

bpname = 'unittest'
view_permission = f'{bpname}_view'
modify_permission = f'{bpname}_modify'
Unittest = tblueprint(bpname, __name__)
UnittestApp = api.namespace('Unittest', path='/', description='Unittest调度接口')
headParser = UnittestApp.parser()
headParser.add_argument('Authorization', location='headers')

@UnittestApp.route('/unittestRun/')
class unittestRun(Resource):
    @UnittestApp.expect(unittestRunSerizlizers)
    def post(self):
        date = request.json
        result = UnittestRunBusiness.unittestRun(date)
        return jsonify(result)

@UnittestApp.route('/unittestSetback')
class setback(Resource):
    @UnittestApp.expect(unittestSetbackArguments)
    def post(self):
        data = unittestSetbackArguments.parse_args(request)
        result = UnittestRunBusiness.setback(data)
        return jsonify(result)