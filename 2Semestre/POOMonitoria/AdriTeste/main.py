from cadastros import inserir_medico, buscar_medico, listar_todos_medicos, alterar_medico, excluir_medico
from cadastros import inserir_paciente, buscar_paciente, listar_todos_pacientes, alterar_paciente, excluir_paciente
from cadastros import inserir_consulta, listar_consulta, listar_uma_consulta, alterar_consulta, excluir_consulta
from funcoes_auxiliares import ler_crm, ler_cpf, ler_opcao_valida
from funcoes_auxiliares import buscar_medico_especialidade, buscar_paciente_cpf, listar_consulta_por_data
import os
import shutil


def limpar_pasta_pyapache():
    pasta = "pyapache"
    if os.path.exists(pasta):
        shutil.rmtree(pasta)
        print("Pasta pyapache limpa.")
    os.makedirs(pasta)

#Acima limpeza automática da pasta pyapache
#------------------Menu Principal-------------------------------

def exibir_menu_principal():
        
    print("========================================")
    print("========================================")
    print("= MEDAGENDA - SISTEMA DE AGENDA MÉDICA =")
    print("========================================")
    print("==========  Menu de opções  ============")
    print("1.===============================Médicos")
    print("2.=============================Pacientes")
    print("3.=============================Consultas")
    print("4.============================Relatórios")
    print("0.==================================Sair")
    print("========================================")
    print("========================================")


def iniciar_sistema():

    consultas = []
    pacientes = []
    medicos = []
    agendas = {}
    


    j = ""
    while j != "0":
        exibir_menu_principal()
        j = ler_opcao_valida ("Escolha uma opção no menu: ",[1,2,3,4,5,0])
        if j == '1':
            menu_medico_escolha(medicos, agendas)
        elif j == '2':
            menu_paciente_escolha(pacientes, agendas)
        elif j == '3':
            menu_consulta(consultas, medicos, pacientes, agendas)
        elif j == '4':
            menu_exibir_relatorio(consultas, medicos, pacientes)
        elif j == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")


#---------------------------Menu de opções de médicos------------------
def menu_medico_inicio():
    print("====================================")
    print("====================================")
    print("1.====================Inserir médico")
    print("2.=========Listar todos os médico(s)")
    print("3.==================Buscar um médico")
    print("4.====================Alterar médico")
    print("5.====================Excluir médico")
    print("0.============================Voltar")
    print("====================================")
    print("====================================")
    

def menu_medico_escolha(medicos, agendas):
    j = ""
    while j != "0":
        menu_medico_inicio()
        j = ler_opcao_valida ("Escolha uma opção no menu: ",[1,2,3,4,5,0])

        if j == '1':
            inserir_medico(medicos, agendas)

        elif j == '2':
            listar_todos_medicos(medicos, agendas)

        elif j == '3':
            crm_digitado = ler_crm("Digite o CRM do médico que deseja buscar: ").strip()
            buscar_medico(medicos, crm_digitado, agendas)

        elif j =='4':
            alterar_medico(medicos, agendas)
        
        elif j == '5':
            excluir_medico(medicos, agendas)

        elif j != "0":
            print("Opção inválida.")

#----------------------------Menu de opções paciente-------------------

def menu_paciente_inicio():
    print("====================================")
    print("====================================")
    print("1.==================Inserir paciente")
    print("2.================Listar paciente(s)")
    print("3.================Buscar um paciente")
    print("4.================= Alterar paciente")
    print("5.==================Excluir paciente")
    print("0.===========================Voltar ")
    print("====================================")
    print("====================================")

def menu_paciente_escolha(pacientes, agendas):
    j = ""
    while j != "0":

        j = menu_paciente_inicio()
        j = ler_opcao_valida ("Escolha uma opção no menu: ",[1,2,3,4,5,0])

        if j == '1':
            inserir_paciente(pacientes, agendas)

        elif j == '2':
            listar_todos_pacientes(pacientes, agendas)

        elif j == '3':
            cpf_digitado = ler_cpf("Digite o CPF do paciente que deseja buscar: ").strip()
            buscar_paciente(pacientes,cpf_digitado, agendas)
        
        elif j == '4':
            alterar_paciente(pacientes, agendas)

        elif j == '5':
            excluir_paciente(pacientes, agendas)

        elif j != "0":
            print("Opção inválida.")

#---------------------------Menu de consultas-----------------

def menu_consulta_inicio():
    print("====================================")
    print("====================================")
    print("1.================= Inserir consulta")
    print("2.============== Listar consultas(s)")
    print("3.============== Buscar uma consulta")
    print("4.================= Alterar consulta")
    print("5.================= Excluir consulta")
    print("0.============================= Sair")
    print("====================================")
    print("====================================")



def menu_consulta(consultas, agendas, medicos, pacientes):
    j = ""
    while j != "0":
        menu_consulta_inicio()
        j = ler_opcao_valida ("Escolha uma opção no menu: ",[1,2,3,4,5,0])

        if j == '1':
            inserir_consulta(consultas, medicos, pacientes, agendas)

        elif j == '2':
            listar_consulta(consultas, agendas)

        elif j == '3':
            listar_uma_consulta(consultas, agendas)

        elif j == '4':
            alterar_consulta(consultas, agendas)

        elif j == '5':
            excluir_consulta(consultas, agendas)

        elif j != "0":
            print("Opção inválida.")

#---------------------Menu-Relatórios-------------
def menu_relatorio(medicos, pacientes, agendas):
    print("===========================================")
    print("|=========================================|")
    print("1.======Dados dos médicos por especialidade")
    print("2.==============Dados dos pacientes por CPF")
    print("3.==============Lista de consultas por data")
    print("0.=====================================Sair")
    print("===========================================")
    print("===========================================")



def menu_exibir_relatorio(agendas, medicos, pacientes):
    j = ""
    while j != "0":
        menu_relatorio()
        j = ler_opcao_valida ("Escolha uma opção no menu: ",[1,2,3,4,5,0])
        if j == '1':
            buscar_medico_especialidade(medicos)

        elif j == '2':
            cpf = ler_cpf("Digite o CPF do paciente que deseja buscar: ").strip()
            buscar_paciente_cpf(pacientes, cpf)

        elif j == '3':
            data = input("Digite a data (AAAA-MM-DD) para listar as consultas: ").strip()
            listar_consulta_por_data(agendas, data)

        elif j != "0":
            print("Opção inválida. ")

            
iniciar_sistema()
