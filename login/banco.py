import sqlite3
import bcrypt


def inicializar_banco():
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    try:
        senha_admin = bcrypt.hashpw(
            "123".encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            ("admin", senha_admin)
        )

        conexao.commit()

    except sqlite3.IntegrityError:
        pass

    finally:
        conexao.close()


def validar_credenciais(usuario, senha):
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT senha FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    resultado = cursor.fetchone()

    conexao.close()

    if resultado:
        senha_hash = resultado[0].encode("utf-8")

        return bcrypt.checkpw(
            senha.encode("utf-8"),
            senha_hash
        )

    return False


def cadastrar_novo_usuario(usuario, senha):
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()

    try:
        senha_hash = bcrypt.hashpw(
            senha.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",
            (usuario, senha_hash)
        )

        conexao.commit()

        sucesso = True

    except sqlite3.IntegrityError:
        sucesso = False

    finally:
        conexao.close()

    return sucesso


def listar_todos_usuarios():
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT usuario, senha FROM usuarios WHERE usuario != 'admin'"
    )

    usuarios = cursor.fetchall()

    conexao.close()

    return usuarios


def deletar_usuario_banco(usuario):
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()

    try:
        cursor.execute(
            "DELETE FROM usuarios WHERE usuario = ?",
            (usuario,)
        )

        conexao.commit()

        sucesso = True

    except Exception:
        sucesso = False

    finally:
        conexao.close()

    return sucesso


def alterar_senha_usuario_banco(usuario, nova_senha):
    conexao = sqlite3.connect("sistema.db")
    cursor = conexao.cursor()

    try:
        nova_senha_hash = bcrypt.hashpw(
            nova_senha.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            "UPDATE usuarios SET senha = ? WHERE usuario = ?",
            (nova_senha_hash, usuario)
        )

        conexao.commit()

        sucesso = True

    except Exception:
        sucesso = False

    finally:
        conexao.close()

    return sucesso