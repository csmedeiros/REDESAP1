import os
from socket import*
import datetime

class PTATServidor:
    def ligaServidor(sock, port):
        serverPort = port
        serverSocket = sock
        serverSocket.bind(('', serverPort))
        serverSocket.listen(10)
        print("Servidor Aberto")

    def loop(serverSocket):
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
                message = "tamanho do arquivo para ser escrito maior que tamanho máximo permitido"
                while len(message)<128:
                    message += "?"
                men_prep = codigo + lenghtA + filenameA + pathA + code + message + body
                connectionSocket.send(str(men_prep).encode())
                cod = men_prep[199]
                log = PTATServidor.log(codigo, path, cod)
                yield log
                continue
            for i in range(199 , (199+lenght)):
                body += comando[i]

            if not comando:
                break
            elif str(codigo) == "0":
                documento = PTATServidor.leArquivo(filename, path, filenameA, pathA, codigo)
                connectionSocket.send(str(documento).encode())
                cod = documento[199]
                log = PTATServidor.log(codigo, path, cod)
                yield log
            elif str(codigo) == "1":
                documento = PTATServidor.criaArquivo(filename, path, body, filenameA, lenghtA, pathA, codigo)
                connectionSocket.send(str(documento).encode())
                cod = documento[199]
                log = PTATServidor.log(codigo, path, cod)
                yield log
            elif str(codigo) == "2":
                documento = PTATServidor.deletar(filename, path, filenameA, lenghtA, pathA, codigo)
                connectionSocket.send(str(documento).encode())
                cod = documento[199]
                log = PTATServidor.log(codigo, path, cod)
                yield log
            elif str(codigo) == "3":
                documento = PTATServidor.listar(path, lenghtA, filenameA, pathA, codigo)
                connectionSocket.send(str(documento).encode())
                cod = documento[199]
                log = PTATServidor.log(codigo, path, cod)
                yield log
            elif str(codigo) == "?":
                documento = PTATServidor.erro(filenameA, lenghtA, pathA, codigo)
                connectionSocket.send(str(documento).encode())
                cod = documento[199]
                log = PTATServidor.log(codigo, path, cod)
                yield log

     
        print("Conexao encerrada")
        connectionSocket.close()
    
    def log(ope, path ,code):
        brasil_tz = datetime.timezone(datetime.timedelta(hours=-3)) # UTC-3 is the time zone for Brazil
        current_time = datetime.datetime.now(brasil_tz)
        formatted_time = current_time.strftime('%H:%M:%S')
        log_prep = str(formatted_time) + ", "+ ope + ", " + path +  ", " + code
        return log_prep
                
    
    def criaArquivo(filename, path, body, filenameA, lenghtA, pathA, codigo):
        arq = path + "/" + filename
        file1 = open(arq, "w")
        try:
            if (len(body) <= 1000000):
                file1.write(body)
                code = "0"
                message = "arquivo escrito com sucesso"
                while len(message)<128:
                    message += "?"
                men_prep = codigo + lenghtA + filenameA + pathA + code + message + body
                return men_prep
        except: 
            if os.path.exists(path) == 0:
                code = "1"
                message = "caminho não existente no servidor"
                while len(message)<128:
                    message += "?"
                men_prep = codigo + lenghtA + filenameA + pathA + code + message + body
                return men_prep
            elif os.path.exists(filename) == 0:
                code = "2"
                message = "nome do arquivo não existente no servidor"
                while len(message)<128:
                    message += "?"
                men_prep = codigo + lenghtA + filenameA + pathA + code + message + body
                return men_prep
        
    def leArquivo(filename,path,filenameA,pathA,codigo):
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
            men_prep = codigo + tamanho + filenameA + pathA + code + message + documento
            return men_prep
        except: 
            if os.path.exists(path) == 0:
                tamanho = "?"
                code = "1"
                message = "caminho não existente no servidor"
                while len(message)<128:
                    message += "?"
                while len(tamanho)<6:
                    tamanho += "?"
                men_prep = codigo + tamanho + filenameA + pathA + code + message
                return men_prep
            elif os.path.exists(filename) == 0:
                tamanho = "?"
                code = "2"
                message = "nome do arquivo não existente no servidor"
                while len(message)<128:
                    message += "?"
                while len(tamanho)<6:
                    tamanho += "?"
                men_prep = codigo + tamanho + filenameA + pathA + code + message
                return men_prep
     
    def deletar(filename, path, filenameA, lenghtA, pathA, codigo):
        arq = path + "/" + filename
        try:
            os.remove(arq)
            code = "0"
            message = "arquivo apagado com sucesso"
            while len(message)<128:
                message += "?"
            men_prep = codigo + lenghtA + filenameA + pathA + code + message
            return men_prep
        except:
            if os.path.exists(path)==0:
                code = "1"
                message = "caminho não existente no servidor"
                while len(message)<128:
                    message += "?"
                men_prep = codigo + lenghtA + filenameA + pathA + code + message
                return men_prep
            elif os.path.exists(filename)==0:
                code = "2"
                message = "nome de arquivo não existente no servidor"
                while len(message)<128:
                    message += "?"
                men_prep = codigo + lenghtA + filenameA + pathA + code + message
                return men_prep

    def listar(path, lenghtA, filenameA, pathA, codigo):   
        caminhoPasta = path
        try:
            documento = str(os.listdir(caminhoPasta))
            code = "0"
            message = "arquivos listados com sucesso"
            tamanho = str(len(documento))
            while len(message)<128:
                message += "?"
            while len(tamanho)<6:
                tamanho += "?"
            men_prep = codigo + tamanho + filenameA + pathA + code + message + documento
            return men_prep
        except:
            if os.path.exists(caminhoPasta)==0:
                code = "1"
                message = "caminho não existente no servidor"
                while len(message)<128:
                    message += "?"
                men_prep = codigo + lenghtA + filenameA + pathA + code + message
                return men_prep
        
    def erro(filenameA, lenghtA, pathA, codigo):
        code = "4"
        message = "operação inválida"
        while len(message)<128:
            message += "?"
        men_prep = codigo + lenghtA + filenameA + pathA + code + message
        return men_prep


if __name__ == '__main__':
    serverSocket = socket(AF_INET, SOCK_STREAM)
    PTATServidor.ligaServidor(serverSocket, 12000)
    for x in PTATServidor.loop(serverSocket):
        print (x)