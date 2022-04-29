





_caminho_txt = 'C:\\Users\\User\\Desktop\\Dev\\moneyBot-main\\ativos_contantes.txt'
_lista_sinais = open(_caminho_txt,'r')
lista_sinais = _lista_sinais.read().split('\n')
_lista_sinais.close()
caminho_txt = 'C:\\Users\\User\\Desktop\\Dev\\moneyBot-main\\listas\\'
caminho_txt_cd = 'C:\\Users\\User\\Desktop\\Dev\\moneyBot-main\\CD.txt'
for ativo in lista_sinais:
    arq = open(caminho_txt_cd, 'a')
    
    arq.write(ativo+' ='"'"'C:\\Users\\User\\Desktop\\Dev\\moneyBot-main\\listas\\'+ativo+'.txt'"'"'\n')