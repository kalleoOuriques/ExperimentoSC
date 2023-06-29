import datetime
import os
from CD import certificadoDigital
from User import usuario
from Crypto.PublicKey import RSA


class autoridadeCentral:

    def __init__(self):
        self.assinatura = 'assinatura'
        self.serieControle = 0

    def gerarCertificado(self, user : usuario):
        # validade de 1 ano
        dataAtual = datetime.datetime.now()
        validade = dataAtual + datetime.timedelta(days=365)

        # geração das chaves RSA
        chavePublica, chavePrivada = self.RSA()
        user.chave_publica = chavePublica
        user.priv = chavePrivada

        # controle do numero de serie do certificado
        self.serieControle += 1

        # criação do certificado
        certificado = certificadoDigital(user.nome, user.email, user.cpf_cnpj, validade, 
                                         chavePublica, self.assinatura, self.serieControle)
        self.registrarNoHD(certificado, chavePrivada)

    # Depois de criar o certificado é hora de registrar o certificado e a chave privada no hd
    def registrarNoHD(self, certificado, chavePrivada):

        dirAtual = os.path.dirname(os.path.abspath(__file__))
        pathPasta = os.path.join(dirAtual, 'HD')

        nomeDaPastaDoUser = f'{certificado.nome}'
        caminhoDoCertificado = os.path.join(pathPasta, nomeDaPastaDoUser)

        # Caso o caminho não exista, ou seja, é a primeira vez
        # que ele cria um certificado. Então, ele cria a pasta
        if not(os.path.exists(caminhoDoCertificado)):
            os.makedirs(caminhoDoCertificado)

        fileCertificado = os.path.join(caminhoDoCertificado, f'{certificado.cpf_cnpj}_{certificado.numeroDeSerie}.txt')
        fileCPrivada = os.path.join(caminhoDoCertificado, f'{certificado.numeroDeSerie}_PK.pem')

        arquivo = open(fileCertificado, "w")
        with open(fileCertificado, "w") as arquivo:

            arquivo.write(f'Nome do titular: {certificado.nome}\n')
            arquivo.write(f'Email: {certificado.email}\n')
            arquivo.write(f'CPF ou CNPJ: {certificado.cpf_cnpj}\n')
            arquivo.write(f'Valido até: {certificado.validade}\n')
            arquivo.write(f'Chave pública: {certificado.chavePublica}\n')
            arquivo.write(f'Número de Série: {certificado.numeroDeSerie}\n')
            arquivo.write(f'Assinatura AC: {certificado.assinaturaAC}\n')

        with open(fileCPrivada, "wb") as arquivo:
            arquivo.write(chavePrivada)


    def RSA(self):
        """
        usa o módulo RSA da lib pycryptodome para gerar um par de chave
        """
        #password = "senha"
        chave = RSA.generate(1024)

        return (chave.public_key().export_key(), chave.export_key())