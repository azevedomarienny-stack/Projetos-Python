class main:
    pass

from Cliente import Cliente
from Conta import Conta

print('Testando o projeto')

c1= Cliente('João', '21000000000')
conta=Conta(c1.get_nome(), 1222)

conta.depositar(100)
conta.saque(50)
conta.extrato()
