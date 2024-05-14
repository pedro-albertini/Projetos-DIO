menu = """

[1] - deposito
[2] - saque
[3] - extrato
[0] - sair

--> """

numero_saque = 0
limite = 500
LIMITE_SAQUE = 3
saldo = 0
deposito = 0
saque = 0

while True:

    opcao = int(input(menu))

    if opcao == 1:
        print("Deposito")
        deposito = float(input("Quanto vc deseja depositar?"))
        if deposito > 0:
            saldo += deposito
        else:
            print("Valor invalido!")
    elif opcao == 2:
        print("Saque")     
        if numero_saque >= LIMITE_SAQUE:
            print("Não é possivel realizar mais saques hoje")
        else:
            saque = float(input("Quando vc deseja sacar?"))
            if saque > 0:
                if saque > limite:
                    print("Não é possivel sacar esse valor")
                elif saque > saldo:
                    print("Não é possivel sacar esse valor")
                else: 
                    saldo -= saque
                    numero_saque += 1
            else:
                print("Valor invalido!")
    elif opcao == 3:
        print("Extrato")
        print(f"""
Deposito: {deposito}
Saque: {saque}


Saldo: {saldo}
""")
    elif opcao == 0:
        break
    else:
        print("opção invalida, escolha novamente")