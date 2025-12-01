from models import especialidades_disponiveis, planos_de_saude
from datetime import datetime, date
import re

#------------------FUNÇÕES AUXILIARES e VALIDAÇÕES-------------------------------

def alterar_informacoes(campo):
    while True:
        resposta = input(f"Deseja alterar {campo}? (1. Sim / 0. Não): ").strip()
        if resposta.isdigit() and resposta in ["1", "0"]:
            return resposta == "1"
        else:
            print("Opção inválida. Digite 1 para Sim ou 0 para Não.")

def ler_opcao_valida(mensagem, opcoes_validas):
    while True:
        entrada = input(mensagem).strip()
        if entrada.isdigit() and entrada in [str(opcao) for opcao in opcoes_validas]:
            return entrada
        else:
            print(f"Digite uma opção válida: {', '.join(str(op) for op in opcoes_validas)}")

def buscar_datas_horas_iguais(consultas,crm,cpf,data_hora): 
    for consulta in consultas:
        if((consulta.medico.crm == crm or consulta.paciente.cpf == cpf)
            and consulta.data_hora == data_hora):
            return True
    return False
    

def cadastrar_horarios_disponiveis():
    horarios = []
    print("\nCadastre os horários disponíveis para o médico:")

    while True:
        try:
            data = input("Data disponível (dd/mm/aaaa): ").strip()
            hora = input("Hora disponível (HH:MM): ").strip()
            dt = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")

            if dt < datetime.now():
                print("Não é possível cadastrar horários passados.")
            elif dt in horarios:
                print("Este horário já foi adicionado.")
            else:
                horarios.append(dt)
                print("Horário adicionado com sucesso!")

        except ValueError:
            print("Formato inválido. Tente novamente.")

        continuar = input("Deseja adicionar outro horário? (s/n): ").strip().lower()
        if continuar != "s":
            break

    return horarios


def buscar_medico_especialidade(lista_medicos):
    especialidade = input("Digite a especialidade que deseja buscar: ").strip().upper()
    encontrados = []

    for medico in lista_medicos:
        if medico.especialidade.upper() == especialidade:
            encontrados.append(medico)

    if not encontrados:
        print("Nenhum médico encontrado com essa especialidade.")
        return

    print(f"== Médicos com especialidade em {especialidade.capitalize()} ==")
    for i, medico in enumerate(encontrados, start=1):
        print(f"{i}. Nome: {medico.nome} | CRM: {medico.crm}")


def buscar_paciente_cpf(lista_pacientes):
    cpf = ler_cpf("Digite o CPF do paciente que deseja buscar: ").strip()
    encontrado = False

    for paciente in lista_pacientes:
        if paciente.cpf == cpf:
            print("== Paciente Encontrado ==")
            print(f"CPF: {paciente.cpf}")
            print(f"Nome: {paciente.nome}")
            print(f"Nascimento: {paciente.nascimento}")
            print(f"Sexo: {paciente.sexo}")
            print(f"Plano: {paciente.plano}")
            
            encontrado = True
            break

    if not encontrado:
        print("Nenhum paciente encontrado com esse CPF.")


def listar_consulta_por_data(lista_consultas):
    data_str = input("Digite a data desejada (dd/mm/aaaa): ")

    try:
        data = datetime.strptime(data_str, "%d/%m/%Y").date()
    except ValueError:
        print("Data inválida. Use o formato dd/mm/aaaa.")
        return

    consultas_encontradas = [c for c in lista_consultas if c.data_hora.date() == data]

    if not consultas_encontradas:
        print("Nenhuma consulta encontrada para essa data.")
        return

    print(f"== Consultas agendadas para {data.strftime('%d/%m/%Y')} ==")
    for i, consulta in enumerate(consultas_encontradas, start=1):
        exibir_resumo_consulta(consulta)


def exibir_resumo_consulta(consulta):
    print("-" * 50)
    print("========Dados do paciente=======")
    print(f"CPF: {consulta.paciente.cpf} | Paciente: {consulta.paciente.nome}")
    print(f"Data e Hora: {consulta.data_hora.strftime('%d/%m/%Y %H:%M')}")
    print(f"Descrição: {consulta.descricao}")
    print("-" * 100)

def exibir_resumo_medico(medico):
    print(f"CRM: {medico.crm} | Nome: {medico.nome} | Especialidade: {medico.especialidade} | Sexo: {medico.sexo}")

def ler_data_nascimento(mensagem="Data de nascimento (dd/mm/aaaa): "):
    while True:
        data_str = input(mensagem)
        try:
            data =  datetime.strptime(data_str, "%d/%m/%Y").date()
            if data > date.today():
                print ("Data inválida. Use o formato dd/mm/aaaa.")
            else:
                return data
        except ValueError:
                print("Data inválida. Use o formato dd/mm/aaaa.")


def ler_data_nascimento_medico(mensagem="Data de nascimento (dd/mm/aaaa): "):
    while True:
        data_str = input(mensagem)
        try:
            nascimento = datetime.strptime(data_str, "%d/%m/%Y").date()
            hoje = date.today()
            idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))

            if idade < 24:
                print("Idade inválida. O médico deve ter no minímo 24 anos.")
            elif nascimento > hoje:
                print("Data de nascimento não pode ser no futuro.")
            else:
                return nascimento
        except ValueError:
            print("Data inválida. Use o formato dd/mm/aaaa.")


def data_hora_formatado(mensagem, formato):
    while True:
        entrada = input(mensagem).strip()
        try:
            return datetime.strptime(entrada, formato)
        except ValueError:
            print(f"Formato inválido! Use o formato {formato}.")


def escolher_especialidade():
    print("Escolha uma especialidade:")
    for esp in especialidades_disponiveis:
        print(esp)

    while True:
        codigo = input("Digite o número da especialidade: ").strip()
        for esp in especialidades_disponiveis:
            if esp.startswith(codigo + "."):
                return esp.split(". ")[1]  #retorna só o nome da especialidade
        print("Código inválido ou não existe no sistema. Tente novamente.")


def escolher_plano_de_saude():
    print("Escolha uma especialidade:")
    for esp in planos_de_saude:
        print(esp)

    while True:
        codigo = input("Digite o número da especialidade: ").strip()
        for esp in planos_de_saude:
            if esp.startswith(codigo + "."):
                return esp.split(". ")[1]  #retorna só o nome da especialidade
        print("Código inválido ou não existe no sistema. Tente novamente.")


def ler_sexo(mensagem="Sexo: (M/F): "):
    while True:
        sexo = input(mensagem).strip().upper()
        if sexo in ["M", "F"]:
            return sexo
        print("Sexo inválido. Digite 'M' ou 'F'.")


def ler_email(mensagem="Email: "):
    padrao_email = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    while True:
        email = input(mensagem).strip().lower()
        if re.match(padrao_email, email):
            return email
        print("Email inválido.Verifique o formato e tente novamente.")


def ler_telefone(mensagem="Telefone: "):
    while True:
        telefone = input(mensagem).strip()
        if telefone.isdigit() and len(telefone) in [10, 11]:
            return telefone
        print("Telefone inválido. Deve conter 10 ou 11 digítos números.")


def ler_nome(mensagem="Nome: "):
    while True:
        nome = input(mensagem).strip().lower()
        if nome:
            return nome
        print("Nome não pode estar vazio.")


def ler_cpf(mensagem="CPF: "):
    while True:
        cpf = input(mensagem).strip()
        if cpf.isdigit() and len(cpf) == 11:
            return cpf
        print("CPF inválido. Deve conter 11 dígitos numéricos.")


def ler_crm(mensagem="CRM: "):
    while True:
        crm = input(mensagem).strip().upper()
        if crm.isdigit() and 4 <= len(crm) <= 6:
            return crm
        print("CRM inválido. Deve conter ao menos 4 dígitos numéricos.")