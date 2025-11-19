from models import Medico, Paciente, AgendaMedica, Consulta
from datetime import datetime, date
from funcoes_auxiliares import  ler_data_nascimento, ler_email, ler_nome, ler_sexo, ler_telefone, ler_cpf, ler_crm, data_hora_formatado
from funcoes_auxiliares import buscar_datas_horas_iguais, ler_data_nascimento_medico, escolher_especialidade, alterar_informacoes, escolher_plano_de_saude
from funcoes_auxiliares import exibir_resumo_consulta, exibir_resumo_medico, cadastrar_horarios_disponiveis, ler_opcao_valida 



#Funções Consulta: Inserir, Listar Todos, Listar um, Alterar, Excluir

def inserir_consulta(consultas, listar_medicos, listar_pacientes, agendas):
    print("==== Insira os dados da consulta: ====")
    print("======================================")
    print("===Insira o CRM ou Especialidade: ====")
    print("1. CRM: ")
    print("2. Especialidade: ")

    escolha = ler_opcao_valida("Escolha uma opção: ", [1,2])

    if escolha == '1':
        crm = ler_crm("Insira o CRM do médico: ").strip()
    elif escolha == '2':
        crm  = escolher_especialidade()




    verificar_indice_medico = buscar_medico(listar_medicos, crm)

    if verificar_indice_medico == -1:
        print("Médico não localizado")
        return
    
    medico = listar_medicos[verificar_indice_medico]
    exibir_resumo_medico(medico)
    
    cpf = ler_cpf ("Insira o CPF: ")
    verificar_indice_paciente = buscar_paciente(listar_pacientes, cpf)
    if verificar_indice_paciente == -1:
            print("Paciente não encontrado")
            return
    
    data = data_hora_formatado("Data da consulta (dd/mm/aaaa)", "%d/%m/%Y").date()
    hora = data_hora_formatado("Horário da consulta (HH:MM)", "%H:%M").time()
    data_hora = datetime.combine (data, hora)  
     
    agenda = agendas.get(crm)
    if not agenda:
        print("Agenda do médico não encontrada.")
        return
    
    if data_hora not in agenda.horarios_disponiveis:
        print("Horário indisponível para este médico.")
        return

    if data_hora < datetime.now():
        print("Data e hora inválidas. Não é possível agendar consultas para datas passadas.")
        return
    
    if buscar_datas_horas_iguais(consultas, crm, cpf, data_hora):
            print("Já existe uma consulta marcada nessa data ou hora")
            return
    
    descricao = input("Descrição da consulta: ").strip()
    nova_consulta = Consulta(
        medico =listar_medicos[verificar_indice_medico],
        paciente = listar_pacientes[verificar_indice_paciente],
        data_hora=data_hora,
        descricao= descricao
    )

    consultas.append(nova_consulta)
    agenda.horarios_disponiveis.remove(data_hora)
    print("\nConsulta agendada com sucesso!")
    exibir_resumo_consulta(nova_consulta)


def listar_consulta(consultas):
    if not consultas:
        print("Não há consultas agendadas.")
        return

    print("== Lista de Consultas Agendadas ==")
    for i, consultas in enumerate(consultas):
        exibir_resumo_medico(consultas)
        exibir_resumo_consulta(consultas)


def listar_uma_consulta(consultas):
    cpf = ler_cpf("Digite o CPF do(a) paciente: ")
    encontrou = False

    print(f"== Consulta(s) para o CPF {cpf} ==")
    
    for consultas in listar_consulta:
        if consultas.paciente.cpf == cpf:
            exibir_resumo_medico(consultas)
            exibir_resumo_consulta(consultas)
            encontrou = True

    if not encontrou:
        print("Nenhuma consulta encontrada para este paciente.")


def alterar_consulta(consultas, lista_medicos):
    cpf = ler_cpf("Digite o CPF do paciente da consulta que deseja alterar: ")
    data_str = data_hora_formatado("Digite a data atual da consulta (dd/mm/aaaa): ")
    hora_str = data_hora_formatado("Digite o horário atual da consulta (hh:mm em 24h): ")

    try:
        data = datetime.strptime(data_str, "%d/%m/%Y").date()
        hora = datetime.strptime(hora_str, "%H:%M").time()
        data_hora = datetime.combine(data, hora)
    except ValueError:
        print("Data ou hora inválida. Use o formato dd/mm/aaaa e hh:mm.")
        return

    for consulta in consultas:
        if consulta.paciente.cpf == cpf and consulta.data_hora == data_hora:
            print("Consulta encontrada. Insira os novos dados:")

            # Novo médico
            novo_crm = ler_crm("Novo CRM do médico: ")
            indice_medico = buscar_medico(lista_medicos, novo_crm)
            if indice_medico == -1:
                print("Médico não localizado.")
                return

            # Nova data e hora
            nova_data_str = data_hora_formatado("Nova data: ")
            nova_hora_str = data_hora_formatado("Novo horário: ")

            try:
                nova_data = datetime.strptime(nova_data_str, "%d/%m/%Y").date()
                nova_hora = datetime.strptime(nova_hora_str, "%H:%M").time()
                nova_data_hora = datetime.combine(nova_data, nova_hora)
            except ValueError:
                print("Nova data ou hora inválida. Use o formato dd/mm/aaaa e hh:mm.")
                return

            # Verifica se já existe uma consulta nesse novo horário
            if buscar_datas_horas_iguais(consultas, novo_crm, cpf, nova_data_hora):
                print("Já existe uma consulta nesse novo horário.")
                return

            # Atualiza os dados
            nova_descricao = input("Nova descrição da consulta: ").strip()
            consulta.medico = lista_medicos[indice_medico]
            consulta.data_hora = nova_data_hora
            if nova_descricao:
                consulta.descricao = nova_descricao

            exibir_resumo_consulta(consultas)
            print("Consulta alterada com sucesso!")
            return

    print("Consulta não encontrada com os dados informados.")


def excluir_consulta(consultas):
    cpf = ler_cpf("Digite o CPF do paciente da consulta que deseja excluir: ")

    consultas_do_paciente = [c for c in agendas if c.paciente.cpf == cpf]

    if not consultas_do_paciente:
        print("Nenhuma consulta encontrada para este CPF.")
        return

    print(f"== Consultas para o CPF {cpf} ==")
    for i, agendas in enumerate(consultas_do_paciente):
        exibir_resumo_consulta(agendas)
    
    try:
        escolha = int(input("Digite o número da consulta que deseja excluir: "))
        if escolha < 0  or escolha < len(consultas_do_paciente):
            consulta_selecionada = consultas_do_paciente[escolha - 1]
            
            confirmacao = int(input(f"Tem certeza que deseja excluir a consulta do paciente {consulta_selecionada.paciente.nome} com o médico {consulta_selecionada.medico.nome} na data {consulta_selecionada.data_hora.strftime('%d/%m/%Y %H:%M')}? (1 - Sim, 2 - Não): "))
            if confirmacao == 1:
                agendas.remove(consulta_selecionada)
                print("Consulta excluída com sucesso.")
            else:
                print("Exclusão cancelada.")
        else:
            print("Opção inválida.")
    except (ValueError, IndexError):
        print("Opção inválida.")
            
        

#-----------------------Funções Médico: Inserir, Listar Todos, Buscar um, Alterar, Excluir

def inserir_medico(lista_medicos, agendas):
    print("Insira as informações do(a) médico(a): ")

    crm = ler_crm("CRM: ")
    for novo_medico in lista_medicos:
        if novo_medico.crm == crm:
            print ("CRM já cadastrado!")
            return

    nome = ler_nome("Nome Completo: ").strip().upper()
    nascimento = ler_data_nascimento_medico("Data de nascimento: ")
    sexo = ler_sexo("Sexo (M/F): ")
    email = ler_email("Email: ")
    telefone = ler_telefone("Telefone: ")
    especialidade = escolher_especialidade()
       
    novo_medico = Medico(nome, nascimento, sexo, email, telefone, crm, especialidade)
    
    lista_medicos.append(novo_medico)
    horarios_disponiveis = cadastrar_horarios_disponiveis()
    agendas[crm] = AgendaMedica(novo_medico, horarios_disponiveis=horarios_disponiveis)
    print("Cadastrado com sucesso!")
        

def listar_todos_medicos(lista_medicos, agendas):
    if not lista_medicos:
        print("Não há médicos cadastrados!")
        return
    
    print ("==Lista de médicos cadastrados==")
    for i, medico in enumerate(lista_medicos, start=1):
            print(f"{i + 1}. CRM: {medico.crm} | Nome: {medico.nome} | Especialidade: {medico.especialidade} ")
            if medico.crm in agendas:
                total_consultas = len(agendas[medico.crm].consultas)
                print(f"   Total de Consultas Agendadas: {total_consultas}")
                print("-" * 100)            
    

def buscar_medico(lista_medico, crm, agendas=None):
    crm = crm.strip()

    for i, medico in enumerate(lista_medico):
        if medico.crm == crm:
            print("== Médico localizado ==")
            print(f"CRM: {medico.crm}")
            print(f"Especialidade: {medico.especialidade}")
            print(f"Nome: {medico.nome}")
            print(f"Sexo: {medico.sexo}")
            print(f"Data de Nascimento: {medico.nascimento}")  
            print(f"Telefone: {medico.telefone}")
            print(f"Email: {medico.email}")
            if agendas and medico.crm in agendas:
                total_consultas = len(agendas[medico.crm].consultas)
                print(f"Total de Consultas Agendadas: {total_consultas}") 
            print("-" * 100)
            return i
    else:
        print("Médico não localizado. Confira os dados informados!")
    return -1

def alterar_medico(listar_medicos, agendas):
    if len(listar_medicos) > 0:
        CRM_a_ser_alterado = ler_crm("Insira o CRM do médico a ser alterado: ")
        indice = buscar_medico(listar_medicos, CRM_a_ser_alterado)

        if indice == -1:
            print("CRM não está cadastrado!")
            return

        medico = listar_medicos[indice]

        if alterar_informacoes("Nome Completo: "):
            medico.nome = ler_nome("Insira o nome completo do médico: ").strip().upper()
        if alterar_informacoes("Data de nascimento: "):
            medico.nascimento = ler_data_nascimento_medico("Insira a data de nascimento do médico: ")
        if alterar_informacoes("Sexo (M/F): "):
            medico.sexo = ler_sexo("Insira o sexo do médico: ").strip()
        if alterar_informacoes("Email: "):
            medico.email = ler_email("Novo email: ").strip().lower()
        if alterar_informacoes("Telefone: "):
            medico.telefone = ler_telefone("Novo telefone: ").strip()
        
        if alterar_informacoes("CRM: "):
            novo_crm = ler_crm("Novo CRM: ").strip()
            agendas[novo_crm] = agendas.pop(medico.crm)
            medico.crm = novo_crm
        
        if alterar_informacoes("Especialidade: "):
            medico.especialidade = escolher_especialidade() 
        print ("Dado(s) alterado(s) com sucesso!")
        print("-" * 100)  
    else:
        print("Ainda não há médico(s) cadastrado(s)!")


def excluir_medico(listar_medicos, agendas):
    if len(listar_medicos) == 0:
        print("Ainda não há médico(s) cadastrado(s)!")
        return
    
    CRM_a_ser_excluido = ler_crm("Insira o CRM do(a) médico(a) a ser excluído(a): ")
    indice = buscar_medico(listar_medicos,CRM_a_ser_excluido)

    if indice == -1:
        print("CRM não cadastrado!")
        return
    
    confirmacao = int(input(f"Tem certeza que deseja excluir o(a) médico(a) {listar_medicos[indice].nome} | CRM {listar_medicos[indice].crm}? (1 - Sim, 2 - Não): "))
    if confirmacao == 1:
            medico_removido = listar_medicos.pop(indice)
            if CRM_a_ser_excluido in agendas:
                del agendas [CRM_a_ser_excluido]
            print(f"Médico(a) {medico_removido.nome} excluído(a) com sucesso!")
    else:
        print("Operação cancelada!")


#------PACIENTE Inserir, Listar Todos, Listar um, Alterar, Excluir

def inserir_paciente(lista_pacientes, agendas):
    print("Insira as informações do(a) paciente(a): ")

    cpf = ler_cpf("CPF: ")
    for novo_paciente in lista_pacientes:
        if novo_paciente.cpf == cpf:
            print ("CPF já cadastrado!")
            return

    nome = ler_nome("Nome: ").strip().upper()
    nascimento = ler_data_nascimento("Data de nascimento do(a) paciente: ")
    sexo = ler_sexo("Sexo (M/F): ")
    email = ler_email("Email: ")
    telefone = ler_telefone("Telefone: ")
    plano = escolher_plano_de_saude()
    historico_medico = input ("Histórico Médico ou Motivo: ")
        
    novo_paciente = Paciente(nome, nascimento, sexo, email, telefone, cpf, plano, historico_medico)
    
    lista_pacientes.append(novo_paciente)
    agendas[cpf] = AgendaMedica(novo_paciente)
    print("Cadastrado com sucesso!")


def listar_todos_pacientes(lista_pacientes, agendas):
    if not lista_pacientes:
        print("Não há pacientes cadastrados!")
        return
    
    print ("==Lista de pacientes cadastrados==")
    for i, paciente in enumerate(lista_pacientes, start=1):
            print(f"{i + 1}. CPF: {paciente.cpf}")
            print(f"Nome: {paciente.nome}")
            print(f"Nascimento: {paciente.nascimento}")
            print(f"Sexo: {paciente.sexo}")
            print(f"Telefone: {paciente.telefone}")
            print(f"Plano: {paciente.plano}")
            print(f"Histórico Médico ou Motivo: {paciente.historico_medico}")
            if paciente.cpf in agendas:
                total_consultas = len(agendas[paciente.cpf].consultas)
                print(f"Total de Consultas Agendadas: {total_consultas}")
                print("-" * 100)
    


def buscar_paciente(lista_paciente, cpf, agendas=None):
    cpf = cpf.strip()

    for i, paciente in enumerate(lista_paciente):
        if paciente.cpf == cpf:
            print("== Paciente localizado ==")
            print(f"CPF: {paciente.cpf}")
            print(f"Nome: {paciente.nome}")
            print(f"Nascimento: {paciente.nascimento}")
            print(f"Sexo: {paciente.sexo}")
            print(f"Telefone: {paciente.telefone}")
            print(f"Plano: {paciente.plano}")
            print(f"Histórico Médico ou Motivo: {paciente.historico_medico}")
            if agendas and paciente.cpf in agendas:
                total_consultas = len(agendas[paciente.cpf].consultas)
                print(f"Total de Consultas Agendadas: {total_consultas}")
            print("-" * 100)
            return i
    else:
        print("Paciente não localizado. Confira os dados informados!")
    return -1

def alterar_paciente(listar_pacientes, agendas):
    if len(listar_pacientes) > 0:
        CPF_a_ser_alterado = ler_cpf("Insira o CPF do paciente a ser alterado: ")
        indice = buscar_paciente(listar_pacientes, CPF_a_ser_alterado)

        if indice == -1:
            print("CPF não está cadastrado!")
            return
        
        paciente = listar_pacientes[indice]
        if alterar_informacoes("Nome Completo: "):
            paciente.nome = ler_nome("Insira o nome do(a) paciente: ")
        if alterar_informacoes("Data de nascimento: "):
            paciente.nascimento = ler_data_nascimento("Insira a data de nascimento do(a) paciente: ")
        if alterar_informacoes("Sexo (M/F): "): 
            paciente.sexo = ler_sexo("Insira o sexo do(a) paciente: ")
        if alterar_informacoes("Email: "):  
            paciente.email = ler_email("Novo email: ")
        if alterar_informacoes("Telefone: "):  
            paciente.telefone = ler_telefone("Novo telefone: ")

        if alterar_informacoes("CPF: "):   
            novo_cpf = ler_cpf("Novo CPF: ").strip()
            agendas[novo_cpf] = agendas.pop(paciente.cpf)
            paciente.cpf = novo_cpf

        if alterar_informacoes("Plano: "):   
            paciente.plano = escolher_plano_de_saude()

        if alterar_informacoes("Histórico Médico ou Motivo: "):
            paciente.historico_medico = input("Insira os dados do histórico médico ou Motivo: ")
        
        print ("Dado(s) alterado(s) com sucesso!")
        print("-" * 100)
    else:
        print("Ainda não há paciente(s) cadastrados!")


def excluir_paciente(listar_pacientes, agendas):
    if len(listar_pacientes) == 0:
        print("Ainda não há pacientes cadastrados!")
        return
    
    CPF_a_ser_excluido = ler_cpf("Insira o CPF do paciente a ser excluído: ")
    indice = buscar_paciente(listar_pacientes, CPF_a_ser_excluido)

    if indice == -1:
        print("CPF não cadastrado!")
        return
    
    confirmacao = int(input(f"Tem certeza que deseja excluir o(a) paciente(a) {listar_pacientes[indice].nome} | CPF {listar_pacientes[indice].cpf}? (1 - Sim, 2 - Não): "))
    if confirmacao == 1:
        paciente_removido = listar_pacientes.pop(indice)
            
        for agenda in agendas.values():
            agenda.consultas = [consulta for consulta in agenda.consultas if consulta.paciente.cpf != CPF_a_ser_excluido]
        print(f"Paciente: {paciente_removido.nome} excluído com sucesso!")
    else:
        print("Operação cancelada!")
        