class Conta:
    def __init__(self, titular, numero):
        self ._saldo = 0.0
        self ._numero = numero
        self ._titular = titular

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, saldo):
        if(saldo<0):
            print('saldo não pode ser negativo')
        else:
            self._saldo = saldo

    def saque(self, valor):
        if (self.saldo>=valor):
            self.saldo-=valor
            print('Saque Realizado com Sucesso')
        else:
            print('Saldo Insuficiente')

    def depositar(self, valor):
        self.saldo+=valor

    def extrato(self):
        print('Cliente: ', self._titular, 'Saldo Atual: ', self._saldo)