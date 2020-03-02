from flask import Blueprint, Flask, jsonify, request
from carroController import CtrlCarro


app_carro = Blueprint('carro', __name__)


@app_carro.route('/carro', methods=['GET'])
def create_carro_render():
    return CtrlCarro().render_page()

@app_carro.route('/api/carro', methods=['POST'])
def create_carro():
    data = request.get_json()
    print(request)
    print("aa")
    print(data)
    new_carro = CtrlCarro().create_carro(data)

    return jsonify(
        status=200,
        data=new_carro)