from Sistema import Sistema
from User import usuario

sistema = Sistema("01")
usuario1 = usuario("Kalleo", "kalleo@gmail.com", "12345678900")

sistema.assinarDocumento(usuario1, "12345678900_1.txt", "doc123.txt")

sistema.verificarAssinatura(usuario1, "doc123Assinado.zip")