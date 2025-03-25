from datetime import datetime, date

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Transacao:
    def registrar(self, conta):
        raise NotImplementedError("Método registrar deve ser implementado.")

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(f"Depósito: R${self.valor:.2f}")
            print(f"Depósito de R${self.valor:.2f} realizado com sucesso!")
        else:
            print("Valor de depósito inválido.")

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > conta.saldo:
            print("Saldo insuficiente.")
        elif conta.saques_diarios >= conta.limite_saques:
            print("Limite de saques diários atingido.")
        else:
            conta.saldo -= self.valor
            conta.saques_diarios += 1
            conta.historico.adicionar_transacao(f"Saque: R${self.valor:.2f}")
            print(f"Saque de R${self.valor:.2f} realizado com sucesso!")

class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def sacar(self, valor):
        saque = Saque(valor)
        saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        deposito.registrar(self)

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia="0001", limite=1000, limite_saques=10):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques
        self.saques_diarios = 0

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# Exemplo de uso
def menu():
    clientes = []

    while True:
        print("1. Criar Cliente")
        print("2. Criar Conta Corrente")
        print("3. Depositar")
        print("4. Sacar")
        print("5. Mostrar Extrato")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome: ")
            cpf = input("CPF: ")
            data_nascimento = input("Data de nascimento (dd/mm/yyyy): ")
            endereco = input("Endereço: ")
            cliente = PessoaFisica(nome, cpf, datetime.strptime(data_nascimento, "%d/%m/%Y").date(), endereco)
            clientes.append(cliente)
            print(f"Cliente {nome} criado com sucesso!")
        elif opcao == '2':
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if cliente:
                numero = len(cliente.contas) + 1
                conta = ContaCorrente(cliente, numero)
                cliente.adicionar_conta(conta)
                print(f"Conta {numero} criada com sucesso para o cliente {cliente.nome}!")
            else:
                print("Cliente não encontrado.")
        elif opcao == '3':
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if cliente:
                numero = int(input("Número da conta: "))
                conta = next((conta for conta in cliente.contas if conta.numero == numero), None)
                if conta:
                    valor = float(input("Valor do depósito: "))
                    conta.depositar(valor)
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")
        elif opcao == '4':
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if cliente:
                numero = int(input("Número da conta: "))
                conta = next((conta for conta in cliente.contas if conta.numero == numero), None)
                if conta:
                    valor = float(input("Valor do saque: "))
                    conta.sacar(valor)
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")
        elif opcao == '5':
            cpf = input("CPF do cliente: ")
            cliente = next((c for c in clientes if c.cpf == cpf), None)
            if cliente:
                numero = int(input("Número da conta: "))
                conta = next((conta for conta in cliente.contas if conta.numero == numero), None)
                if conta:
                    print("\nExtrato:")
                    for transacao in conta.historico.transacoes:
                        print(transacao)
                    print(f"Saldo atual: R${conta.saldo:.2f}")
                else:
                    print("Conta não encontrada.")
            else:
                print("Cliente não encontrado.")
        elif opcao == '6':
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

menu()
