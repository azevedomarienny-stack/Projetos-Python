import customtkinter as ctk
from tkinter import messagebox
import re
from banco import (
    inicializar_banco, 
    validar_credenciais, 
    cadastrar_novo_usuario, 
    listar_todos_usuarios, 
    deletar_usuario_banco,
    alterar_senha_usuario_banco
)

ctk.set_appearance_mode("light")

class Dashboard(ctk.CTk):
    def __init__(self, nome_usuario):
        super().__init__()
        self.title("Dashboard - Sistema Principal")
        self.geometry("850x550")
        self.resizable(False, False)
        self.configure(fg_color="#FFFFFF")

        self.nome_usuario = nome_usuario
        self.cor_vinho = "#4A0E17"
        self.cor_rosa = "#D81B60"

        self.sidebar = ctk.CTkFrame(master=self, width=220, height=550, fg_color=self.cor_vinho, corner_radius=0)
        self.sidebar.place(x=0, y=0)

        self.lbl_menu = ctk.CTkLabel(master=self.sidebar, text="PAINEL ADM" if nome_usuario == "admin" else "MENU", font=("Helvetica", 16, "bold"), text_color="#FFFFFF")
        self.lbl_menu.place(relx=0.5, y=30, anchor="center")

        self.scroll_usuarios = ctk.CTkScrollableFrame(master=self.sidebar, width=180, height=350, fg_color="transparent")
        self.scroll_usuarios.place(x=10, y=60)

        self.painel_principal = ctk.CTkFrame(master=self, width=590, height=510, fg_color="#FFFFFF", corner_radius=0)
        self.painel_principal.place(x=240, y=20)

        self.atualizar_lista_menu()
        self.mostrar_boas_vindas()

        self.btn_sair = ctk.CTkButton(master=self.sidebar, text="Sair", fg_color=self.cor_rosa, hover_color="#AD1457", command=self.destroy)
        self.btn_sair.place(relx=0.5, y=510, anchor="center")

    def mostrar_boas_vindas(self):
        for widget in self.painel_principal.winfo_children():
            widget.destroy()

        lbl_welcome = ctk.CTkLabel(master=self.painel_principal, text=f"Olá, {self.nome_usuario.upper()}!\nBem-vindo ao Painel de Controle.", font=("Helvetica", 24, "bold"), text_color=self.cor_vinho)
        lbl_welcome.pack(pady=(100, 10))

        if self.nome_usuario == "admin":
            lbl_instrucao = ctk.CTkLabel(master=self.painel_principal, text="← Selecione um usuário na barra lateral para gerenciar.", font=("Helvetica", 13, "italic"), text_color="gray")
            lbl_instrucao.pack(pady=10)

    def atualizar_lista_menu(self):
        for widget in self.scroll_usuarios.winfo_children():
            widget.destroy()

        if self.nome_usuario == "admin":
            usuarios = listar_todos_usuarios()
            if not usuarios:
                lbl_vazio = ctk.CTkLabel(master=self.scroll_usuarios, text="Nenhum usuário\ncadastrado.", font=("Helvetica", 11, "italic"), text_color="#FFFFFF")
                lbl_vazio.pack(pady=20)
                return

            for usuario, senha in usuarios:
                btn_user = ctk.CTkButton(
                    master=self.scroll_usuarios, text=usuario, fg_color="transparent", text_color="#FFFFFF",
                    hover_color="#6B1D28", anchor="w", font=("Helvetica", 13, "bold"),
                    command=lambda u=usuario, s=senha: self.exibir_detalhes_usuario(u, s)
                )
                btn_user.pack(fill="x", pady=4, padx=5)

    def exibir_detalhes_usuario(self, usuario, senha):
        for widget in self.painel_principal.winfo_children():
            widget.destroy()

        lbl_titulo_card = ctk.CTkLabel(master=self.painel_principal, text=f"Gerenciar Usuário: {usuario}", font=("Helvetica", 22, "bold"), text_color=self.cor_vinho)
        lbl_titulo_card.pack(anchor="w", padx=40, pady=(20, 10))

        card_dados = ctk.CTkFrame(master=self.painel_principal, width=500, height=300, fg_color="#F4F4F6", corner_radius=15)
        card_dados.pack(anchor="w", padx=40, pady=10, fill="x")
        card_dados.pack_propagate(False)

        lbl_user_info = ctk.CTkLabel(master=card_dados, text=f"Nome de Usuário:  {usuario}", font=("Helvetica", 15, "bold"), text_color="#000000")
        lbl_user_info.pack(anchor="w", padx=30, pady=(30, 10))

        lbl_senha_info = ctk.CTkLabel(master=card_dados, text=f"Senha Registrada:  {senha}", font=("Helvetica", 15), text_color="#333333")
        lbl_senha_info.pack(anchor="w", padx=30, pady=10)

        painel_botoes = ctk.CTkFrame(master=card_dados, fg_color="transparent")
        painel_botoes.pack(fill="x", padx=30, pady=(30, 0))

        btn_alterar = ctk.CTkButton(master=painel_botoes, text="ALTERAR SENHA", fg_color="#4A0E17", hover_color="#32090F", font=("Helvetica", 12, "bold"), height=40, command=lambda: self.abrir_janela_alterar(usuario, senha))
        btn_alterar.pack(side="left", expand=True, fill="x", padx=(0, 10))

        btn_excluir = ctk.CTkButton(master=painel_botoes, text="EXCLUIR USUÁRIO", fg_color=self.cor_rosa, hover_color="#AD1457", font=("Helvetica", 12, "bold"), height=40, command=lambda: self.confirmar_exclusao(usuario))
        btn_excluir.pack(side="right", expand=True, fill="x", padx=(10, 0))

    def abrir_janela_alterar(self, usuario, senha_atual):
        for widget in self.painel_principal.winfo_children():
            widget.destroy()

        lbl_titulo_card = ctk.CTkLabel(master=self.painel_principal, text=f"Alterar Senha: {usuario}", font=("Helvetica", 22, "bold"), text_color=self.cor_vinho)
        lbl_titulo_card.pack(anchor="w", padx=40, pady=(20, 10))

        card_dados = ctk.CTkFrame(master=self.painel_principal, width=500, height=300, fg_color="#F4F4F6", corner_radius=15)
        card_dados.pack(anchor="w", padx=40, pady=10, fill="x")
        card_dados.pack_propagate(False)

        lbl_instrucao = ctk.CTkLabel(master=card_dados, text="Digite a nova senha forte:", font=("Helvetica", 15, "bold"), text_color="#000000")
        lbl_instrucao.pack(anchor="w", padx=30, pady=(30, 10))

        input_nova_senha = ctk.CTkEntry(master=card_dados, width=280, height=40, corner_radius=20, placeholder_text="Nova senha", show="*", justify="center")
        input_nova_senha.pack(anchor="w", padx=30, pady=10)

        painel_botoes = ctk.CTkFrame(master=card_dados, fg_color="transparent")
        painel_botoes.pack(fill="x", padx=30, pady=(30, 0))

        def salvar_mudanca():
            nova_senha = input_nova_senha.get()
            if not nova_senha:
                messagebox.showwarning("Campo Vazio", "Por favor, preencha a nova senha.")
                return

            padrao_senha = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
            if not re.match(padrao_senha, nova_senha):
                messagebox.showerror("Senha Fraca", "A nova senha deve ter no mínimo 8 caracteres, números, maiúsculas, minúsculas e caractere especial.")
                return

            if alterar_senha_usuario_banco(usuario, nova_senha):
                messagebox.showinfo("Sucesso", f"Senha de '{usuario}' atualizada com sucesso!")
                self.atualizar_lista_menu()
                self.exibir_detalhes_usuario(usuario, nova_senha)
            else:
                messagebox.showerror("Erro SQL", "Não foi possível atualizar os dados.")

        btn_salvar = ctk.CTkButton(master=painel_botoes, text="CONFIRMAR ALTERAÇÃO", fg_color=self.cor_rosa, hover_color="#AD1457", font=("Helvetica", 12, "bold"), height=40, command=salvar_mudanca)
        btn_salvar.pack(side="left", expand=True, fill="x", padx=(0, 10))

        btn_cancelar = ctk.CTkButton(master=painel_botoes, text="CANCELAR", fg_color="#4A0E17", hover_color="#32090F", font=("Helvetica", 12, "bold"), height=40, command=lambda: self.exibir_detalhes_usuario(usuario, senha_atual))
        btn_cancelar.pack(side="right", expand=True, fill="x", padx=(10, 0))

    def confirmar_exclusao(self, usuario):
        resposta = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja deletar o usuário '{usuario}' permanentemente?")
        if resposta:
            if deletar_usuario_banco(usuario):
                messagebox.showinfo("Sucesso", f"Usuário '{usuario}' excluído via comando SQL DELETE!")
                self.atualizar_lista_menu()
                self.mostrar_boas_vindas()
            else:
                messagebox.showerror("Erro SQL", "Não foi possível excluir o usuário.")


class TelaLogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Acesso ao Sistema")
        self.geometry("750x450")
        self.resizable(False, False)
        self.configure(fg_color="#FFFFFF")

        self.cor_vinho_fundo = "#4A0E17"
        self.cor_rosa_btn = "#D81B60"
        self.cor_texto_claro = "#FFFFFF"
        self.modo_cadastro = False

        self.painel_esquerdo = ctk.CTkFrame(master=self, width=375, height=450, fg_color=self.cor_vinho_fundo, corner_radius=0)
        self.painel_esquerdo.place(x=0, y=0)

        self.painel_direito = ctk.CTkFrame(master=self, width=375, height=450, fg_color="#FFFFFF", corner_radius=0)
        self.painel_direito.place(x=375, y=0)
        
        self.label_decorativa = ctk.CTkLabel(master=self.painel_direito, text="Painel de Controle\nSua Empresa", font=("Helvetica", 20, "bold"), text_color="#4A0E17")
        self.label_decorativa.place(relx=0.5, rely=0.5, anchor="center")

        self.label_titulo = ctk.CTkLabel(master=self.painel_esquerdo, text="BEM-VINDO", font=("Helvetica", 24, "bold"), text_color=self.cor_texto_claro)
        self.label_titulo.place(relx=0.5, rely=0.15, anchor="center")

        self.input_usuario = ctk.CTkEntry(master=self.painel_esquerdo, width=280, height=40, corner_radius=20, placeholder_text="Usuário", fg_color="#FFFFFF", text_color="#000000", placeholder_text_color="gray", border_width=0, justify="center")
        self.input_usuario.place(relx=0.5, rely=0.35, anchor="center")

        self.input_senha = ctk.CTkEntry(master=self.painel_esquerdo, width=280, height=40, corner_radius=20, placeholder_text="Senha", show="*", fg_color="#FFFFFF", text_color="#000000", placeholder_text_color="gray", border_width=0, justify="center")
        self.input_senha.place(relx=0.5, rely=0.50, anchor="center")
        
        self.check_lembrar = ctk.CTkCheckBox(master=self.painel_esquerdo, text="Lembrar-me", font=("Helvetica", 11), text_color=self.cor_texto_claro, checkmark_color=self.cor_vinho_fundo, fg_color="#FFFFFF", border_width=2, checkbox_width=18, checkbox_height=18)
        self.check_lembrar.place(x=48, y=273)
        
        self.label_alternar = ctk.CTkLabel(master=self.painel_esquerdo, text="Cadastrar nova conta", font=("Helvetica", 10, "underline"), text_color=self.cor_texto_claro, cursor="hand2")
        self.label_alternar.place(x=225, y=273)
        
        # CORRIGIDO: Evento de clique do mouse adicionado
        self.label_alternar.bind("<Button-1>", lambda event: self.alternar_modo())
        
        self.btn_principal = ctk.CTkButton(master=self.painel_esquerdo, text="ENTRAR", width=280, height=40, corner_radius=20, fg_color=self.cor_rosa_btn, hover_color="#AD1457", font=("Helvetica", 14, "bold"), text_color=self.cor_texto_claro, command=self.processar_acao)
        self.btn_principal.place(relx=0.5, rely=0.78, anchor="center")
        
    def alternar_modo(self):
        self.modo_cadastro = not self.modo_cadastro
        if self.modo_cadastro:
            self.label_titulo.configure(text="REGISTRAR")
            self.btn_principal.configure(text="CADASTRAR")
            self.label_alternar.configure(text="Voltar para o Login")
            self.check_lembrar.place_forget()
        else:
            self.label_titulo.configure(text="BEM-VINDO")
            self.btn_principal.configure(text="ENTRAR")
            self.label_alternar.configure(text="Cadastrar nova conta")
            self.check_lembrar.place(x=48, y=273)
            
    def processar_acao(self):
        import re
        usuario = self.input_usuario.get()
        senha = self.input_senha.get()
        
        if not usuario or not senha:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")
            return
            
        if self.modo_cadastro:
            padrao_senha = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
            if not re.match(padrao_senha, senha):
                mensagem_erro = (
                    "A senha não atende aos requisitos de segurança:\n\n"
                    "• Mínimo de 8 caracteres\n"
                    "• Pelo menos uma letra maiúscula\n"
                    "• Pelo menos uma letra minúscula\n"
                    "• Pelo menos um número\n"
                    "• Pelo menos um caractere especial (@, $, !, %, *, ?, &)"
                )
                messagebox.showerror("Senha Fraca", mensagem_erro)
                return
                
            if cadastrar_novo_usuario(usuario, senha):
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso via SQL!")
                self.alternar_modo()
            else:
                messagebox.showerror("Erro SQL", "Este nome de usuário já existe.")
        else:
            if validar_credenciais(usuario, senha):
                messagebox.showinfo("Sucesso", f"Login autorizado via banco SQL!")
                self.destroy()
                dashboard_app = Dashboard(usuario)
                dashboard_app.mainloop()
            else:
                messagebox.showerror("Erro SQL", "Usuário ou senha inválidos.")


if __name__ == "__main__":
    inicializar_banco()
    app = TelaLogin()
    app.mainloop()
