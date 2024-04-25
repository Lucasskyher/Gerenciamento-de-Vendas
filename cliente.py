import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os.path
import pickle
from tkinter import simpledialog
from typing import Any

class Cliente:
    def __init__(self, nome, cpf, endereco, email):
        self.__nome = nome
        self.__cpf = cpf
        self.__endereco = endereco
        self.__email = email

    @property
    def nome(self):
        return self.__nome

    @property
    def cpf(self):
        return self.__cpf
    
    @property
    def endereco(self):
        return self.__endereco
    
    @property
    def email(self):
        return self.__email
    
    def getCliente(self):
        return f"Nome: {self.__nome}\nCPF: {self.__cpf}\nEndereço: {self.__endereco}\nE-mail: {self.__email}\n\n--+--+--+--+--+--+--+--+--\n"

    def atualizarCliente(self,novo_nome,novo_cpf,novo_endereco,novo_email):
        
        self.__nome = novo_nome
        self.__cpf = novo_cpf
        self.__endereco = novo_endereco
        self.__email = novo_email

class CadastroCliente(tk.Toplevel):
    def __init__(self, controle):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Cadastrar Cliente")
        self.controle = controle

        self.frameNome = ttk.Frame(self)
        self.frameCpf = ttk.Frame(self)
        self.frameEndereco = ttk.Frame(self)
        self.frameEmail = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        
        self.frameNome.pack()
        self.frameCpf.pack()
        self.frameEndereco.pack()
        self.frameEmail.pack()
        self.frameButton.pack()

        self.labelNome = ttk.Label(self.frameNome, text="Nome: ")
        self.labelCpf = ttk.Label(self.frameCpf, text="CPF: ")
        self.labelEndereco = ttk.Label(self.frameEndereco, text="Endereço: ")
        self.labelEmail = ttk.Label(self.frameEmail, text="E-mail: ")
        
        self.labelNome.pack(side="left")
        self.labelCpf.pack(side="left")
        self.labelEndereco.pack(side="left") 
        self.labelEmail.pack(side="left")

        self.inputNome = ttk.Entry(self.frameNome, width=50)
        self.inputNome.pack(side="left")
        self.inputCpf = ttk.Entry(self.frameCpf, width=50)
        self.inputCpf.pack(side="left")
        self.inputEndereco = ttk.Entry(self.frameEndereco, width=50)
        self.inputEndereco.pack(side="left")
        self.inputEmail = ttk.Entry(self.frameEmail, width=50)
        self.inputEmail.pack(side="left")

        self.buttonSubmit = ttk.Button(self.frameButton, text="Salvar")
        self.buttonSubmit.pack(side="left")
        self.buttonSubmit.bind("<Button>", controle.enterHandler)

        self.buttonClear = ttk.Button(self.frameButton, text="Limpar")
        self.buttonClear.pack(side="left")
        self.buttonClear.bind("<Button>", controle.clearHandler)

        self.buttonFecha = ttk.Button(self.frameButton, text="Concluído")
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.fechaHandler)

    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)

class ConsultaCliente(tk.Toplevel):
    def __init__(self, controle, clientes):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Consultar Clientes")
        self.controle = controle

        self.frameCliente = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)

        self.frameCliente.pack()
        self.frameButton.pack()

        self.labelCliente = ttk.Label(self.frameCliente, text="Lista de Clientes: ")
        self.labelCliente.pack(side="top")

        self.textCliente = tk.Text(self.frameCliente, height=16, width=50)
        self.textCliente.pack(side="top")
        self.textCliente.insert(tk.END, clientes)

        self.buttonFecha = ttk.Button(self.frameButton, text="Concluído")
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.fechaHandler)

class alterarCliente(tk.Toplevel):
    def __init__(self ,controle, listaCliente):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Alterar Carnes")
        self.controle = controle
        self.clientes = listaCliente
        self.limite = None

        self.frameCliente = ttk.Frame(self)
        self.frameAlt = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        self.frameCliente.pack()
        self.frameAlt.pack()
        self.frameButton.pack()

        self.labelCliente = ttk.Label(self.frameCliente, text="Escolha um Cliente: ")
        self.labelCliente.pack(side="top")

        self.combo_cod = ttk.Combobox(self.frameCliente, values=[nom.nome for nom in self.clientes])
        self.combo_cod.pack()

        self.btn_selecionar = ttk.Button(self.frameButton, text="Selecionar", command=self.clienteSelecionado)
        self.btn_selecionar.pack()
    
    def clienteSelecionado(self):
        self.frame_nome = tk.Frame(self.frameAlt)
        self.frame_nome.pack(pady=(20,0))
        self.frame_cpf = tk.Frame(self.frameAlt)
        self.frame_cpf.pack(pady=(20,0))
        self.frame_ender = tk.Frame(self.frameAlt)
        self.frame_ender.pack(pady=(20,0))
        self.frame_email = tk.Frame(self.frameAlt)
        self.frame_email.pack(pady=(20,0))
        
        self.label_nome = tk.Label(self.frame_nome, text="Novo Nome: ")
        self.label_nome.pack(side="left")
        self.entry_nome = tk.Entry(self.frame_nome)
        self.entry_nome.pack()
        
        self.label_cpf = tk.Label(self.frame_cpf, text="Novo CPF: ")
        self.label_cpf.pack(side="left")
        self.entry_cpf = tk.Entry(self.frame_cpf)
        self.entry_cpf.pack()
        
        self.label_ender = tk.Label(self.frame_ender, text="Novo endereço: ")
        self.label_ender.pack(side="left")
        self.entry_ender = tk.Entry(self.frame_ender)
        self.entry_ender.pack()
        
        self.label_email = tk.Label(self.frame_email, text="Novo email: ")
        self.label_email.pack(side="left")
        self.entry_email = tk.Entry(self.frame_email)
        self.entry_email.pack()
        
        self.btn_selecionar = ttk.Button(self.frameButton, text="Concluido", command=self.att)
        self.btn_selecionar.pack()
        
    def att(self):
        nome: Any = self.combo_cod.get().strip()
        novo_nome: Any =self. entry_nome.get()
        novo_cpf: Any = self.entry_cpf.get()
        novo_ender: Any = self.entry_ender.get()
        novo_email:Any = self.entry_email.get()

        cliente_encontrado = False

        for cliente in self.clientes:
            if str(cliente.nome) == str(nome):
                cliente.atualizarCliente(novo_nome,novo_cpf, novo_ender,novo_email)
                # Adicione aqui a lógica para exibir uma mensagem de sucesso, por exemplo:
                messagebox.showinfo("Sucesso", "Cliente atualizado!")
                cliente_encontrado = True
                break

        if not cliente_encontrado:
            messagebox.showinfo("Erro", "Código não existe!")

class removerCliente(tk.Toplevel):
    def __init__(self,controle,listaCliente):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Remover Cliente")
        self.controle = controle
        self.clientes = listaCliente
        self.limite = None

        self.framecliente = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        self.framecliente.pack()
        self.frameButton.pack()

        self.labelcliente = ttk.Label(self.framecliente, text="Escolha uma cliente: ")
        self.labelcliente.pack(side="top")

        self.combo_nome = ttk.Combobox(self.framecliente, values=[nom.nome for nom in self.clientes])
        self.combo_nome.pack()

        self.btn_selecionar = ttk.Button(self.frameButton, text="Remover", command=self.clienteSelecionado)
        self.btn_selecionar.pack()
    
    def clienteSelecionado(self):
        nome = self.combo_nome.get()
        
        if nome:
            for cliente in self.clientes:
                if str(nome) == str(cliente.nome):
                    objeto = cliente
                    self.clientes.remove(objeto)
                    messagebox.showinfo("Sucesso", "Cliente removido!")
                    break        
                else :
                    messagebox.showinfo("Erro", "Cliente não encontrado!")

class CtrlCliente:
    def __init__(self, controlePrincipal):
        self.ctrlPrincipal = controlePrincipal
        self.listaClientes = []
        self.limite = None  # Inicialize a variável limite
        
        if not os.path.isfile("clientes.pickle"):
            self.listaClientes = []
        else:
            with open("clientes.pickle", "rb") as f:
                self.listaClientes = pickle.load(f)

    def salvaCliente(self):
        if len(self.listaClientes) != 0:
            with open("clientes.pickle","wb") as f:
                pickle.dump(self.listaClientes, f)
    
    def cadastrarCliente(self): 
        self.limite = CadastroCliente(self)

    def enterHandler(self, event):
        nome = str(self.limite.inputNome.get())
        cpf = str(self.limite.inputCpf.get())
        endereco = str(self.limite.inputEndereco.get())
        email = str(self.limite.inputEmail.get())

        cliente = Cliente(nome, cpf, endereco, email)

        self.listaClientes.append(cliente)

        self.limite.mostraJanela('Sucesso', 'Cliente cadastrado!')

        self.clearHandler(event)

    def clearHandler(self, event):
        self.limite.inputNome.delete(0, len(self.limite.inputNome.get()))
        self.limite.inputCpf.delete(0, len(self.limite.inputCpf.get()))
        self.limite.inputEndereco.delete(0, len(self.limite.inputEndereco.get()))
        self.limite.inputEmail.delete(0, len(self.limite.inputEmail.get()))

    def fechaHandler(self, event):
        self.limite.destroy()

    def consultarCliente(self): 
        if len(self.listaClientes) == 0:
            messagebox.showinfo('Falha', 'Não existem clientes cadastrados!')
        else:
            clientes = ''

            for cliente in self.listaClientes:
                clientes += cliente.getCliente() + "\n"

            self.limite = ConsultaCliente(self, clientes)
            
    def getListaCliente(self):
        return self.listaClientes

    def adicionarNovoCliente(self, nome, cpf, endereco, email):
        cliente = Cliente(nome, cpf, endereco, email)
        self.listaClientes.append(cliente)
        return cliente
    
    def consultarClienteCPF(self):
        cpf = simpledialog.askstring("Consultar CPF", "Digite o CPF do Cliente:")
        listaCliente = self.getListaCliente()
        chec = 0
        if cpf:
            for cl in listaCliente:
                if cpf == cl.cpf:
                    messagebox.showinfo("Sucesso", "Cliente encontrado! \n\nNome: {} \nEndereço: {} \nE-mail: {}".format(cl.nome, cl.endereco, cl.email))
                    chec = 1 
            if chec == 0:
                messagebox.showinfo("Erro", "CPF não encontrado!")

        else:
            messagebox.showinfo('Falha', 'Número de CPF inválido!')
            
    def alterarCliente(self):
        return alterarCliente(self,self.listaClientes)
    
    def removerCliente(self):
        return removerCliente(self,self.listaClientes)
