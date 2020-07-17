from flask import render_template
from carroModel import ModelCarro

class CtrlCarro:
    
    def render_page(self):
        carros = ModelCarro().get_carros()
        return render_template('carro.html', carros=carros)
    
    def create_carro(self, data):
        name, description, marca = data['name'], data['description'], data['marca']
        carro = ModelCarro()
        carro.set_name(name)
        carro.set_description(description)
        carro.set_marca(marca)

        if carro.fabricar_carro():
            return "Criado com sucesso!"
        return "Ocorreu um erro"
    


