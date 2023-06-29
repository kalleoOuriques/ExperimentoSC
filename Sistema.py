import os
from datetime import datetime
import hashlib
import shutil
import zipfile
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64
from AC import autoridadeCentral


class Sistema:

    def __init__(self, nome):
        self.nome = nome
        self.autoridade = autoridadeCentral()


    def acessarHD(self, user):
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_pasta = os.path.join(diretorio_atual, 'HD')
        caminho_pastaUser = os.path.join(caminho_pasta, user.nome)
        return caminho_pastaUser
        # verificar se 

    def verificarAssinatura(self, user_assinador, arquivo):

        # Verificar por indicação do usuário qual o documento que deve ser assinado
        # Receber a pasta compactada
        # Descriptografar o hash do documento com a chave pública do usuário

        # Transformar o documento txt em hash
        # comparar os dois hash

        caminho_user: str = self.acessarHD(user_assinador)
        caminho_arquivo = os.path.join(caminho_user, arquivo)  # caminho do zip

        with zipfile.ZipFile(caminho_arquivo) as arquivo_zipado:
            arquivo_zipado.extractall(f"{caminho_user}/doc123Assinado/")

        with open(f"{caminho_user}/doc123Assinado/doc123.txt") as doc:
            doc = doc.read()
            hash_a_verificar = hashlib.sha256(doc.encode('utf-8')).hexdigest()
            #hash_a_verificar = SHA256.new(doc)
            print("hash do doc: ", hash_a_verificar)

        with open(f"{caminho_user}/doc123Assinado/EncryptHash.txt", 'r') as signature:
            hash_criptografado = signature.read()
            decoded_hash = base64.b64decode(hash_criptografado)
            #decoded_hash = decoded_hash.decode('utf-8')

            #print("tamanho hash abrir: ", len(decoded_hash))
            #print("hash decoded: ", decoded_hash)
            

            chave = RSA.import_key(user_assinador.priv) # chave publica no objeto da lib (RsaKey)

            cipher = PKCS1_OAEP.new(chave)
            #cipher = pkcs1_15.new(chave)
            string = cipher.decrypt(decoded_hash).decode('utf-8')
            print("string: ", string)
            if string == hash_a_verificar:
                print("VERIFICAÇÃO COM SUCESSO")

    

    def gerarCertificado(self, user):
        # chama a ac passando o user como parâmetro 
        self.autoridade.gerarCertificado(user)
        pass

    def assinarDocumento(self, user, certificado, documento):
        
        # Validar o certificado enviado

        # pegar a validade e o cpf_cnpj do certificado enviado
        caminhoCertificado = os.path.join(self.acessarHD(user), certificado)
        arquivo = open(caminhoCertificado, "r")
        conteudo = arquivo.read()
        valData = conteudo[(conteudo.find("Valido até:")+12):conteudo.find("Valido até:")+38]
        cpfCnpj = conteudo[(conteudo.find("CPF ou CNPJ:")+13):conteudo.find("CPF ou CNPJ:")+24]
        
        # pegar o numero de serie para saber qual chave pegar
        numeroDeSerie = '0'
        for i in conteudo[(conteudo.find("Número de Série:")+17):]:

            if i.isdigit():
                numeroDeSerie += i
            else:
                break

        numeroDeSerie = numeroDeSerie[1:]
        arquivo.close()

        # verificar se o cpf ou cnpj bate com o usuário
        if user.cpf_cnpj != cpfCnpj:
            return {'status': False, 'descricao': 'O cpf/cnpj do certificado diferente do usuário!' }
        
        # verificar o tempo de validade do certificado
        valDataObj = datetime.strptime(valData, "%Y-%m-%d %H:%M:%S.%f").date()
        dataAtual = datetime.now().date()

        if valDataObj < dataAtual:
            return {'status': False, 'descricao': 'Este certificado já expirou!' }
            
        # transformar esta string em um hash

        self.gerarCertificado(user)
    
        caminhoDocumento = os.path.join(self.acessarHD(user), documento)
        arquivo = open(caminhoDocumento, 'r')
        documentoS = arquivo.read()
        arquivo.close()

        hash = hashlib.sha256(documentoS.encode('utf-8')).hexdigest()

        # Carregar a chave privada em formato PEM a partir do arquivo .txt

        # Subtrair do HD do usuário a chave privada
        # referente ao certificado enviado
        caminhoChavePrivada = os.path.join(self.acessarHD(user), f'{numeroDeSerie}_PK.pem' )

        # Carregar a chave privada
        with open(caminhoChavePrivada, 'rb') as arquivo_chave:
            chave_privada = RSA.import_key(arquivo_chave.read())

        # Criar instância do objeto PKCS1_OAEP
        cipher = PKCS1_OAEP.new(chave_privada)
        #cipher = pkcs1_15.new(chave_privada)

        # Converter o hash para bytes
        hash_bytes = hash.encode('utf-8')
        #hash_bytes = SHA256.new(hash_bytes)
        #print("hash de assinar taman", len(hash_bytes))

        # Criptografar o hash
        hash_criptografado = cipher.encrypt(hash_bytes)
        #hash_criptografado = cipher.sign(hash_bytes)
        print("taman hash cripto", len(hash_criptografado))
        print(hash_criptografado)
        print("\n")
        
        # criar uma pasta com o hash criptografado +
        # o documento original
        caminhoPasta = os.path.join(self.acessarHD(user), f'{documento[:documento.find(".")]}Assinado' )
        self.criar_pasta_zipar_arquivos(user, caminhoPasta, caminhoDocumento, hash_criptografado)

    def criar_pasta_zipar_arquivos(self, user, caminho_pasta, caminhoDocumento,  hash_criptografado):
        
        # Criar a pasta
        if not os.path.exists(caminho_pasta):
            os.mkdir(caminho_pasta)

        # Criar txt do hash criptografado na pasta criada
        caminhoArquivo = os.path.join(caminho_pasta, 'EncryptHash.txt' )
        hashBase64 = base64.b64encode(hash_criptografado)
        with open(caminhoArquivo, 'w') as arquivo:
            arquivo.write(hashBase64.decode('utf-8'))
        
        # Copiando o documento para a pasta
        shutil.copy(caminhoDocumento, caminho_pasta)

        # Obter o diretório atual
        diretorio_atual = self.acessarHD(user)
        try:

            # Obter o nome da pasta base
            nome_pasta_base = os.path.basename(caminho_pasta)
            # Zipar a pasta
            caminho_zip = os.path.join(diretorio_atual, f'{nome_pasta_base}.zip')
            with zipfile.ZipFile(caminho_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(caminho_pasta):
                    for file in files:
                        arquivo = os.path.join(root, file)
                        zipf.write(arquivo, os.path.relpath(arquivo, caminho_pasta))
            
            # Excluir a pasta não zipada
            shutil.rmtree(caminho_pasta)
            
            print(f"O arquivo zip '{caminho_zip}' foi gerado.")
            
        except Exception as e:
            print(f"Ocorreu um erro: {str(e)}")
