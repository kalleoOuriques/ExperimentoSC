import os
class usuario:
    def __init__(self, nome, email, cpf_cnpj):
        self.nome = nome
        self.email = email
        self.cpf_cnpj = cpf_cnpj
        self.chave_publica = None

    # Primeiro verifica a existencia de um certificado do usuario
    # Tentanto acessar a pasta do usuario no "HD"
    def certificado(self):
        dirAtual = os.path.dirname(os.path.abspath(__file__))
        pathPasta = os.path.join(dirAtual, 'HD')
        nomeDaPastaDoUser = f'{self.nome}'

        caminhoDoCertificado = os.path.join(pathPasta, nomeDaPastaDoUser)

        if os.path.exists(caminhoDoCertificado):
            return {'status': True, 'response': caminhoDoCertificado}

        else:
            return {'status': False, 'respose': 'Certificado inexistente!'}