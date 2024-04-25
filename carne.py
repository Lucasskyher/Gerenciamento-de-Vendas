import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os.path
import pickle
from tkinter import simpledialog
from typing import Any

class Carne:
    def __init__(self, codigo, descricao, preco):
        self.__codigo = codigo
        self.__descricao = descricao
        self.__preco = preco

    @property
    def codigo(self):
        return self.__codigo

    @property
    def descricao(self):
        return self.__descricao
    
    @property
    def preco(self):
        return self.__preco

    def getCarne(self):
        return f"Código: {self.__codigo}\nDescrição: {self.__descricao}\nPreço por kilo: R${self.__preco}\n\n--+--+--+--+--+--+--+--+--\n"

    def atualizarCarne(self, novo_codigo,nova_descricao, novo_preco):
        self.__codigo = novo_codigo
        self.__descricao = nova_descricao
        self.__preco = novo_preco

class CadastroCarne(tk.Toplevel):
    def __init__(self, controle):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Cadastrar Carne")
        self.controle = controle
        self.limite = None  # Inicialize a variável limite

        self.frameCodigo = ttk.Frame(self)
        self.frameDescricao = ttk.Frame(self)
        self.framePreco = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        
        self.frameCodigo.pack()
        self.frameDescricao.pack()
        self.framePreco.pack()
        self.frameButton.pack()

        self.labelCodigo = ttk.Label(self.frameCodigo, text="Código: ")
        self.labelDescricao = ttk.Label(self.frameDescricao, text="Descrição: ")
        self.labelPreco = ttk.Label(self.framePreco, text="Preço: ")
        
        self.labelCodigo.pack(side="left")
        self.labelDescricao.pack(side="left")
        self.labelPreco.pack(side="left") 

        self.inputCodigo = ttk.Entry(self.frameCodigo, width=50)
        self.inputCodigo.pack(side="left")
        self.inputDescricao = ttk.Entry(self.frameDescricao, width=50)
        self.inputDescricao.pack(side="left")
        self.inputPreco = ttk.Entry(self.framePreco, width=50)
        self.inputPreco.pack(side="left")

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

class ConsultaCarne(tk.Toplevel):
    def __init__(self, controle, carnes):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Consultar Carnes")
        self.controle = controle
        self.limite = None 

        self.frameCarne = ttk.Frame(self)
        
        self.frameButton = ttk.Frame(self)

        self.frameCarne.pack()
        
        self.frameButton.pack()

        self.labelCarne = ttk.Label(self.frameCarne, text="Lista de Carnes: ")
        self.labelCarne.pack(side="top")

        self.textCarne = tk.Text(self.frameCarne, height=16, width=50)
        self.textCarne.pack(side="top")
        self.textCarne.insert(tk.END, carnes)

        self.buttonFecha = ttk.Button(self.frameButton, text="Concluído")
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.fechaHandler)

class alterarCarne(tk.Toplevel):
    def __init__(self ,controle, listaCarne):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Alterar Carnes")
        self.controle = controle
        self.carnes = listaCarne
        self.limite = None

        self.frameCarne = ttk.Frame(self)
        self.frameAlt = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        self.frameCarne.pack()
        self.frameAlt.pack()
        self.frameButton.pack()

        self.labelCarne = ttk.Label(self.frameCarne, text="Escolha uma Carne: ")
        self.labelCarne.pack(side="top")

        self.combo_cod = ttk.Combobox(self.frameCarne, values=[cod.codigo for cod in self.carnes])
        self.combo_cod.pack()

        self.btn_selecionar = ttk.Button(self.frameButton, text="Selecionar", command=self.carneSelecionada)
        self.btn_selecionar.pack()
    
    def carneSelecionada(self):
        self.frame_cod = tk.Frame(self.frameAlt)
        self.frame_cod.pack(pady=(20,0))
        self.frame_desc = tk.Frame(self.frameAlt)
        self.frame_desc.pack(pady=(20,0))
        self.frame_preco = tk.Frame(self.frameAlt)
        self.frame_preco.pack(pady=(20,0))
        
        self.label_cod = tk.Label(self.frame_cod, text="Nova codigo: ")
        self.label_cod.pack(side="left")
        self.entry_cod = tk.Entry(self.frame_cod)
        self.entry_cod.pack()
        
        self.label_desc = tk.Label(self.frame_desc, text="Nova Descrição: ")
        self.label_desc.pack(side="left")
        self.entry_desc = tk.Entry(self.frame_desc)
        self.entry_desc.pack()
        
        self.label_preco = tk.Label(self.frame_preco, text="Novo Preco: ")
        self.label_preco.pack(side="left")
        self.entry_preco = tk.Entry(self.frame_preco)
        self.entry_preco.pack()
        
        self.btn_selecionar = ttk.Button(self.frameButton, text="Concluido", command=self.att)
        self.btn_selecionar.pack()
        
    def att(self):
        cod: Any = self.combo_cod.get()
        novo_codigo: Any =self. entry_cod.get()
        nova_descricao: Any = self.entry_desc.get()
        novo_preco: Any = self.entry_preco.get()

        carne_encontrada = False

        for carne in self.carnes:
            if int(carne.codigo) == int(cod):
                carne.atualizarCarne(novo_codigo,nova_descricao, novo_preco)
                # Adicione aqui a lógica para exibir uma mensagem de sucesso, por exemplo:
                messagebox.showinfo("Sucesso", "Carne atualizada!")
                carne_encontrada = True
                break

        if not carne_encontrada:
            messagebox.showinfo("Erro", "Produto não existe!")
            
class removerCarne(tk.Toplevel):
    def __init__(self,controle,listaCarne):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Alterar Carnes")
        self.controle = controle
        self.carnes = listaCarne
        self.limite = None

        self.frameCarne = ttk.Frame(self)
        self.frameAlt = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        self.frameCarne.pack()
        self.frameAlt.pack()
        self.frameButton.pack()

        self.labelCarne = ttk.Label(self.frameCarne, text="Escolha uma Carne: ")
        self.labelCarne.pack(side="top")

        self.combo_cod = ttk.Combobox(self.frameCarne, values=[cod.codigo for cod in self.carnes])
        self.combo_cod.pack()

        self.btn_selecionar = ttk.Button(self.frameButton, text="Remover", command=self.carneSelecionada)
        self.btn_selecionar.pack()
    
    def carneSelecionada(self):
        cod = self.combo_cod.get()
        carneEncontrada = False
        if cod:
            for carne in self.carnes:
                if str(cod) == str(carne.codigo):
                    objeto = carne
                    self.carnes.remove(objeto)
                    carneEncontrada = True
                    break        
            if carneEncontrada == True:
                messagebox.showinfo("Sucesso", "Carne removida!")
            else :
                messagebox.showinfo("Erro", "Carne não encontrada!")
        
class CtrlCarne:
    def __init__(self, controlePrincipal):
        self.ctrlPrincipal = controlePrincipal
        self.listaCarnes = []
        self.limite = None  # Inicialize a variável limite
        if not os.path.isfile("carnes.pickle"):
            self.listaCarnes = []
        else:
            with open("carnes.pickle", "rb") as f:
                self.listaCarnes = pickle.load(f)

    ##Cadastro
    def salvaCarne(self):
        if len(self.listaCarnes) != 0:
            with open("carnes.pickle","wb") as f:
                pickle.dump(self.listaCarnes, f)

    def cadastrarCarne(self): 
        self.limite = CadastroCarne(self)    
    
    def enterHandler(self, event):
        codigo = int(self.limite.inputCodigo.get())
        descricao = str(self.limite.inputDescricao.get())
        preco = float(self.limite.inputPreco.get())

        listaCarne = self.listaCarnes

        chec = 0
        
        for carne in listaCarne:
            if carne.codigo == codigo:
                chec = 1

        if chec == 0:
            Cn = Carne(codigo, descricao, preco)

            self.listaCarnes.append(Cn)

            self.limite.mostraJanela('Sucesso', 'Carne cadastrada!')
        else:
            self.limite.mostraJanela('Erro', 'Código já existente!')

        self.clearHandler(event)
    ##
    ##Limpar Inupts.
    def clearHandler(self, event):
        self.limite.inputCodigo.delete(0, len(self.limite.inputCodigo.get()))
        self.limite.inputDescricao.delete(0, len(self.limite.inputDescricao.get()))
        self.limite.inputPreco.delete(0, len(self.limite.inputPreco.get()))

    def fechaHandler(self, event=None):
        self.limite.destroy()
    ##
    ##Consulta
    def consultarCarne(self): 
        if len(self.listaCarnes) == 0:
            messagebox.showinfo('Falha', 'Não existem carnes cadastradas!')
        else:
            carnes = ''
            for carne in self.listaCarnes:
                carnes += carne.getCarne() + "\n"
            self.limite = ConsultaCarne(self, carnes)
    ##
    ##Gets
    def getListaCodigosCarne(self):
        return [carne.codigo for carne in self.listaCarnes]
    
    def getListaProdutos(self):
        return self.listaCarnes
    ##
    ##Consultas
    def consultarProdutoCod(self):
        codigo = simpledialog.askstring("Consultar Produto", "Digite o código do Produto:")
        listaCarnes = self.getListaProdutos()
        chec = 0
        if codigo:
            codigo = int(codigo)
            for prod in listaCarnes:
                if codigo == prod.codigo:
                    messagebox.showinfo("Sucesso", "Produto encontrado! \n\nDescrição: {} \nPreço por quilo: R${:.2f}".format(prod.descricao, prod.preco))
                    chec = 1 
            if chec == 0:
                messagebox.showinfo("Erro", "Código não encontrado!")

        else:
            messagebox.showinfo('Falha', 'Número de código inválido!')
    ##
    ##Alterar
    def alterarCarne(self):
        
        return alterarCarne(self,self.listaCarnes)
                
    ##
    ##Remoção
    def removerCarne(self):
        
        return removerCarne(self,self.listaCarnes)
    ##
    
    def getCarne(self):
        return self.Carne.getCarne()