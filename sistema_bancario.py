from datetime import datetime

if __name__ == "__main__":

    def menu():
        menu = """
        [d] -> Depositar
        [s] -> Sacar
        [e] -> Extrato
        [q] -> Sair

        -> """
        return input(menu)

    def depositar(saldo, valor, extrato, num_transacoes):
        if num_transacoes < 10:
            valor = float(input("Qual o valor do depósito?: "))
            if valor > 0:
                data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                saldo += valor 
                extrato += f"{data_hora}\tDepósito:\tR$ {valor:.2f}\n"
                num_transacoes += 1
                print("Depósito realizado com sucesso!")
            else:
                print ("Operação falhou! Insira um valor válido.")
        else:
            print("Operação falhou! Limite de transações diárias atingido.")
        
        return saldo, extrato, num_transacoes

    def sacar(saldo, valor, extrato, num_transacoes):
        if num_transacoes < 10:
            valor = int(input("Qual o valor do saque?: "))
            if valor > 0:
                if valor <= saldo and valor <= 500:
                    data_hora = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    saldo -= valor
                    extrato += f"{data_hora}\tSaque:\t\tR$ {valor:.2f}\n"
                    num_transacoes += 1
                    print("Saque realizado com sucesso!")
                elif valor > 500:
                    print("Operação falhou! O valor do saque excede o limite.")
                else:
                    print("Operação falhou! Saldo insuficiente.")
            else:
                print ("Operação falhou! Insira um valor válido.")
        else:
            print("Operação falhou! Limite de transações diárias atingido.")

        return saldo, extrato, num_transacoes
    
    def exibir_extrato(saldo, extrato):
        print("\n==================== EXTRATO ====================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\n\t\t\tSaldo:\t\tR$ {saldo:.2f}")
        print("==================================================")

    def main():
        saldo = 0
        extrato = ""
        num_transacoes = 0

        while True:
            opcao = menu()
            valor = None
            match opcao:
                case "d":
                    saldo, extrato, num_transacoes = depositar(saldo, valor, extrato, num_transacoes)

                case "s":
                    saldo, extrato, num_transacoes = sacar(saldo, valor, extrato, num_transacoes)

                case "e":
                    exibir_extrato(saldo, extrato)

                case "q":
                    break
                
main()