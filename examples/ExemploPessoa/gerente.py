from pessoa import Pessoa 

class Gerente(Pessoa):
    
    def __init__(self, nome, salario):
        # Pessoa.__init__(self, nome) #Funciona
        super(Gerente, self).__init__(nome) #Funciona
        self.salario = salario
    
    

if __name__ == "__main__":
    g = Gerente("eduardo", 1000)
    funciona = g.retorno_maluco1()
    functiona2 = g.retorno_maluco2()
