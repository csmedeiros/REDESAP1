while True:
    cmd = input("PTAT:/ client >>> ")

    class PTATCliente:
        def __init__(self):
            self.requisicao = True
        def criaRequisicao(self, entrada:str):
            import os
            x = entrada.split()
            if x[0] == "read":
                op = "0"
                caminhoRemoto = x[1]
                i = caminhoRemoto.rfind('\\')
                path = caminhoRemoto[0:i]
                while len(path)<128:
                    path+='?'
                fileName = caminhoRemoto[i+1:len(caminhoRemoto)]
                while len(fileName)<64:
                    fileName+='?'
                length = "??????"
                requisicao = op+length+fileName+path
                return(requisicao)
            if x[0]=="write":
                op = "1"
                caminhoLocal = x[1]
                caminhoRemoto = x[2]
                if os.path.exists(caminhoLocal)==0:
                    print("Arquivo local não encontrado. Certifique-se que o caminho foi digitado corretamente ou que arquivo exista na pasta.")
                else:
                    with open(caminhoLocal) as r:
                        body = r.read()
                    length = len(body)
                    length = str(length)
                    while len(length)<6:
                        length = length+'?'
                    i = caminhoRemoto.rfind('\\')
                    path = caminhoRemoto[0:i]
                    while len(path)<128:
                        path+='?'
                    fileName = caminhoRemoto[i+1:len(caminhoRemoto)]
                    while len(fileName)<64:
                        fileName+='?'
                    requisicao = op+length+fileName+path+body
                    return(requisicao)
            if x[0]=="del":
                op="2"
                caminhoRemoto = x[1]
                i = caminhoRemoto.rfind('?')
                path = caminhoRemoto[0:i]
                while len(path)<128:
                    path+='?'
                fileName = caminhoRemoto[i+1:len(caminhoRemoto)]
                while len(fileName)<64:
                    fileName+='?'
                length = "??????"
                requisicao = op+length+fileName+path
                return(requisicao)
            if x[0]=="list":
                op="3"
                path = x[1]
                while len(path)<128:
                    path+='?'
                fileName = '?'*64
                length='?'*6
                requisicao = op+length+fileName+path
                return(requisicao)

        def clienteServidor(self, req):
            import socket
            serverAddress = "localhost"
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
                clientSocket.connect((serverAddress, 81))
                clientSocket.send(req.encode())
                resposta = clientSocket.recv(12000).decode()
                if len(resposta)==328:
                    respostaFormatada = "Código:{}\nMensagem do servidor: {}".format(resposta[199], resposta[200:327])
                    return(respostaFormatada)
                if len(resposta)>328:
                    respostaFormatada = "Código:{} -> {}\nConteudo: {}".format(resposta[199], resposta[200:327], resposta[328:len(resposta)])
                    return(respostaFormatada)
    ptat = PTATCliente()
    requisicao = str(ptat.criaRequisicao(cmd))
    ptat.clienteServidor(requisicao)