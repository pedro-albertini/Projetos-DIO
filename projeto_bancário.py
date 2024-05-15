def main():
    LIMITE_SAQUE = 3
    AGENCIA = "0001"

    saldo = 0
    numero_saque = 0
    numero_conta = 1
    limite = 500
    extrato = ""
    
    usuario = []
    conta = []

    while True:

        opcao = menu()

        if opcao == 1:
            print("====DEPOSITO====")
            deposito = float(input("Quanto vc deseja depositar? "))
            saldo, extrato = depositar(deposito, saldo, extrato)
        elif opcao == 2:
            print("====SAQUE====")
            if numero_saque >= LIMITE_SAQUE:
                print("Não é possivel realizar mais saques hoje")
            else:     
                saque = float(input("Quando vc deseja sacar? "))
                saldo, extrato, numero_saque = sacar(saldo=saldo, limite=limite, numero_saque=numero_saque, saque=saque, extrato=extrato)
        elif opcao == 3:
            print("====EXTRATO====")
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == 4:
            print("====NOVO-USUARIO====")
            criar_usuario(usuario)
        elif opcao == 5:
            print("====NOVA-CONTA====")
            criar_conta(usuario=usuario, conta=conta,agencia=AGENCIA, numero_conta=numero_conta)
            numero_conta += 1
        elif opcao == 6:
            print("====LISTA-CONTAS====")
            listar_contas(conta=conta)
        elif opcao == 0:
            break
        else:
            print("opção invalida, escolha novamente")

   

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

def depositar(deposito, saldo, extrato ,/):
    if deposito > 0:
        saldo += deposito
        extrato += f"Deposito: R$ {deposito:.2f}\n"
    else:
        print("Valor invalido!")
    return saldo, extrato

def sacar(*,saque, saldo, limite, numero_saque, extrato):
    if saque > saldo:
        print("Saldo insufuciente")
    elif saque > limite:
        print("Saque excede o limite")
    elif saque > 0:
        saldo -= saque
        extrato += f"Saque: R% {saque}\n"
        numero_saque += 1
    else:
        print("Valor invalido!")
    return saldo, extrato, numero_saque

def exibir_extrato(saldo ,/, *, extrato):
    print(extrato)
    print(f"\n\nSaldo: R$ {saldo}")

def criar_usuario(usuario):
    cpf = int(input("Digite seu CPF: "))
    filtro = filtrar_usuario(cpf,usuario)
    if filtro:
        print("Esse cpf já foi cadastrado")
        return
    nome = str(input("Digite seu nome: "))
    data_nascimento = input("Digite sua data de nascimento: ")
    endereco = str(input("Digite seu endereço: "))

    usuario.append({"nome": nome, "cpf": cpf,"data de nascimento": data_nascimento, "endereço": endereco})
    print("Usuario criado com sucesso!")

def filtrar_usuario(cpf, usuario):
    for i in usuario:
        if i["cpf"] == cpf:
            return 1
        else:
            return None

def criar_conta(usuario, conta, agencia, numero_conta):
    aux = int(input("Digite seu CPF: "))
    for i in usuario:
        if i["cpf"] == aux:
            conta.append({"usuario":i['nome'], "agencia":agencia, "numero da conta":numero_conta})
            print("Conta cadastrada com sucesso!")
        else:
            return print("Não existe usuario para cadastrar a conta")

def listar_contas(conta):
    for contas in conta:
        print(f"""
Agencia: {contas['agencia']}
N/C: {contas['numero da conta']}
Titular: {contas['usuario']}

""")
        
main()