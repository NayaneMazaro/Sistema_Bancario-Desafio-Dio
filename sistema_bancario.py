if __name__ == "__main__":
    
    saldo = 0
    limite = 500
    extrato = ""
    contador = 1

    menu = """
    [d] -> Depositar
    [s] -> Sacar
    [e] -> Extrato
    [q] -> Sair

    -> """

    while True:
        opcao = input(menu)
        match opcao:
            case "d":
                valor = float(input("Qual o valor do deposito?: "))
                if valor > 0:
                    saldo += valor 
                    extrato += f"Depósito: R$ {valor:.2f}\n"
                else:
                    print ("Operação falhou! Insira um valor válido.")

            case "s":
                if contador <= 3:
                    valor = int(input("Qual o valor do saque?: "))
                    if valor <= saldo and valor <= 500:
                        saldo -= valor
                        contador += 1
                        print("Saque realizado com sucesso!")
                    elif valor > 500:
                        print("Operação falhou! O valor do saque excede o limite.")
                    else:
                        print("Operação falhou! Saldo insuficiente.")
                else:
                    print("Operação falhou! Limite de saques atingido.")

            case "e":
                print("\n================ EXTRATO ================")
                print("Não foram realizadas movimentações." if not extrato else extrato)
                print(f"\nSaldo: R$ {saldo:.2f}")
                print("==========================================")

            case "q":
                break
