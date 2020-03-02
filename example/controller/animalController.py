from flask import render_template
from animalModel import ModelAnimal

class CtrlAnimal:
    
    def render_page(self):
        animals = ModelAnimal().get_animals()
        return render_template('animal.html', animals=animals)
    
    def create_animal(self, data):
        print(data)
        name, description = data['name'], data['description']
        animal = ModelAnimal()
        animal.set_name(name)
        animal.set_description(description)

        if animal.create_animal():
            return "Criado com sucesso!"
        return "Ocorreu um erro"

