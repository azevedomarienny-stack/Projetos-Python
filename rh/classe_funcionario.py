import random 


class Funcionario:

    def __init__(
            self, 
            nome,
            email,
            celular, 
            cpf, 
            cargo, 
            departamento, 
            data_contratacao
            ):

        #Dados génericos
        self.nome= nome
        self.email= email
        self.celular= celular
        self.cpf= cpf

        #Dados para o RH adm
        self.cargo = cargo
        self.departamento = departamento
        self.data_contratacao = data_contratacao

        #Matrícula automática
        self.matricula = random.randint(1000, 9999)

        #Dados de pagamento
        self.horas = {}
        self.salario_hora = {}


    #Cadastrro de horas trabalhadas
    def cadastro_hora(self, mes, horas):

        self.horas[mes] = horas

    #Cadastro do valor da hora
    def cadastro_salario_hora(self, mes, valor):
        self.salario_hora[mes] = valor

    #Calculo do salario
    def calcula_salario(self, mes):

        if(mes not in self.horas) or (mes not in self.salario_hora):
            return "Mês Inexistente"
        salario = self.horas[mes] * self.salario_hora[mes]
    
        #Bonus para cargos superiores
        if "Senior" in self.cargo:
            salario *= 1.10
        return salario
    
    #Exibição do Funcionario
    def __repr__(self):
        return(
            f"\nFuncionário: {self.nome}"
            f"\nMatrícula: {self.matricula}"
            f"\nCargo: {self.cargo}"
            f"\nDepartamento: {self.departamento}"
            f"\nCPF: {self.cpf}"
            f"\nEmail: {self.email}"
            f"\nCelular: {self.celular}"
            f"\nData de Contratação: {self.data_contratacao}"
            f"\nHoras Registradas: {self.horas}"
            f"\nSalário/horas: {self.salario_hora}"
            f"\n================================================="
        )
    

func = Funcionario(
        "teste",
        "teste@gmail.com",
        "999999-99999",
        "111.111.111-11",
        "Dev",
        "TI",
        "01/01/2024"
    )
print(func.nome)