from abc import ABC, abstractmethod
import textwrap



def menu():
    menu = """

[1] - deposito
[2] - saque
[3] - extrato
[4] - novo usuario
[5] - criar conta
[6] - listar contas
[0] - sair

--> """
    return int(input(menu))

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_usuario(cpf, clientes)
    
    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_clientes(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF fo cliente: ")
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_clientes(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF fo cliente: ")
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return

    conta = recuperar_conta_clientes(cliente)
    if not conta:
        return
    
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"{transacao["tipo"]}: R${transacao["valor"]:.2f}"
    
    print(extrato)
    print(f"Saldo: R${conta.saldo:.2f}")

def criar_usuario(clientes):
    cpf = input("Informe o CPF fo cliente: ")
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    nome = str(input("Digite seu nome: "))
    data_nascimento = input("Digite sua data de nascimento: ")
    endereco = str(input("Digite seu endereço: "))

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("Cliente criado com sucesso!")

def filtrar_usuario(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0]if clientes_filtrados else None

def recuperar_conta_clientes(cliente):
    if not cliente.contas:
        print("Cliente não possui conta!")
        return
    return cliente.conta[0]

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF fo cliente: ")
    cliente = filtrar_usuario(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

def listar_contas(contas):
    for conta in contas:
        print("#" * 100)
        print(textwrap.dedent(str(conta)))
       



class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
        super().__init__(endereco)       

class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0
        self._agencia = "0001"
        self._numero = numero
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo
    @property
    def agencia(self):
        return self._agencia
    @property
    def numero(self):
        return self._numero
    @property
    def cliente(self):
        return self._cliente
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo =self.saldo
        if valor > saldo:
            print("Saldo insufuciente")
        #elif valor > limite:
            #print("Saque excede o limite")
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso")
            #extrato += f"Saque: R% {saque}\n"
            #numero_saque += 1
            return True
        else:
            print("Valor invalido!")
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("Deposito realizado com sucesso")
            #extrato += f"Deposito: R$ {deposito:.2f}\n"
        else:
            print("Valor invalido!")
            return False
        return True
    
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite = 500, limite_saques = 3):
        self._limite = limite
        self._limite_saques = limite_saques
        super().__init__(cliente, numero)

    def sacar(self, valor):
        numero_saque = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])
        if numero_saque >= self.limite_saques:
            print("Não é possivel realizar mais saques hoje")
        elif self.limite > valor:
            print("Saque excede o limite")
        else:
            return super().sacar(valor)
            
        return False
    
    def __str__(self):
        return f"""
Agenica: {self.agencia}
N/C: {self.numero}
Titular: {self.cliente.nome}
"""

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor
            }
        )

class Transacoes(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacoes):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def regitrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adiocinar_transacao(self)      

class Deposito(Transacoes):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def regitrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adiocinar_transacao(self)

def main():
    clientes = []
    contas = []
    

    while True:

        opcao = menu()

        if opcao == 1:
            print("====DEPOSITO====")
            depositar(clientes)
        elif opcao == 2:
            print("====SAQUE====")
            sacar(clientes)
        elif opcao == 3:
            print("====EXTRATO====")
            exibir_extrato(clientes)
        elif opcao == 4:
            print("====NOVO-USUARIO====")
            criar_usuario(clientes)
        elif opcao == 5:
            print("====NOVA-CONTA====")
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif opcao == 6:
            print("====LISTA-CONTAS====")
            listar_contas(contas)
        elif opcao == 0:
            break
        else:
            print("opção invalida, escolha novamente")

main()

