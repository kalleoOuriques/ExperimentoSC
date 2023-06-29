import os
from User import usuario
from AC import autoridadeCentral

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
usuario1 = usuario("Kalleo", "kalleo@gmail.com", "12345678900")

print(usuario1.certificado())

ac.gerarCertificado(usuario1)

print(usuario1.certificado())