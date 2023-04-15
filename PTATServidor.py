class PTATServidor:
    def ligaServidor(self, sock, port:int):
        serverSocket = sock
        serverSocket.bind(("127.0.0.1", port))
        serverSocket.listen(10)
        print("Servidor Aberto")

    def loop(self, serverSocket):
        while (True):
            connectionSocket, addr = serverSocket.accept()
            comando = str(connectionSocket.recv(10000000).decode())
            codigo = comando[0]
            lenghtA = ""
            filenameA = ""
            pathA = ""
            body = ""
            for i in range (1, 7):
                lenghtA += comando[i]
            lenght = lenghtA.replace("?","")
            if lenght == "":
                lenght = 0
            else:
                lenght = int(lenght)
                
            for i in range(7, 71):
                filenameA += comando[i]
            filename = filenameA.replace("?","")
            for i in range(71, 199):
                pathA += comando[i]
            path = pathA.replace("?","")
            if lenght > 48000:
                code = "3"
                message = "tamanho do arquivo para ser escrito maior que tamanho máximo permitido, nenhum arquivo foi lido"
                while len(message)<128:
                    message += "?"
                men_prep = codigo + lenghtA + filenameA + pathA + code + message + body
                connectionSocket.send(str(men_prep).encode())
                cod = men_prep[199]
                log = PTATServidor.log(self, codigo, path, cod)
                yield log
                continue
            for i in range(199 , (199+lenght)):
                body += comando[i]

            if not comando:
                break
            elif str(codigo) == "0":
                documento = str(PTATServidor.leArquivo(self, filename, path, filenameA, pathA, codigo))
                connectionSocket.send(str(documento).encode())
                cod = documento[199]
                log = PTATServidor.log(self, codigo, path, cod)
                yield log
            elif str(codigo) == "1":
                documento = str(PTATServidor.criaArquivo(self, filename, path, body, filenameA, lenghtA, pathA, codigo))
                connectionSocket.send(str(documento).encode())
                print(documento+"\n"+str(len(documento)))
                cod = documento[199]
                log = PTATServidor.log(self, codigo, path, cod)
                yield log
            elif str(codigo) == "2":
                documento = str(PTATServidor.deletar(self, filename, path, filenameA, lenghtA, pathA, codigo))
                connectionSocket.send(str(documento).encode())
                cod = documento[199]
                log = PTATServidor.log(self, codigo, path, cod)
                yield log
            elif str(codigo) == "3":
                documento = str(PTATServidor.listar(self, path, lenghtA, filenameA, pathA, codigo))
                connectionSocket.send(str(documento).encode())
                cod = documento[199]
                log = PTATServidor.log(self, codigo, path, cod)
                yield log
            elif str(codigo) == "?":
                documento = str(PTATServidor.erro(self, filenameA, lenghtA, pathA, codigo))
                connectionSocket.send(str(documento).encode())
                cod = documento[199]
                log = PTATServidor.log(self, codigo, path, cod)
                yield log

     
        print("Conexao encerrada")
        connectionSocket.close()
    
    def log(self, ope, path ,code):
        brasil_tz = datetime.timezone(datetime.timedelta(hours=-3)) # UTC-3 is the time zone for Brazil
        current_time = datetime.datetime.now(brasil_tz)
        formatted_time = current_time.strftime('%H:%M:%S')
        log_prep = str(formatted_time) + ", "+ ope + ", " + path +  ", " + code
        return log_prep
                
    
    def criaArquivo(self, filename, path, body, filenameA, lenghtA, pathA, codigo):
        
        try:
            if (len(body) <= 1000000):
                arq = path + "/" + filename
                file1 = open(arq, "w")
                file1.write(body)
                code = "0"
                message = "arquivo escrito com sucesso"
                while len(message)<128:
                    message += "?"
                men_prep:str = codigo + lenghtA + filenameA + pathA + code + message + body
                return str(men_prep)
            else:
                code = "4"
                message = "tamanho do arquivo para ser escrito maior que tamanho máximo permitido, nenhum arquivo foi escrito"
                while len(message)<128:
                    message += "?"
                men_prep:str = codigo + lenghtA + filenameA + pathA + code + message + ""
                return str(men_prep)
        except: 
            if os.path.exists(path) == 0 or pathA =="?"*128:
                code = "1"
                message = "caminho não existente no servidor, nenhum arquivo foi escrito"
                while len(message)<128:
                    message += "?"
                men_prep:str = codigo + lenghtA + filenameA + pathA + code + message + body
                return str(men_prep)
            elif os.path.exists(path+"/"+filename) == 0 or filenameA == "?"*64:
                code = "2"
                message = "nome do arquivo não existente no servidor, nenhum arquivo foi escrito"
                while len(message)<128:
                    message += "?"
                men_prep:str = codigo + lenghtA + filenameA + pathA + code + message + body
                return str(men_prep)
        
    def leArquivo(self, filename, path,filenameA,pathA,codigo):
        arq = path + "/" + filename
        try: 
            file1 = open(arq, "r")
            documento = str(file1.readlines())
            tamanho = str(len(documento))
            code = "0"
            message = "arquivo lido com sucesso"
            while len(message)<128:
                message += "?"
            while len(tamanho)<6:
                tamanho += "?"
            men_prep:str = codigo + tamanho + filenameA + pathA + code + message + documento
            return str(men_prep)
        except: 
            if os.path.exists(path) == 0:
                tamanho = "?"
                code = "1"
                message = "caminho não existente no servidor, nenhum arquivo foi lido"
                while len(message)<128:
                    message += "?"
                while len(tamanho)<6:
                    tamanho += "?"
                men_prep:str = codigo + tamanho + filenameA + pathA + code + message
                return str(men_prep)
            elif os.path.exists(path+"/"+filename) == 0 or filename=="?"*64:
                tamanho = "?"
                code = "2"
                message = "nome do arquivo não existente no servidor, nenhum arquivo foi lido"
                while len(message)<128:
                    message += "?"
                while len(tamanho)<6:
                    tamanho += "?"
                men_prep:str = codigo + tamanho + filenameA + pathA + code + message
                return str(men_prep)
    def deletar(self, filename, path, filenameA, lenghtA, pathA, codigo):
        try:
            os.remove(path+"/"+filename)
            code = "0"
            message = "arquivo apagado com sucesso"
            while len(message)<128:
                message += "?"
            men_prep:str = codigo + lenghtA + filenameA + pathA + code + message
            return str(men_prep)
        except:
            if os.path.exists(path)==0:
                code = "1"
                message = "caminho não existente no servidor, nenhum arquivo foi deletado"
                while len(message)<128:
                    message += "?"
                men_prep:str = codigo + lenghtA + filenameA + pathA + code + message
                return str(men_prep)
            elif os.path.exists(path+"/"+filename)==0 or filename=="?"*64:
                code = "2"
                message = "nome de arquivo não existente no servidor, nenhum arquivo foi deletado"
                while len(message)<128:
                    message += "?"
                men_prep:str = codigo + lenghtA + filenameA + pathA + code + message
                return str(men_prep)

    def listar(self, path, lenghtA, filenameA, pathA, codigo):   
        caminhoPasta = path
        try:
            documento = str(os.listdir(str(caminhoPasta)))
            code = "0"
            message = "arquivos listados com sucesso"
            tamanho = str(len(documento))
            while len(message)<128:
                message += "?"
            while len(tamanho)<6:
                tamanho += "?"
            men_prep:str = codigo + tamanho + filenameA + pathA + code + message + documento
            return str(men_prep)
        except:
            if os.path.exists(str(caminhoPasta))==0:
                code = "1"
                message = "caminho não existente no servidor"
                while len(message)<128:
                    message += "?"
                men_prep:str = codigo + lenghtA + filenameA + pathA + code + message
                return str(men_prep)
        
    def erro(self, filenameA, lenghtA, pathA, codigo):
        code = "4"
        message = "operação inválida"
        while len(message)<128:
            message += "?"
        men_prep:str = codigo + lenghtA + filenameA + pathA + code + message
        return str(men_prep)


if __name__ == '__main__':
    import socket
    import os
    import datetime
    socketInstance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PTATServidor().ligaServidor(socketInstance, 12000)
    for x in PTATServidor().loop(socketInstance):
        print (x)