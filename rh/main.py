from classe_funcionario import Funcionario

# Lista principal do sistema
classe_funcionario = []

# Funcionario 1
func1 = Funcionario(
    "Marcos Silva", "marcosiilva@gmail.com", "(21)00000-000000",
    "111.111.111-11", "Desenvolvedor Senior", "TI", "10/01/2024"
)
func1.cadastro_hora("Jan", 160)
func1.cadastro_salario_hora("Jan", 50)
classe_funcionario.append(func1)

# Funcionário 2
func2 = Funcionario(
    "Ana Souza", "ana@gmail.com", "(21)98888-2222",
    "222.222.222-22", "Designer", "Marketing", "15/03/2023"
)
func2.cadastro_hora("Jan", 140)
func2.cadastro_salario_hora("Jan", 35)
classe_funcionario.append(func2)

# Funcionário 3
func3 = Funcionario(
    "Carlos Lima", "carlos@gmail.com", "(21)97777-3333",
    "333.333.333-33", "Analista Senior", "Financeiro", "22/08/2022"
)
func3.cadastro_hora("Jan", 180)
func3.cadastro_salario_hora("Jan", 45)
classe_funcionario.append(func3)


# MENU PRINCIPAL
while True:
    print("\n===============SISTEMA RH===============")
    print("1 - Listar Funcionários")
    print("2 - Buscar por nome")
    print("3 - Buscar por Matrícula")
    print("4 - Calcular Salário")
    print("5 - Sair")
    print("=====================================================")

    opcao = input("Escolha uma Opção: ").strip()

    # 1 - Listar Todos
    if opcao == "1":
        if not classe_funcionario:
            print("Nenhum funcionário cadastrado.")
        else:
            for f in classe_funcionario:
                print(f)
            
    # 2 - Buscar por nome
    elif opcao == "2":
        nome_busca = input("Digite o nome: ").strip().lower()
        resultados = [f for f in classe_funcionario if f.nome.lower() == nome_busca]
        
        if resultados:
            for f in resultados:
                print(f)
        else:
            print("Funcionário não encontrado.")
    
    # 3 - Buscar por matricula
    elif opcao == "3":
        try:
            matricula_busca = int(input("Digite a matrícula: "))
            resultados = [f for f in classe_funcionario if f.matricula == matricula_busca]
            
            if resultados:
                print(resultados[0])
            else:
                print("Matrícula não Encontrada.")
        except ValueError:
            print("Erro: Digite apenas números para a matrícula.")
    
    # 4 - Calcular salário
    elif opcao == "4":
        try:
            matricula_busca = int(input("Digite a matrícula: "))
            mes = input("Digite o mês: ").strip()
            resultados = [f for f in classe_funcionario if f.matricula == matricula_busca]
            
            if resultados:
                funcionario = resultados[0]
                salario = funcionario.calcula_salario(mes)
                print(f"\nSalário de {funcionario.nome}: R$ {salario}")
            else:
                print("Funcionário Inexistente, verifique os dados.")
        except ValueError:
            print("Erro: Digite apenas números para a matrícula.")
    
    # 5 - Sair
    elif opcao == "5":
        print("Encerrando Sistema......")
        break

    # Opção inválida do menu principal
    else:
        print("Opção Inválida. Escolha um número de 1 a 5.")
