from Sistema import Sistema
from User import user
import os

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

# criação do sistema que será utilizado pelo usuário
sistema = Sistema("01")

# criação do usuário do sistema
userKalleo = user("Kalleo", "kalleo@gmail.com", "12345678900")

# geração de certificado por meio do sistema
sistema.gerarCertificado(userKalleo)

# geração do documento exemplo que será assinado
documento = open(os.path.join(caminho_pastaKalleo, 'doc123.txt'), "w")
documento.write("escrevendo no documento que vai ser assinado...")
documento.close()

# assinatura do documento
# parâmetros respectivamente: usuário que irá assinar seu documento,
# certificado que deseja utilizar, documento que será assinado
sistema.assinarDocumento(userKalleo, "12345678900_1.txt", "doc123.txt")

# verificação da validade da assinatura
# parâmetros respectivamente: usuário que teoricamente assinou o documento,
# documento assinado.

#sistema.verificarAssinatura(userKalleo, "doc123Assinado.zip")