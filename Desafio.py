import re

class Banco:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Banco, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def depositar(self, conta, valor):
        if valor > 0:
            conta.saldo += valor
            conta.extrato.append(f"Depósito: R${valor:.2f}")
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
        else:
            print("Valor de depósito inválido. Tente novamente.")

    def sacar(self, conta, valor):
        if valor > conta.limite_saque:
            print(f"Valor de saque excede o limite de R${conta.limite_saque:.2f}.")
        elif conta.saques_diarios >= conta.limite_saques_diarios:
            print("Limite de saques diários atingido.")
        elif valor > conta.saldo:
            print("Saldo insuficiente.")
        else:
            conta.saldo -= valor
            conta.extrato.append(f"Saque: R${valor:.2f}")
            conta.saques_diarios += 1
            print(f"Saque de R${valor:.2f} realizado com sucesso!")

    def mostrar_extrato(self, conta):
        print("\nExtrato:")
        for operacao in conta.extrato:
            print(operacao)
        print(f"Saldo atual: R${conta.saldo:.2f}\n")

class ContaCorrente:
    contas_correntes = []

    def __init__(self, agencia, numero_conta, usuario, saldo=0):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.banco = Banco()
        self.saldo = 0
        self.extrato = []
        self.limite_saque = 1000
        self.saques_diarios = 0
        self.limite_saques_diarios = 10

    @staticmethod
    def criar_conta_corrente(usuario):
        agencia = "0001"
        numero_conta = len(ContaCorrente.contas_correntes) + 1
        conta = ContaCorrente(agencia, numero_conta, usuario)
        ContaCorrente.contas_correntes.append(conta)
        print(f"Conta corrente {numero_conta} criada com sucesso para o usuário {usuario.nome}!")

    @staticmethod
    def encontrar_conta_por_cpf(cpf):
        for conta in ContaCorrente.contas_correntes:
            if conta.usuario.cpf == cpf:
                return conta
        return None

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

    usuarios = []

    @staticmethod
    def criar_usuario(nome, data_nascimento, cpf, endereco):
        cpf = ''.join(filter(str.isdigit, cpf))

        # Check if CPF is already in use
        for usuario in Usuario.usuarios:
            if usuario.cpf == cpf:
                print(f"Erro: CPF {cpf} já está em uso.")
                return

        novo_usuario = Usuario(nome, data_nascimento, cpf, endereco)
        Usuario.usuarios.append(novo_usuario)
        print(f"Usuário {nome} criado com sucesso!")

    @staticmethod
    def vincular_usuario_conta(cpf):
        cpf = ''.join(filter(str.isdigit, cpf))

        for usuario in Usuario.usuarios:
            if usuario.cpf == cpf:
                ContaCorrente.criar_conta_corrente(usuario)
                return
        print(f"Erro: Usuário com CPF {cpf} não encontrado.")

def menu():
    while True:
        print("1. Depositar")
        print("2. Sacar")
        print("3. Mostrar Extrato")
        print("4. Novo Cliente")
        print("5. Nova Conta Corrente")
        print("6. Listar Contas Correntes")
        print("7. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cpf = input("Digite o CPF da conta: ")
            conta = ContaCorrente.encontrar_conta_por_cpf(cpf)
            if not conta:
                print(f"Erro: Conta com CPF {cpf} não encontrada.")
                continue
            valor = float(input("Digite o valor para depósito: "))
            conta.banco.depositar(conta, valor)
        elif opcao == '2':
            cpf = input("Digite o CPF da conta: ")
            conta = ContaCorrente.encontrar_conta_por_cpf(cpf)
            if not conta:
                print(f"Erro: Conta com CPF {cpf} não encontrada.")
                continue
            valor = float(input("Digite o valor para saque: "))
            conta.banco.sacar(conta, valor)
        elif opcao == '3':
            cpf = input("Digite o CPF da conta: ")
            conta = ContaCorrente.encontrar_conta_por_cpf(cpf)
            if not conta:
                print(f"Erro: Conta com CPF {cpf} não encontrada.")
                continue
            conta.banco.mostrar_extrato(conta)
        elif opcao == '4':
            nome = input("Digite o nome do cliente: ")
            data_nascimento = input("Digite a data de nascimento (dd/mm/yyyy): ")
            cpf = input("Digite o CPF: ")
            endereco = input("Digite o endereço: ")
            Usuario.criar_usuario(nome, data_nascimento, cpf, endereco)
        elif opcao == '5':
            cpf = input("Digite o CPF do cliente: ")
            Usuario.vincular_usuario_conta(cpf)
        elif opcao == '6':
            print("\nContas Correntes:")
            for conta in ContaCorrente.contas_correntes:
                print(f"Agência: {conta.agencia}, Conta: {conta.numero_conta}, Usuário: {conta.usuario.nome}")
            print()
        elif opcao == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

menu()
