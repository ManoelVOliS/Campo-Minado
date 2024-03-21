import tkinter as tk
import random

class CampoMinado:
    def __init__(self, master, tamanhoMapa, probabilidade) -> None:
        self.master = master
        self.tamanhoMapa = tamanhoMapa
        self.probabilidade = probabilidade
        self.vidas = 3
        self.blocos_percorridos = 0
        self.mapa = [[self.gerar_elemento() for _ in range(tamanhoMapa)] for _ in range(tamanhoMapa)]

        self.carroX = 0
        self.carroY = 0
        self.mapa[self.carroY][self.carroX] = 'carro'

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=30*self.tamanhoMapa, height=30*self.tamanhoMapa, bg="gray")
        self.canvas.pack(side=tk.LEFT)  # Posiciona o canvas à esquerda

        # Adiciona uma frame para a tabela de informações
        self.info_frame = tk.Frame(self.master)
        self.info_frame.pack(side=tk.RIGHT)  # Posiciona a frame à direita

        # Adiciona labels para exibir as informações
        tk.Label(self.info_frame, text="Blocos Percorridos:").pack()
        self.label_blocos_percorridos = tk.Label(self.info_frame, text=str(self.blocos_percorridos))
        self.label_blocos_percorridos.pack()

        tk.Label(self.info_frame, text="Vidas:").pack()
        self.label_vidas = tk.Label(self.info_frame, text=str(self.vidas))
        self.label_vidas.pack()

        self.desenharMapa()

    def gerar_elemento(self):
        if random.random() < self.probabilidade:
            return 1
        elif random.random() < 0.1:
            return 'vida_verde'
        else:
            return 0

    def desenharMapa(self):
        self.canvas.delete("all")
        for y in range(self.tamanhoMapa):
            for x in range(self.tamanhoMapa):
                cor = "white"
                if self.mapa[y][x] == 'carro':
                    cor = "blue"
                elif self.mapa[y][x] == 1:
                    cor = "red"
                    self.canvas.create_rectangle(x*30+10, y*30+10, (x+1)*30-10, (y+1)*30-10, fill="black")
                elif self.mapa[y][x] == 'vida_verde':
                    cor = "green"
                    self.canvas.create_rectangle(x*30+10, y*30+10, (x+1)*30-10, (y+1)*30-10, fill="green")
                self.canvas.create_rectangle(x*30, y*30, (x+1)*30, (y+1)*30, fill=cor)

    def moverCarro(self, dx, dy):
        newX = self.carroX + dx
        newY = self.carroY + dy
        if 0 <= newX < self.tamanhoMapa and 0 <= newY < self.tamanhoMapa:
            self.mapa[self.carroY][self.carroX] = 0
            self.carroX = newX
            self.carroY = newY
            self.blocos_percorridos += 1
            self.label_blocos_percorridos.config(text=str(self.blocos_percorridos))  # Atualiza a label de blocos percorridos
            if self.mapa[newY][newX] == 1:
                self.vidas -= 1
                self.label_vidas.config(text=str(self.vidas))  # Atualiza a label de vidas
                if self.vidas <= 0:
                    self.fimJogo(False)
                    return
            elif self.mapa[newY][newX] == 'vida_verde':
                self.vidas += 1
                self.label_vidas.config(text=str(self.vidas))  # Atualiza a label de vidas
            self.mapa[newY][newX] = 'carro'
            self.desenharMapa()
        else:
            print("Movimento inválido!")

    def reiniciarJogo(self):
        self.vidas = 3  
        self.blocos_percorridos = 0
        self.label_blocos_percorridos.config(text=str(self.blocos_percorridos))  # Reinicia a label de blocos percorridos
        self.label_vidas.config(text=str(self.vidas))  # Reinicia a label de vidas
        self.carroX = 0 
        self.carroY = 0
        self.mapa = [[self.gerar_elemento() for _ in range(self.tamanhoMapa)] for _ in range(self.tamanhoMapa)]
        self.mapa[self.carroY][self.carroX] = 'carro'
        self.desenharMapa()
        if self.vidas <= 0:
            self.master.destroy()  # Fecha a janela do jogo
            iniciarJogo()  # Volta para a tela de menu

    def fimJogo(self, sucesso):
        if sucesso:
            print("Parabéns! Você concluiu o desafio com sucesso!")
        else:
            print("Game Over!")
            self.reiniciarJogo()

def iniciarJogo():
    root = tk.Tk()
    root.title("Campo Minado")
    tk.Label(root, text="Tamanho do mapa:").pack()
    entryTamanhoMapa = tk.Entry(root)
    entryTamanhoMapa.pack()

    tk.Button(root, text="Iniciar", command=lambda: criarJanelaJogo(root, entryTamanhoMapa)).pack()
    root.mainloop()

def criarJanelaJogo(root_menu, entry_tamanho_mapa):
    tamanhoMapa = int(entry_tamanho_mapa.get())
    root_menu.destroy()  # Fecha a janela do menu
    root_jogo = tk.Tk()
    root_jogo.title("Campo Minado")
    campo = CampoMinado(root_jogo, tamanhoMapa, 0.4)
    root_jogo.bind("<Up>", lambda event: campo.moverCarro(0, -1))
    root_jogo.bind("<Down>", lambda event: campo.moverCarro(0, 1))
    root_jogo.bind("<Left>", lambda event: campo.moverCarro(-1, 0))
    root_jogo.bind("<Right>", lambda event: campo.moverCarro(1, 0))
    root_jogo.mainloop()

# Iniciar o jogo
iniciarJogo()
