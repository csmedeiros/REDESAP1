import os
def deletar(x):
    if x[0]=="del":
        caminhoPasta = x[2]
        nomeArquivo = x[1]
        caminhoCompleto = "{}/{}}".format(caminhoPasta, nomeArquivo)
        try:
            os.remove(caminhoCompleto)
            code = 0
            errorMsg = "arquivo apagado com sucesso"
            resposta = "{} {} {} {} {}".format(x[0], nomeArquivo, caminhoPasta, code, errorMsg)
            #conn.send(resposta.encode())
        except:
            if os.path.exists(caminhoPasta)==0:
                code = 1
                errorMsg = "caminho não existente no servidor"
                resposta = "{} {} {} {} {}".format(x[0], nomeArquivo, caminhoPasta, code, errorMsg)
                #conn.send(resposta.encode())
            elif os.path.exists(caminhoCompleto)==0:
                code = 2
                errorMsg = "nome de arquivo não existente no servidor"
                resposta = "{} {} {} {} {}".format(x[0], nomeArquivo, caminhoPasta, code, errorMsg)
                #conn.send(resposta.encode())
def listar(x):
    if x[0]=="list":    
        caminhoPasta = x[1]
        try:
            listaArquivos = os.listdir(caminhoPasta)
            code = 0
            errorMsg = "arquivos listados com sucesso"
            resposta = "{} {} {} {} {}".format(x[0], caminhoPasta, code, errorMsg, listaArquivos)
            #conn.send(resposta.encode())
        except:
            if os.path.exists(caminhoPasta)==0:
                code = 1
                errorMsg = "caminho não existente no servidor"
                resposta = "{} {} {} {} {}".format(x[0], caminhoPasta, code, errorMsg)
                #conn.send(resposta.encode())