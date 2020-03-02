from flask import render_template
from userModel import ModelUser

class CtrlUser:
    
    def render_page(self):
        users = ModelUser().get_users()
        return render_template('user.html', users=users)
    
    def create_user(self, data):
        print(data)
        name, description = data['name'], data['description']
        user = ModelUser()
        user.set_name(name)
        user.set_description(description)

        if user.create_user():
            return "Criado com sucesso!"
        return "Ocorreu um erro"

