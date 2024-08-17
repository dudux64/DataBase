import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

def main():
    # Configuração do banco de dados
    db_config = {
        'host': 'localhost',         # Endereço do servidor MySQL (use 'localhost' se estiver rodando localmente)
        'user': 'root',              # Seu nome de usuário MySQL
        'password': '2136',          # Sua senha MySQL
        'database': 'meu_banco_de_dados'  # Nome do banco de dados que você criou
    }

    try:
        # Criar um pool de conexões MySQL
        pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                           pool_size=5,
                                           pool_reset_session=True,
                                           **db_config)

        connection = pool.get_connection()

        if connection.is_connected():
            cursor = connection.cursor()
            y = int(input("Se você quiser adicionar, digite 1; Se quiser remover, digite 2, Digite 3 se Quiser Alterar Um dado!: "))

            if y == 1:
                nome = input("Nome do Cliente: ")
                email = input("Email do Cliente: ")

                # Inserir dados na tabela 'users'
                insert_users_query = """
                    INSERT INTO users (name, email) 
                    VALUES (%s, %s)
                """
                try:
                    cursor.execute(insert_users_query, (nome, email))
                    connection.commit()
                    print(f"{nome} adicionado com sucesso!")
                except Error as error:
                    # Verificar se o erro é de entrada duplicada
                    if error.errno == 1062:  # ER_DUP_ENTRY
                        print('Dados de exemplo já existem na tabela "users"')
                    else:
                        # Se não for erro de entrada duplicada, relançar a exceção
                        raise error

            elif y == 2:
                id = int(input("Qual o número do ID que deseja remover?: "))

                # Deletar dados da tabela 'users'
                delete_users_query = "DELETE FROM users WHERE id = %s"
                try:
                    cursor.execute(delete_users_query, (id,))
                    connection.commit()
                    print(f"ID {id} removido com sucesso!")
                except Error as error:
                    print(f"Erro ao remover o ID {id}: {error}")

            elif y == 3:  # Supondo que a opção 3 seja para atualizar
                id = int(input("Qual o número do ID que deseja atualizar?: "))
                novo_nome = input("Novo Nome do Cliente: ")
                novo_email = input("Novo Email do Cliente: ")

                update_query = """
                    UPDATE users
                    SET name = %s, email = %s
                    WHERE id = %s
                """
                try:
                    cursor.execute(update_query, (novo_nome, novo_email, id))
                    connection.commit()
                    print(f"ID {id} atualizado com sucesso!")
                except Error as error:
                    print(f"Erro ao atualizar o ID {id}: {error}")

            else:
                print("ERRO! Opção inválida.")
            

            # Selecionar todos os usuários
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            print('Dados atuais na tabela "users":')
            for row in results:
                print(row)

    except Error as err:
        print(f'Ocorreu um erro: {err}')
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print('Conexão ao pool foi encerrada')

if __name__ == "__main__":
    main()
