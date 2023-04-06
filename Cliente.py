class PTATCliente: 
    def criaRequisicao(entrada:str):
        import os
        x = entrada.split()
        if entrada=="" or entrada==" "*len(entrada):
            return("Nada inserido. Insira a operação desejada e seus respectivos parâmetros.")
        elif x[0]!="read" and x[0]!="write" and x[0]!="del" and x[0]!="list":
            return("Operação inválida")
        elif x[0] == "read":
            op = "0"
            caminhoRemoto = x[1]
            i = caminhoRemoto.rfind('/')
            path = caminhoRemoto[0:i]
            while len(path)<128:
                path+='?'
            fileName = caminhoRemoto[i+1:len(caminhoRemoto)]
            while len(fileName)<64:
                fileName+='?'
            length = "??????"
            requisicao = op+length+fileName+path
            return(requisicao)
        elif x[0]=="write":
            op = "1"
            caminhoLocal = x[1]
            caminhoRemoto = x[2]
            if os.path.exists(caminhoLocal)==0:
                return("Arquivo local não encontrado. Certifique-se que o caminho foi digitado corretamente ou que arquivo exista na pasta.")
            else:
                with open(caminhoLocal) as r:
                    body = r.read()
                length = len(body)
                length = str(length)
                while len(length)<6:
                    length = length+'?'
                i = caminhoRemoto.rfind('/')
                path = caminhoRemoto[0:i]
                while len(path)<128:
                    path+='?'
                fileName = caminhoRemoto[i+1:len(caminhoRemoto)]
                while len(fileName)<64:
                    fileName+='?'
                requisicao = op+length+fileName+path+body
                return(requisicao)
        elif x[0]=="del":
            op="2"
            caminhoRemoto = x[1]
            i = caminhoRemoto.rfind('/')
            path = caminhoRemoto[0:i]
            while len(path)<128:
                path+='?'
            fileName = caminhoRemoto[i+1:len(caminhoRemoto)]
            while len(fileName)<64:
                fileName+='?'
            length = "??????"
            requisicao = op+length+fileName+path
            return(requisicao)
        elif x[0]=="list":
            op="3"
            path = x[1]
            while len(path)<128:
                path+='?'
            fileName = '?'*64
            length='?'*6
            requisicao = op+length+fileName+path
            return(requisicao)
    def clienteServidor(req):
        import socket
        serverAddress = "127.0.0.1"
        if len(req)<199:
                print(req)
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
                clientSocket.connect((serverAddress, 12000))
                clientSocket.send(req.encode())
                resposta = clientSocket.recv(1024).decode()
                mensagem = resposta[200:327]
                mensagem = mensagem.replace("?", "")
                if len(resposta)==328:
                    respostaFormatada = "Código:{} -> {}".format(resposta[199], mensagem)
                    if verbose == True:
                        print(respostaFormatada)
                elif len(resposta)>328:
                    respostaFormatada = "Código:{} -> {}\nConteudo: {}".format(resposta[199], mensagem, resposta[328:len(resposta)])
                    if verbose == True:
                        print(respostaFormatada)
if __name__=='__main__':
    while True:
        verbose = False
        cmd = input("PTAT:/ client >>> ")
        requisicao = str(PTATCliente.criaRequisicao(cmd))
        PTATCliente.clienteServidor(requisicao)