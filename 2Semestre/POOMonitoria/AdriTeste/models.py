#Classes Principais

class Pessoa:
    def __init__(self, nome, nascimento, sexo, email, telefone):
        self.nome = nome
        self.nascimento = nascimento
        self.sexo = sexo
        self.email = email
        self.telefone = telefone
        
        
class Medico(Pessoa):
    def __init__(self, nome, nascimento, sexo, email, telefone, crm, especialidade):
        super().__init__(nome, nascimento, sexo, email, telefone)
        self.crm = crm
        self.especialidade = especialidade.strip().upper()

    @property
    def crm(self):
        return self._crm
    
    @crm.setter
    def crm(self, valor):
        valor = valor.strip()
        if valor.isdigit() and 4 <= len(valor) <= 6:
            self._crm = valor
        else:
            raise ValueError("CRM inválido. Deve conter entre 4 e 6 dígitos numéricos.")


class Paciente(Pessoa):
    def __init__(self, nome, nascimento, sexo, email, telefone, cpf, plano, historico_medico):
        super().__init__(nome, nascimento, sexo, email, telefone)
        self.cpf = cpf
        self.plano = plano
        self.historico_medico = historico_medico

    @property
    def cpf(self):
        return self._cpf
    
    @cpf.setter
    def cpf(self, valor):
        if valor.isdigit() and len(valor) == 11:
            self._cpf = valor
        else:
            raise ValueError("CPF inválido. Deve conter 11 dígitos numéricos.")

class Consulta:
    def __init__(self, medico, paciente, data_hora, descricao):
        self.paciente = paciente
        self.medico = medico
        self.data_hora = data_hora
        self.descricao = descricao
       
    def __str__(self):
        return (f"CRM: {self.medico.crm} | Médico: {self.medico.nome} | Especialidade: {self.medico.especialidade}\n"
                f"CPF: {self.paciente.cpf} | Paciente: {self.paciente.nome}\n"
                f"Data: {self.data_hora} | Descrição: {self.descricao}")

class AgendaMedica:
    def __init__(self, medico, horarios_disponiveis=None, consultas=None):
        self.medico = medico
        self.horarios_disponiveis =  horarios_disponiveis if horarios_disponiveis else []
        self.consultas = consultas if consultas else []

    def agendar_consulta(self, consulta: Consulta):
        self.consultas.append(consulta)

    def listar_consultas(self):
        
        if not self.consultas:
            print("Nenhuma consulta agendada.")
            return
        for i, consulta in enumerate(self.consultas):
            print(f"{i}. {consulta}\n")

            

    def alterar_consulta(self, consulta: Consulta, novo_medico=None, nova_data_hora=None, novo_paciente=None):
        if consulta in self.consultas:
            if novo_medico:
                consulta.medico = novo_medico
            if nova_data_hora:
                consulta.data_hora = nova_data_hora
            if novo_paciente:
                consulta.paciente = novo_paciente

    def cancelar_consulta(self, consulta: Consulta):
        if consulta in self.consultas:
            self.consultas.remove(consulta)
            print("Consulta cancelada com sucesso.")
    
    def buscar_consultas_por_cpf(self, cpf: str):
        resultados = [consulta for consulta in self.consultas if consulta.paciente.cpf == cpf]
        if resultados:
            print(f"\nConsultas encontradas para o CPF {cpf}:")
            for i, consulta in enumerate(resultados):
                print(f"{i}. Médico: {consulta.medico.nome} | Especialidade: {consulta.medico.especialidade}")
                print(f"    Data: {consulta.data_hora} | Descrição: {consulta.descricao}")
        else:
            print(f"\nNenhuma consulta encontrada para o CPF {cpf}.")


especialidades_disponiveis = [
    "2. CARDIOLOGIA", "3. ENDOCRINOLOGIA", "6. DERMATOLOGIA",
     "9. NEUROLOGIA", "10. PEDIATRIA", "12. PSIQUIATRIA", ""
     "45. GINECOLOGIA", "52. ORTOPEDIA", "50. OFTALMOLOGIA", 
    ]

planos_de_saude = [
    "1. AMIL", "2. BRADESCO", "3. GEAP",
    "4. HAPVIDA", "5. NOTREDAME", "6. OUTROS",
    "7. PORTO SEGURO", "8. SAUDE CAIXA","9. SULAMERICA", 
    "10. UNIMED", "11. PARTICULAR"
]