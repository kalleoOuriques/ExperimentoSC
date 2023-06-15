import datetime
import os
from CD import certificadoDigital
from User import usuario



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
            os.mkdir(caminhoDoCertificado)

        fileCertificado = os.path.join(caminhoDoCertificado, f'{certificado.cpf_cnpj}_{certificado.numeroDeSerie}.txt')
        fileCPrivada = os.path.join(caminhoDoCertificado, f'{certificado.numeroDeSerie}_PK.txt')

        arquivo = open(fileCertificado, "w")

        arquivo.write(f'Nome do titular: {certificado.nome}\n')
        arquivo.write(f'Email: {certificado.email}\n')
        arquivo.write(f'CPF ou CNPJ: {certificado.cpf_cnpj}\n')
        arquivo.write(f'Valido até: {certificado.validade}\n')
        arquivo.write(f'Chave pública: {certificado.chavePublica}\n')
        arquivo.write(f'Número de Série: {certificado.numeroDeSerie}\n')
        arquivo.write(f'Assinatura AC: {certificado.assinaturaAC}\n')
        
        arquivo.close()

        arquivo = open(fileCPrivada, "w")

        arquivo.write(f'{chavePrivada}\n')
        
        arquivo.close()


    def RSA(self):
        return "cPU", "CPri"