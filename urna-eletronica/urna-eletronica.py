import datetime, tkinter, re

font_family = ("Arial 10")
font_color = "#FFFFFF"
background = "#1e1e1e"

def fecharJanela():
    
    window_eleitores.destroy()
    quit()

def ordenar_candidatos(candidato):
    return candidato['votos']

def contagemDeVotos():
    for candidato in candidatos:
        candidato['votos'] = votos_confirmados.count(candidato['numero'])

def realizarClassificacao():

    ranking = sorted(candidatos, key=ordenar_candidatos, reverse=True)

    return ranking

def mostrarRanking():

    for pos, candidato in enumerate(ranking):

        txt_rank['text'] += f"{pos + 1} - {candidato['nome']}, com {candidato['votos']}\n"
    
def isValidDay():

    data_atual = datetime.date.today()

    if data_atual.ctime()[0:3] == 'Sun':
        return True
    else:
        txt_tempo_data['text'] = "Hoje não é domingo!"
        return False

def isValidTime():

    data_atual = datetime.date.today()

    dia_atual = data_atual.day
    mes_atual = data_atual.month
    ano_atual = data_atual.year

    horario_atual = datetime.datetime.now()
    horario_final = datetime.datetime(ano_atual, mes_atual, dia_atual, 18, 0, 0)

    if horario_atual >= horario_final:
        txt_tempo_data['text'] = "As eleições se encerraram!"
        window_tempo_data.mainloop()
        return False
    else:
        dif_horario = horario_final - horario_atual
        txt_tempo_data['text'] = f"Ainda faltam {dif_horario} para encerrar as eleições"
        window_tempo_data.mainloop()
        return True

def criarArquivoEleitores():

    arq_info_ele = open('info/eleitores.txt', 'w')

    for eleitor in info_eleitores:
        arq_info_ele.write(f"{eleitor[0]}  {eleitor[1]} {eleitor[2]}\n")

    arq_info_ele.close()

def criarArquivoCandidatos():

    arq_info_cand = open('info/candidatos.txt', 'w')

    for pos, candidato in enumerate(ranking):

        arq_info_cand.write(f"{pos + 1} - {candidato['nome']}, com {candidato['votos']}\n")

    arq_info_cand.close()
        
candidatos = [dict(nome="Bolsonaro", numero = "22", votos=0), 
                  dict(nome="Lula", numero="13", votos=0),
                  dict(nome="Ciro", numero="12", votos=0)]

votos_confirmados = list()

info_eleitores = list()

def validarInformacoes():

    res_confirmar['text'] = ""

    exist_candidato = False
    exist_nome = False
    exist_cpf = False

    nome = input_nome.get().capitalize()

    padrao_nome = re.compile("[a-zA-Z\D]+")
    padrao2_nome = re.compile("[\S]+")

    if re.fullmatch(padrao_nome, nome) == None:
        res_nome['text'] = "Nome inválido!\n"
        res_nome['text'] += "Digite-o novamente!"
        input_nome.delete(0, tkinter.END)
    elif re.fullmatch(padrao2_nome, nome) == None:
        res_nome['text'] = "Nome inválido!\n"
        res_nome['text'] += "Digite-o novamente!"
        input_nome.delete(0, tkinter.END)   
    else:
        exist_nome = True
        res_nome['text'] = ""

    cpf = input_cpf.get()

    if len(cpf) == 11 or len(cpf) == 14:
        if ("." in cpf) and ("-" in cpf):
            if cpf[0:3].isnumeric() and cpf[4:7].isnumeric() and cpf[8:11].isnumeric() and cpf[12:14].isnumeric():
                cpf = cpf[0:3] + cpf[4:7] + cpf[8:11] + cpf[12:14]
                exist_cpf = True
                res_cpf['text'] = ""
            else:
                res_cpf['text'] = "CPF inválido!\n"
                res_cpf['text'] += "Digite-o novamente!"
                input_cpf.delete(0, tkinter.END)
        else:
            if not(cpf.isnumeric()):
                res_cpf['text'] = "CPF inválido!\n"
                res_cpf['text'] += "Digite-o novamente!"
                input_cpf.delete(0, tkinter.END)
            else:
                exist_cpf = True
                res_cpf['text'] = ""
    else:
        res_cpf['text'] = "Esse CPF não atende\n"
        res_cpf['text'] += "a quantidade correta!\n"
        res_cpf['text'] += "Digite-o novamente!"
        input_cpf.delete(0, tkinter.END)

    candidato_escolhido = input_num_cand.get()

    for candidato in candidatos:

        nome_candidato, numero_candidato, votos_candidato = candidato.values()

        if candidato_escolhido == numero_candidato:
            exist_candidato = True
            res_num_cand['text'] = ""
        else:
            continue

    if not(exist_candidato):
        res_num_cand['text'] = f"O número desse\n"
        res_num_cand['text'] += "candidato não consta\n"
        res_num_cand['text'] += "no sistema!\n"
        res_num_cand['text'] += "Digite-o novamente!"
        input_num_cand.delete(0, tkinter.END)

    if info_eleitores == [] and exist_candidato and exist_nome and exist_cpf:

        votos_confirmados.append(candidato_escolhido)

        info_eleitores.append((cpf, nome, candidato_escolhido))

        window_eleitores.destroy()
  
    else:

        if info_eleitores != []:

            if not(cpf in info_eleitores[0]):
                if exist_candidato and exist_cpf and exist_nome:

                    votos_confirmados.append(candidato_escolhido)

                    info_eleitores.append((cpf, nome, candidato_escolhido))

                    window_eleitores.destroy()

                else: 
                    res_confirmar['text'] = "Algumas da informações\n"
                    res_confirmar['text'] = "digitadas é inválida!"
                    res_confirmar['fg'] = "#FF0000"
            else:
                res_cpf['text'] = "Esse CPF consta como já votado!"
                input_cpf.delete(0, tkinter.END)

while True:

    window_tempo_data = tkinter.Tk()
    window_tempo_data.title("Informação Tempo/Data")
    window_tempo_data.configure(background=background)
    window_tempo_data.geometry("350x50")

    txt_tempo_data = tkinter.Label(master=window_tempo_data, bg=background, font=font_family, fg=font_color, anchor="w", text="")
    txt_tempo_data.grid(padx=10, pady=10)

    if isValidDay():

        if isValidTime():

            window_tempo_data.mainloop()

        # Janela para realizar voto

            window_eleitores = tkinter.Tk()
            window_eleitores.title("Realizar Voto")
            window_eleitores.geometry("500x600")
            window_eleitores.configure(background="#1e1e1e")


            # Campo Nome
            txt_nome = tkinter.Label(master=window_eleitores, text="1° Nome do Eleitor", anchor='w', font=font_family , bg=background, fg=font_color)
            txt_nome.grid(row=0, column=0, padx=5, pady=10)

            input_nome = tkinter.Entry(master=window_eleitores, bg="#DADADA")
            input_nome.grid(row=1, column=0, padx=5, pady=5)

            res_nome = tkinter.Label(master=window_eleitores, bg=background, fg="#FF0000", height=3, text="")
            res_nome.grid(row=2, column=0, padx=5, pady=5)

            # Campo Tempo

            txt_tempo = tkinter.Label(master=window_eleitores, text="", font=font_family, bg=background, fg=font_color)
            txt_tempo.grid(row=0, column=1, padx=5, pady=5)

            # Campo CPF
            txt_cpf = tkinter.Label(master=window_eleitores, text="CPF", anchor='w', font=font_family, bg=background, fg=font_color)
            txt_cpf.grid(row=3, column=0, padx=5, pady=5)

            input_cpf = tkinter.Entry(master=window_eleitores, bg="#DADADA")
            input_cpf.grid(row=4, column=0, padx=5, pady=5)

            res_cpf = tkinter.Label(master=window_eleitores, fg="#FF0000", text="", bg=background, height=3)
            res_cpf.grid(row=5, column=0, padx=5, pady=5)


            # Campo Número do Candidato
            txt_num_cand = tkinter.Label(master=window_eleitores, text="Número do Candidato", anchor='w', font=font_family, bg=background, fg=font_color)
            txt_num_cand.grid(row=6, column=0, padx=5, pady=5)

            input_num_cand = tkinter.Entry(master=window_eleitores, bg="#DADADA", width="2", font=("Arial 25"))
            input_num_cand.grid(row=7, column=0, padx=5, pady=5)

            res_num_cand = tkinter.Label(master=window_eleitores, bg=background, fg="#FF0000", text="", height=4)
            res_num_cand.grid(row=8, column=0, padx=5, pady=5)

            # Campo Cofirmar
            btn_confirmar = tkinter.Button(master=window_eleitores, text="Confirmar", command=validarInformacoes, borderwidth=5)
            btn_confirmar.grid(row=9, column=2, padx=5, pady=5)

            res_confirmar = tkinter.Label(master=window_eleitores, text="", bg=background, fg="#00FF44", height=3)
            res_confirmar.grid(row=10, column=0, padx=5, pady=5)

            # Campo Sair Janela
            txt_fechar = tkinter.Label(master=window_eleitores, text="Clique aqui para fechar a janela", fg=font_color, bg=background)
            txt_fechar.grid(row=11, column=2, padx=5, pady=10)

            btn_fechar = tkinter.Button(master=window_eleitores, text="Fechar", command=fecharJanela, borderwidth=5)
            btn_fechar.grid(row=12, column=2)

            window_eleitores.mainloop()

        else:
            break
    else:
        break

contagemDeVotos()

ranking = realizarClassificacao()

window_winner = tkinter.Tk()
window_winner.geometry('40x20')
window_winner.title("Vencedor da Eleição")
window_winner.configure(background=background)

txt_vencedor = tkinter.Label(master=window_winner, text=f"{ranking[0]['nome']} venceu!", bg=background, fg=font_color, font=font_family)
txt_vencedor.grid(column=0, row=0)

window_winner.mainloop()

window_rank = tkinter.Tk()
window_rank.title("Ranking Final")

txt_rank = tkinter.Label(master=window_rank, text="", bg=background, fg=font_color, font=font_family)
txt_rank.grid(column=0, row=0)

mostrarRanking()

window_rank.mainloop()

criarArquivoEleitores()

criarArquivoCandidatos()
