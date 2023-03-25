def criaArquivo(endereco, mensagem):
    file1 = open(endereco, "w")
    if (len(mensagem) <= 128):
        file1.write(mensagem)
        return "Arquivo escrito com sucesso"
    else:
        return "Tamanho do arquivo para ser escrito maior que tamanho máximo permitido"
    

print(criaArquivo("testeDeTexto.txt", "Teste de mensagemTeste de mensagemTeste de mensagemTeste de mensagemTeste de mensagemTeste de mensagemTeste de mensagemTeste de mensagem"))