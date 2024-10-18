from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

if __name__ == "__main__":

    class Cliente:
        def __init__(self, endereco):
            self.endereco = endereco
            self.contas = []

        def realizar_transacao(self, conta, transacao):
            transacao.registrar(conta)

        def adicionar_conta(self, conta):
            self.contas.append(conta)

    class PessoaFisica(Cliente):
        def __init__(self, cpf, nome, data_nascimento, endereco):
            super().__init__(endereco)
            self.cpf = cpf
            self.nome = nome
            self.data_nascimento = data_nascimento


    class Conta:
        def __init__(self, numero, cliente):
            self._saldo = 0
            self._numero = numero
            self._agencia = "0001"
            self._cliente = cliente
            self._historico = Historico()

        @classmethod
        def nova_conta(cls, cliente, numero):
            return cls(numero, cliente)

        @property
        def saldo(self):
            return self._saldo

        @property
        def numero(self):
            return self._numero

        @property
        def agencia(self):
            return self._agencia

        @property
        def cliente(self):
            return self._cliente

        @property
        def historico(self):
            return self._historico
        
        def sacar(self, valor):
            if valor > 0 and valor <= self._saldo:
                self._saldo -= valor
                print("Saque realizado com sucesso!")
                return True
            else:
                print("Operação falhou! Saldo insuficiente ou valor inválido.")
                return False

        
        def depositar(self, valor):
            if valor > 0:
                self._saldo += valor
                print("Depósito realizado com sucesso!")
                return True
            else:
                print("Operação falhou! Insira um valor válido.")
                return False
        
    class ContaCorrente(Conta):
        def __init__(self, numero, cliente, limite=500, limite_saques=3):
            super().__init__(numero, cliente)
            self._limite = limite
            self._limite_saques = limite_saques

        def sacar(self, valor):
            numero_saques = len(
                [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
            )

            excedeu_limite = valor > self._limite
            excedeu_saques = numero_saques >= self._limite_saques

            if excedeu_limite:
                print("\nOperação falhou! O valor do saque excede o limite.")

            elif excedeu_saques:
                print("Operação falhou! Limite de saques atingido.")

            else:
                return super().sacar(valor)

            return False

        def __str__(self):
            return f"""\
                Agência:\t{self.agencia}
                C/C:\t\t{self.numero}
                Titular:\t{self.cliente.nome}
            """

    class Historico:
        def __init__(self):
            self._transacoes = []

        @property
        def transacoes(self):
            return self._transacoes

        def adicionar_transacao(self, tipo, valor):
            self._transacoes.append({
                "tipo": tipo,
                "valor": valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            })

    class Transacao(ABC):
        @abstractmethod
        def registrar(self, conta):
            pass

    class Saque(Transacao):
        def __init__(self, valor):
            self._valor = valor

        def registrar(self, conta):
            if conta.sacar(self._valor):
                conta.historico.adicionar_transacao("Saque:\t", self._valor)

    class Deposito(Transacao):
        def __init__(self, valor):
            self._valor = valor

        def registrar(self, conta):
            if conta.depositar(self._valor):
                conta.historico.adicionar_transacao("Depósito:", self._valor)

    def menu():
        menu = """\n
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
        return input(textwrap.dedent(menu))


    def filtrar_cliente(cpf, clientes):
        clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
        return clientes_filtrados[0] if clientes_filtrados else None


    def recuperar_conta_cliente(cliente):
        if not cliente.contas:
            print("\nCliente não possui conta!")
            return

        # FIXME: não permite cliente escolher a conta
        return cliente.contas[0]


    def depositar(clientes):
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\nCliente não encontrado!")
            return

        valor = float(input("Informe o valor do depósito: "))
        transacao = Deposito(valor)

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)


    def sacar(clientes):
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\nCliente não encontrado!")
            return

        valor = float(input("Informe o valor do saque: "))
        transacao = Saque(valor)

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        cliente.realizar_transacao(conta, transacao)


    def exibir_extrato(clientes):
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\n@@@ Cliente não encontrado! @@@")
            return

        conta = recuperar_conta_cliente(cliente)
        if not conta:
            return

        print("\n==================== EXTRATO ====================")
        transacoes = conta.historico.transacoes

        if not transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in transacoes:
                print(f"{transacao['data']}\t{transacao['tipo']}\tR$ {transacao['valor']:.2f}")
        
        print(f"\n{'Saldo':<34}\tR$ {conta.saldo:.2f}")

        print("==================================================")


    def criar_cliente(clientes):
        cpf = input("Informe o CPF (somente número): ")
        cliente = filtrar_cliente(cpf, clientes)

        if cliente:
            print("\nJá existe cliente com esse CPF!")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)

        clientes.append(cliente)

        print("\nCliente criado com sucesso!")


    def criar_conta(numero_conta, clientes, contas):
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente(cpf, clientes)

        if not cliente:
            print("\nCliente não encontrado, fluxo de criação de conta encerrado!")
            return

        conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
        contas.append(conta)
        cliente.contas.append(conta)

        print("\nConta criada com sucesso!")


    def listar_contas(contas):
        for conta in contas:
            print("=" * 100)
            print(textwrap.dedent(str(conta)))


    def main():
        clientes = []
        contas = []

        while True:
            opcao = menu()

            if opcao == "d":
                depositar(clientes)

            elif opcao == "s":
                sacar(clientes)

            elif opcao == "e":
                exibir_extrato(clientes)

            elif opcao == "nu":
                criar_cliente(clientes)

            elif opcao == "nc":
                numero_conta = len(contas) + 1
                criar_conta(numero_conta, clientes, contas)

            elif opcao == "lc":
                listar_contas(contas)

            elif opcao == "q":
                break

            else:
                print("\nOperação inválida, por favor selecione novamente a operação desejada.")

    main()