class Protocolo:
    def __init__(self, comando, endereco, mensagem):
        self.comando = comando
        self.endereco = endereco
        self.mensagem = mensagem


    def criaArquivo(self):
        file1 = open(self.endereco, "w")
        if (len(self.mensagem) <= 128):
            file1.write(self.mensagem)
            return "Arquivo escrito com sucesso"
        else:
            return "Tamanho do arquivo para ser escrito maior que tamanho máximo permitido"

    def __str__(self):
         if (self.comando == "read"):
            return Protocolo.criaArquivo(self)