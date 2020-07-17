class Pessoa:

    def __init__(self, nome):
        self.nome = nome
    
    def print(self, inteiro_qualquer):
        print(self.nome)
    
    def retorno_maluco1(self): 
        return self.retorno_maluco2()
    
    def retorno_maluco2(self):
        return self.retorno_maluco3()
    
    def retorno_maluco3(self):
        input_qualquer = input()
        if (input_qualquer == "4"):
            return ()
        return {}