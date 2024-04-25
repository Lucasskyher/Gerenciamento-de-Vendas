import tkinter as tk
from tkinter import PhotoImage
import carne as cn  # Certifique-se de que o módulo 'carne' esteja corretamente importado
import cliente as cl  # Importe o módulo 'cliente' ou o módulo correto
import vendas as vn

class TelaPrincipal:
    def __init__(self, root, controle):
        self.controle = controle
        self.root = root
        self.root.geometry('960x540')
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=960, height=540)
        self.canvas.pack()

        self.menubar = tk.Menu(self.root)
        
        self.menuCadastro = tk.Menu(self.menubar)
        self.menuConsulta = tk.Menu(self.menubar)
        self.menuAlterar = tk.Menu(self.menubar)
        self.menuRemover = tk.Menu(self.menubar)
        self.menuVendas = tk.Menu(self.menubar)

        self.menuCadastro.add_command(label="Cadastrar Carnes", command=self.controle.cadastrarCarne)
        self.menuCadastro.add_command(label="Cadastrar Clientes", command=self.controle.cadastrarClientes)  # Corrigido
        self.menubar.add_cascade(label="CADASTROS", menu=self.menuCadastro)

        self.menuConsulta.add_command(label="Consultar Carnes", command=self.controle.consultarCarne)
        self.menuConsulta.add_command(label="Consultar Clientes", command=self.controle.consultarClientes)  # Corrigido
        self.menuConsulta.add_command(label="Consultar Cliente com CPF", command=self.controle.consultarClienteCPF)
        self.menuConsulta.add_command(label="Consultar Produto com Código", command=self.controle.consultarProdutoCod)
        self.menuConsulta.add_command(label="Consultar Faturamento por Produto", command=self.controle.consultarFaturamentoProd)
        self.menuConsulta.add_command(label="Consultar Faturamento por Cliente",command=self.controle.consultarFaturamentoCliente)
        self.menuConsulta.add_command(label="Consultar Faturamento por Período",command=self.controle.consultarPeriodo)
        self.menuConsulta.add_command(label="Consultar Faturamento por Período de Cliente",command=self.controle.consultarPeriodoCliente)
        self.menubar.add_cascade(label="CONSULTAS", menu=self.menuConsulta)

        self.menuVendas.add_command(label="Emitir Nota Fiscal", command=self.controle.emitirNota)
        self.menuVendas.add_command(label="Exibir Nota Fiscal", command=self.controle.exibirNota)
        self.menuVendas.add_command(label="Exibir Maiores vendas", command=self.controle.maioresVendas)
        self.menubar.add_cascade(label="VENDAS", menu=self.menuVendas)

        self.menuAlterar.add_command(label="Alterar Informações Carnes", command=self.controle.alterarCarne)  # Alterado para 'alterarCarne'
        self.menuAlterar.add_command(label="Alterar Informações Clientes", command=self.controle.alterarCliente)  # Adicionado
        self.menubar.add_cascade(label="ALTERAR", menu=self.menuAlterar)

        self.menuRemover.add_command(label="Remover Carnes", command=self.controle.removerCarne)  # Alterado para 'removerCarne'
        self.menuRemover.add_command(label="Remover Clientes", command=self.controle.removerCliente)  # Adicionado
        self.menubar.add_cascade(label="REMOVER", menu=self.menuRemover)

        self.root.config(menu=self.menubar)

class Iniciar:
    def __init__(self):
        self.root = tk.Tk()
        self.CtrlCarne = cn.CtrlCarne(self)
        self.CtrlCliente = cl.CtrlCliente(self)  # Adicionado
        self.CtrlVendas = vn.CtrlVendas(self)
        self.tela = TelaPrincipal(self.root, self)
        self.root.title("Açougue Alquimia da Carne")
        self.root.mainloop()
        
        self.CtrlCliente.salvaCliente()
        self.CtrlCarne.salvaCarne()
        self.CtrlVendas.salvaVendas()
        self.CtrlVendas.salvaNotas()

    def cadastrarCarne(self):
        self.CtrlCarne.cadastrarCarne()

    def consultarCarne(self):
        self.CtrlCarne.consultarCarne()

    def cadastrarClientes(self):
        self.CtrlCliente.cadastrarCliente()

    def consultarClientes(self):
        self.CtrlCliente.consultarCliente()

    def alterarCarne(self):  # Adicionado
       self.CtrlCarne.alterarCarne()

    def alterarCliente(self):  # Adicionado
        self.CtrlCliente.alterarCliente()

    def removerCarne(self):  # Adicionado
        self.CtrlCarne.removerCarne()

    def removerCliente(self):  # Adicionado
        self.CtrlCliente.removerCliente()
    
    def emitirNota(self):
        self.CtrlVendas.emitirNota()

    def exibirNota(self):
        self.CtrlVendas.exibirNota()

    def consultarClienteCPF(self):
        self.CtrlCliente.consultarClienteCPF()

    def consultarProdutoCod(self):
        self.CtrlCarne.consultarProdutoCod()

    def consultarFaturamentoProd(self):
        self.CtrlVendas.consultarFaturamentoProd()

    def consultarFaturamentoCliente(self):
        self.CtrlVendas.consultarFaturamentoCliente()
        
    def consultarPeriodo(self):
        self.CtrlVendas.consultarPeriodo()
        
    def consultarPeriodoCliente(self):
        self.CtrlVendas.consultarPeriodoCliente()
    
    def maioresVendas(self):
        self.CtrlVendas.maioresVendas()

if __name__ == '__main__':
    c = Iniciar()
