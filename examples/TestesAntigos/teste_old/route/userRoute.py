
from flask import Blueprint, Flask, jsonify, request
from userrController import CtrlUser


app_user = Blueprint('user', __name__)


@app_user.route('/user', methods=['GET'])
def render_user():
    return CtrlUser().render_page()

@app_user.route('/api/user', methods=['POST'])
def create_user():
    data = request.get_json()
    print(request)
    print("aa")
    print(data)
    new_user = CtrlUser().create_user(data)

    return jsonify(
        status=200,
        data=new_user
    )