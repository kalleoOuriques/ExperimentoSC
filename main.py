import os
from User import usuario
from AC import autoridadeCentral
from Sistema import Sistema

usuario_atual = None

def gerar_certificado():
    nome = input("Qual seu nome?")
    email = input("Qual seu email? ")
    cpf = input("Qual seu CPF Ou CNPJ?")
    usuario_atual = usuario(nome, email, cpf)
    sistema.gerarCertificado(usuario_atual)
    return usuario_atual.certificado()

def assinar_documento():
    arquivo = input("digite o nome do documento")
    sistema.assinarDocumento(usuario_atual, "12345678900_1.txt", arquivo)

def verificar_assinatura():
    arquivo = input("Digite o nome do .zip")
    sistema.verificarAssinatura(usuario_atual, arquivo)

def deletar_arquivos_diretorio(caminho_diretorio):
    # Verificar se o caminho do diretório é válido
    if not os.path.isdir(caminho_diretorio):
        print(f"{caminho_diretorio} não é um diretório válido.")
        return
    
    # Deletar os arquivos dentro do diretório
    for nome_arquivo in os.listdir(caminho_diretorio):
        caminho_arquivo = os.path.join(caminho_diretorio, nome_arquivo)
        if os.path.isfile(caminho_arquivo):
            os.remove(caminho_arquivo)
            print(f"Arquivo {nome_arquivo} deletado com sucesso.")

    # Deletar o diretório vazio
    os.rmdir(caminho_diretorio)
    print(f"Diretório {caminho_diretorio} deletado com sucesso.")

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_pasta = os.path.join(diretorio_atual, 'HD')
caminho_pastaKalleo = os.path.join(caminho_pasta, 'Kalleo')
deletar_arquivos_diretorio(caminho_pastaKalleo)

ac = autoridadeCentral()

sistema = Sistema("1")

while True:
    print("Escolha sua opção")
    print("""[q] para sair
[c] para gerar um certificado
[a] para assinar um documento
[v] para verificar um documento""")

    opcao_escolhida = input("Qual sua opção? ")
    if opcao_escolhida == "q":
        break
    elif opcao_escolhida == "c":
        print(gerar_certificado())
        break
    elif opcao_escolhida == "a":
        assinar_documento()
        break
    elif opcao_escolhida == "v":
        verificar_assinatura()
        break

#usuario1 = usuario("Kalleo", "kalleo@gmail.com", "12345678900")

#print(usuario1.certificado())

#ac.gerarCertificado(usuario1)

#print(usuario1.certificado())