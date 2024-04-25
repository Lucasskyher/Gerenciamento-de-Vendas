import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import os.path
import pickle
import cliente as cliente
import carne as carne
import random
from tkcalendar import DateEntry
from datetime import date


class Vendas:
    def __init__(self, cliente, produtos, numNota, valorNota, data):
        self.__cliente = cliente
        self.__produtos = produtos
        self.__numNota = numNota
        self.__valorNota = valorNota
        self.__data = data

    @property
    def cliente(self):
        return self.__cliente

    @property
    def produtos(self):
        return self.__produtos

    @property
    def numNota(self):
        return self.__numNota

    @property
    def valorNota(self):
        return self.__valorNota
    
    @property
    def data(self):
        return self.__data
    
    def getVenda(self):
        return f"Cliente: {self.__cliente}\nProdutos: {self.__produtos}\nNumero da Nota: {self.__numNota}\nValor da Nota: {self.__valorNota}\nData: {self.__data}\n\n--+--+--+--+--+--+--+--+--\n"


class Nota(Vendas):
    def __init__(self, quantidade, descricao, valorTotal:float):
        self.__quantidade = quantidade
        self.__descricao = descricao
        self.__valorTotal = valorTotal

    @property
    def quantidade(self):
        return self.__quantidade

    @property
    def descricao(self):
        return self.__descricao

    @property
    def valorTotal(self):
        return self.__valorTotal

class EmitirNota(tk.Toplevel):
    def __init__(self, controle):
        tk.Toplevel.__init__(self)

        self.geometry('300x150')
        self.title("Adicionar Produtos")
        self.controle = controle

        self.frameCodigo= tk.Frame(self)
        self.frameQuant = tk.Frame(self)
        self.frameData = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        self.frameCodigo.pack()
        self.frameQuant.pack()
        self.frameData.pack()
        self.frameButton.pack()
        

        self.labelCodigo = tk.Label(self.frameCodigo,text="Informe o código do produto: ")
        self.labelCodigo.pack(side="left")
        self.inputCodigo = tk.Entry(self.frameCodigo, width=15)
        self.inputCodigo.pack(side="left")

        self.labelQuant = tk.Label(self.frameQuant,text="Quantidade vendida (KG): ")
        self.labelQuant.pack(side="left")
        self.inputQuant = tk.Entry(self.frameQuant, width=15)
        self.inputQuant.pack(side="left")
        
        self.labelDataIn = tk.Label(self.frameData,text="Data da Emissão: ")
        self.labelDataIn.pack(side = "left")
        self.frameData = DateEntry(self.frameData, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.frameData.pack()

        self.buttonSubmit = tk.Button(self.frameButton, text="Adicionar produto")    
        self.buttonSubmit.pack(side="left")
        self.buttonSubmit.bind("<Button>", controle.adicionaProduto)

        self.buttonSubmit = tk.Button(self.frameButton, text="Emitir Nota")    
        self.buttonSubmit.pack(side="left")
        self.buttonSubmit.bind("<Button>", controle.emiteNota)

        self.buttonSubmit = tk.Button(self.frameButton, text="Cancelar Emissão")    
        self.buttonSubmit.pack(side="left")
        self.buttonSubmit.bind("<Button>", controle.cancelaNota)


class ExibirNota(tk.Toplevel):
    def __init__(self, controle, venda_encontrada):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Exibir Notas")
        self.controle = controle

        self.frameNota = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)

        self.frameNota.pack()
        self.frameButton.pack()

        self.labelNota = ttk.Label(self.frameNota, text="Nota correspondente: ")
        self.labelNota.pack(side="top")

        # Mostra o número da nota
        self.textNota = tk.Text(self.frameNota, height=16, width=50)
        self.textNota.pack(side="top")
        self.textNota.insert(tk.END, f"Número da Nota: {venda_encontrada.numNota}\n")
        self.textNota.insert(tk.END, f"\nData: {venda_encontrada.data}\n")

        # Mostra as informações do cliente (CPF e nome)
        self.textNota.insert(tk.END, f"CPF: {venda_encontrada.cliente.cpf}\n")
        self.textNota.insert(tk.END, f"Nome: {venda_encontrada.cliente.nome}\n")

        # Mostra os detalhes dos itens da nota (quantidade, descrição, valor do item)
        self.textNota.insert(tk.END, "Itens da Nota:\n")
        valor_total_nota = 0

        for item in venda_encontrada.produtos:
            valor_total_nota += item.valorTotal
            info_item = f"Quantidade: {item.quantidade} KG \nDescrição: {item.descricao} \nValor do Item: R${item.valorTotal:.2f}\n"
            self.textNota.insert(tk.END, info_item)

        # Mostra o valor total da nota
        self.textNota.insert(tk.END, f"\nValor Total da Nota: R${valor_total_nota:.2f}\n")

        self.buttonFecha = ttk.Button(self.frameButton, text="Concluído")
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.fechaHandler)

class ConsultarPeriodo(tk.Toplevel):
    
    def __init__(self,controle,listaVendas):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Faturamento por período")
        self.controle = controle
        self.vendas = listaVendas
        self.limite = None

        self.frameIncial = ttk.Frame(self)
        self.frameFinal = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        
        self.frameData = ttk.Frame(self)
        self.frameFat = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        
        self.frameIncial.pack()
        self.frameFinal.pack()
        self.frameData.pack()
        self.frameFat.pack()
        self.frameButton.pack()
        
        self.dataInicial = None
        self.dataFinal = None
        
        self.labelDataIn = tk.Label(self.frameIncial,text="Data Inicial: ")
        self.labelDataIn.pack(side = "left")
        self.dataInicial = DateEntry(self.frameIncial, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.dataInicial.pack()
        self.labelDataFim = tk.Label(self.frameFinal,text="Data Final: ")
        self.labelDataFim.pack(side = "left")
        self.dataFinal = DateEntry(self.frameFinal, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.dataFinal.pack()
        
        self.btn_selecionar = ttk.Button(self.frameButton, text="Selecionar", command=self.ExibirPeriodo)
        self.btn_selecionar.pack()
        
        self.buttonFecha = ttk.Button(self.frameButton, text="Concluído")
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.fechaHandler)
        
    def ExibirPeriodo (self):
        self.dataIn = self.dataInicial.get_date()
        self.dataFim = self.dataFinal.get_date()
        faturamento_total = 0

        for venda in self.vendas:
            for item in venda.produtos:
                if isinstance(venda.data, datetime.date) and isinstance(self.dataIn, datetime.date) and isinstance(self.dataFim, datetime.date) and self.dataIn <= venda.data <= self.dataFim:
                    faturamento_total += item.valorTotal
           
        self.labelData = ttk.Label(self.frameData, text="Data: ")
        self.labelData.pack(side="top")

        # Mostra o número da Data
        self.textData = tk.Text(self.frameData, height=16, width=50)
        self.textData.pack(side="top")
        self.textData.insert(tk.END, f"Data Inicial: {self.dataIn}\n")
        self.textData.insert(tk.END, f"\nData Final: {self.dataFim}\n")
        self.textData.insert(tk.END, f"Faturamento no período: R${faturamento_total}\n")
        
class ConsultarPeriodoCliente(tk.Toplevel):
    
    def __init__(self,controle,cliente,listaVendas):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Faturamento do Cliente por período")
        self.controle = controle
        self.vendas = listaVendas
        self.cliente = cliente
        self.limite = None

        self.frameIncial = ttk.Frame(self)
        self.frameFinal = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        
        self.frameData = ttk.Frame(self)
        self.frameFat = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        
        self.frameIncial.pack()
        self.frameFinal.pack()
        self.frameData.pack()
        self.frameFat.pack()
        self.frameButton.pack()
        
        self.dataInicial = None
        self.dataFinal = None
        
        self.labelDataIn = tk.Label(self.frameIncial,text="Data Inicial: ")
        self.labelDataIn.pack(side = "left")
        self.dataInicial = DateEntry(self.frameIncial, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.dataInicial.pack()
        self.labelDataFim = tk.Label(self.frameFinal,text="Data Final: ")
        self.labelDataFim.pack(side = "left")
        self.dataFinal = DateEntry(self.frameFinal, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.dataFinal.pack()
        
        self.btn_selecionar = ttk.Button(self.frameButton, text="Selecionar", command=self.ExibirPeriodo)
        self.btn_selecionar.pack()
        
        self.buttonFecha = ttk.Button(self.frameButton, text="Concluído")
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.fechaHandler)
        
    def ExibirPeriodo (self):
        self.dataIn = self.dataInicial.get_date()
        self.dataFim = self.dataFinal.get_date()
        faturamento_total = 0

        for venda in self.vendas:
            if venda.cliente.cpf == self.cliente:
                for item in venda.produtos:
                    if isinstance(venda.data, datetime.date) and isinstance(self.dataIn, datetime.date) and isinstance(self.dataFim, datetime.date) and self.dataIn <= venda.data <= self.dataFim:
                        faturamento_total += item.valorTotal
           
        self.labelData = ttk.Label(self.frameData, text="Data: ")
        self.labelData.pack(side="top")

        # Mostra o número da Data
        self.textData = tk.Text(self.frameData, height=16, width=50)
        self.textData.pack(side="top")
        self.textData.insert(tk.END, f"Data Inicial: {self.dataIn}\n")
        self.textData.insert(tk.END, f"\nData Final: {self.dataFim}\n")
        self.textData.insert(tk.END, f"Faturamento no período do cliente: R${faturamento_total}\n")

class MaioresVendas(tk.Toplevel):
    def __init__(self, controle, listaVendas):
        tk.Toplevel.__init__(self)
        self.geometry('640x360')
        self.title("Maiores Vendas")
        self.controle = controle
        self.vendas = listaVendas
        
        self.frameVenda = ttk.Frame(self)
        self.frameButton = ttk.Frame(self)
        self.frameVenda.pack()
        self.frameButton.pack()
    
        self.labelVenda = ttk.Label(self.frameVenda, text="Maiores Vendas: ")
        self.labelVenda.pack(side="top")

        self.textVenda = tk.Text(self.frameVenda, height=16, width=50)
        self.textVenda.pack(side="top")
        self.textVenda.insert(tk.END, self.vendas)

        self.buttonFecha = ttk.Button(self.frameButton, text="Concluído")
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.fechaHandler)

class CtrlVendas():
    def __init__(self, controlePrincipal):
        self.ctrlPrincipal = controlePrincipal
        self.listaCliente = []
        self.listaProdutos = []
        self.listaAddProd = []
        self.clienteAtual = None
        self.valorFat = None

        if not os.path.isfile("vendas.pickle"):
            self.listaVendas = []
        else:
            with open("vendas.pickle", "rb") as f:
                self.listaVendas = pickle.load(f)
        
        if not os.path.isfile("notas.pickle"):
            self.listaNotas = []
        else:
            with open("notas.pickle", "rb") as f:
                self.listaNotas = pickle.load(f)

    def salvaVendas(self):
        if len(self.listaVendas) != 0:
            with open("vendas.pickle", "wb") as f:
                pickle.dump(self.listaVendas, f)
    
    def salvaNotas(self):
        if len(self.listaNotas) != 0:
            with open("notas.pickle", "wb") as f:
                pickle.dump(self.listaNotas, f)
    

    def emitirNota(self):
        self.listaCliente = self.ctrlPrincipal.CtrlCliente.getListaCliente()

        cpf = simpledialog.askstring("Consultar CPF", "Digite o CPF do Cliente:")

        chec = 0

        if cpf:
            for cl in self.listaCliente:
                if cpf == cl.cpf:
                    self.clienteAtual = cl
                    chec = 1 
                    messagebox.showinfo("CPF já Cadastrado", "Cliente {} já está cadastrado!".format(cl.nome))
                    self.limiteEm = EmitirNota(self)
                    break

            if chec == 0:
                messagebox.showinfo("Erro", "CPF não encontrado! Cadastre o cliente.")
                nome = simpledialog.askstring("Cadastrar Novo Cliente", "Digite o Nome do Cliente:")
                endereco = simpledialog.askstring("Cadastrar Novo Cliente", "Digite o Endereço do Cliente:")
                email = simpledialog.askstring("Cadastrar Novo Cliente", "Digite o E-mail do Cliente:")
                if nome:
                    if endereco:
                        if email:
                            self.clienteAtual = self.ctrlPrincipal.CtrlCliente.adicionarNovoCliente(nome, cpf, endereco, email)
                            messagebox.showinfo("Sucesso", "Cliente {} cadastrado com Sucesso".format(nome)) 
                            self.limiteEm = EmitirNota(self)
                        else:
                            messagebox.showinfo('Falha', 'Erro na criação do cliente!')
                    else:
                        messagebox.showinfo('Falha', 'Erro na criação do cliente!')
                else:
                    messagebox.showinfo('Falha', 'Erro na criação do cliente!')
        else:
            messagebox.showinfo('Falha', 'Número de CPF inválido!')



    def adicionaProduto(self, event):
        self.listaProdutos = self.ctrlPrincipal.CtrlCarne.getListaProdutos()
        Codigo = int(self.limiteEm.inputCodigo.get())
        Quant = float(self.limiteEm.inputQuant.get())


        chec = 0

        tamanho = len(self.listaAddProd)

        for cn in self.listaProdutos:
            if Codigo == cn.codigo:
                if tamanho <= 9:
                    valor = cn.preco * Quant
                    nota = Nota(Quant, cn.descricao, valor)
                    self.listaAddProd.append(nota)
                    self.listaNotas.append(nota)
                    messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!\nDescrição: {} \nPreço: R${:.2f}" .format(cn.descricao, cn.preco))  
                    chec = 1
                else:
                    messagebox.showinfo("Erro", "Limite de produtos da nota alcançado.")
                    chec = 2

        if chec == 0:
            messagebox.showinfo("Erro", "Código de produto inválido!")


    def emiteNota(self, event):
        numNota = random.randint(1,10000)
        valor = 0
        for prod in self.listaAddProd:
            valor += prod.valorTotal

        data_atual = self.limiteEm.frameData.get_date()

        vendas = Vendas(self.clienteAtual, self.listaAddProd, numNota, valor, data_atual)
        self.listaVendas.append(vendas)
        messagebox.showinfo("Sucesso", "Nota Emitida com Sucesso\nNúmero identificador: {}\nValor Total: R${:.2f}\nData de emissão: {}".format(numNota, valor, data_atual))

        self.listaAddProd = []
        self.limiteEm.destroy()

    def cancelaNota(self, event):
        self.listaAddProd = []
        self.limiteEm.destroy()

    def exibirNota(self): 

        if len(self.listaVendas) == 0:
            messagebox.showinfo('Falha', 'Não existem notas cadastradas!')
        else:
            vendas_encontrada = None
            numNota = simpledialog.askstring("Exibir Nota", "Informe o número da nota:")
            if numNota:
                numNota = int(numNota)
                for venda in self.listaVendas:
                    if numNota == venda.numNota:
                        vendas_encontrada = venda
                        break  

                if vendas_encontrada:
                    self.limiteEx = ExibirNota(self, vendas_encontrada) 
                else:
                    messagebox.showinfo('Falha', 'Número da nota inválido!')
            else:
                messagebox.showinfo('Falha', 'Número da nota inválido!')


    def fechaHandler(self, event):
        self.limiteEx.destroy()

    def consultarFaturamentoProd(self):
        codigo = simpledialog.askstring("Consultar Produto", "Digite o código do Produto:")
        listaProdutos = self.ctrlPrincipal.CtrlCarne.getListaProdutos()
        Descricao = None
        faturamento_total = 0
        chec = 0
        if codigo:
            codigo = int(codigo)

            for prod in listaProdutos:
                if codigo == prod.codigo:
                    Descricao = prod.descricao
                    chec = 1
                    for venda in self.listaVendas:
                        for item in venda.produtos:
                            if item.descricao == Descricao:
                                faturamento_total += item.valorTotal
                                
                    messagebox.showinfo("Código Encontrado", "Faturamento total do produto {}: R${:.2f}".format(Descricao, faturamento_total))
            if chec == 0:
                messagebox.showinfo("Erro", "Código não encontrado!")

        else:
            messagebox.showinfo('Falha', 'Número de código inválido!')

    def consultarPeriodo(self):
         
        self.limiteEx = ConsultarPeriodo(self,self.listaVendas)
        
    def consultarPeriodoCliente(self):
        
        cpf = simpledialog.askstring("Consultar CPF", "Digite o CPF do Cliente:")
        listaCliente = self.ctrlPrincipal.CtrlCliente.getListaCliente()
        chec = 0
        if cpf:
            for cl in listaCliente:
                if cpf == cl.cpf:
                    messagebox.showinfo("Sucesso", "Cliente encontrado! \nNome: {} \n".format(cl.nome))
                    chec = 1 
                    self.limiteEx = ConsultarPeriodoCliente(self,cpf,self.listaVendas)
            if chec == 0:
                messagebox.showinfo("Erro", "CPF não encontrado!")

        else:
            messagebox.showinfo('Falha', 'Número de CPF inválido!')
        

    def consultarFaturamentoCliente(self):
        cpf = simpledialog.askstring("Consultar Produto", "Digite o CPF do Cliente:")
        if cpf:
            try:
                faturamento_total = 0
                cliente_encontrado = False

                for venda in self.listaVendas:
                    if cpf == venda.cliente.cpf:
                        cliente_encontrado = True
                        faturamento_total += venda.valorNota
                        Nome = venda.cliente.nome

                if cliente_encontrado:
                    messagebox.showinfo("Código Encontrado", f"Faturamento total do(a) cliente {Nome}: R${faturamento_total:.2f}")
                else:
                    messagebox.showinfo("Erro", "CPF não encontrado!")

            except ValueError:
                messagebox.showinfo('Falha', 'Número de CPF inválido!')
        else:
            messagebox.showinfo('Falha', 'Número de CPF inválido!')
            
    def maioresVendas(self):
        if len (self.listaVendas) == 0 :
            messagebox.showinfo('Falha', 'Não existem vendas cadastradas!')
        else:
            
            listaCarnes = self.ctrlPrincipal.CtrlCarne.getListaProdutos()
            listaProd = self.listaNotas
            Descricao = None
            faturamento_total = 0
            faturamento_por_produto = {}
            maioresProd = []
            quantProd = {}
            produtosFinais = ""
            
            ##ORDENA POR FATURAMENTO
            
            for prod in listaCarnes:
                    Descricao = prod.descricao
                    faturamento_total = 0
                    
                    for venda in self.listaVendas:
                        for item in venda.produtos:
                            if item.descricao == Descricao:
                                faturamento_total += item.valorTotal
                    
                    faturamento_por_produto[Descricao] = faturamento_total
            
            
            produtos_ordenados = sorted(faturamento_por_produto.items(), key = lambda x: x[1], reverse = True)
            
                                
            for prod in produtos_ordenados:
                Descricao=prod[0]
                for item in listaCarnes:
                    if Descricao == item.descricao:
                        maioresProd.append(item)
                        for nota in listaProd:
                            if nota.descricao == Descricao:
                                quantProd[Descricao]=nota.quantidade
            
            top_5_produtos = maioresProd[:5]
            # for prod in listaProdutos:
            #     Descricao = prod.descricao
            for item in top_5_produtos:
                quantidade = quantProd.get(item.descricao, 0)
                # print('\n'+ str(quantidade))
                produtosFinais += 'Dados do produto: \n' +item.getCarne() +"Faturamento: \n"+ 'R$: '+ str(faturamento_por_produto[item.descricao]) + '\n' + 'Quantidade: '+str(quantidade) + '\n<<<<<------------------->>>>>\n\n' ## falta a qauntidade vendida getCarne(prod)
                    
            self.limiteEx =  MaioresVendas(self,produtosFinais)
            
            