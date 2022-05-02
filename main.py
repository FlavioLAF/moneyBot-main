
import os
import configparser

from datetime import datetime
from iqoptionapi.stable_api import IQ_Option

import logging
logging.disable(level=(logging.DEBUG))

config = configparser.RawConfigParser()
config.read('C:\\Users\\User\\Desktop\\Dev\\moneyBot-main\\config.cfg')
_dict_config = dict(config.items('CONFIG'))

amount = float(_dict_config['aporte'])
_esperar_usuario_fechar = _dict_config['esperar_usuario_fechar']
_arquivo_sinais = open('C:\\Users\\User\\Desktop\\Dev\\moneyBot-main\\ListaSinais.txt','r')

api = IQ_Option(_dict_config['usuario'], _dict_config['senha'])
_conect_api = api.connect()
api.change_balance(_dict_config['tipo_de_conta'])

lista_arquivo = _arquivo_sinais.read() 

lista = lista_arquivo.split('\n')

#_______________________________SUB CLASSES INICIO_________________________________
class func:
    def bol_ativo_fechado(_id):
        try:
            if 'code' in _id:
                print('ATIVO FECHADO!')
                bol_esperar_usuario_fechar()
            else:
                pass    
        except TypeError:
            pass
#_______________________________SUB CLASSES FIM___________________________________

#___________________________FUNÇÕES-INICIO________________________________________

def bol_esperar_usuario_fechar():
    if _esperar_usuario_fechar == 'N' or _esperar_usuario_fechar == 'n':
        exit()    
    elif(_esperar_usuario_fechar == 'S' or _esperar_usuario_fechar == 'S'):
        os.system('pause')
    else:
        print('Valor da chave: esperar_usuario_fechar, esta incorreta (só S ou N), por favor, corrija!')
        os.system('pause')

def bol_ativo_fechado(_id, _sinal):
    try:
        if 'code' in _id:
            print('ATIVO FECHADO: ',_sinal[1])
            return True
        else:
            return False  
    except TypeError:
        pass
    
def hora_minuto(lista):
    for index, percorre in enumerate(lista):
        _horario = lista[index].split(';')

    _hora_mim = _horario[2].split(':')

    hora_mim = _hora_mim[0] +':'+ _hora_mim[1]
    
    return hora_mim

def time_frame(time):
    if time == 'M1' or time == 'm1':
        return 1
    if time == 'M5' or time == 'm5':
        return 5
    if time == 'M15' or time == 'm15':
        return 15
    if time == 'H1' or time == 'H1':
        return 60

def resultado(_id):
    func.bol_ativo_fechado(_id)
    while True:
        ck, win = api.check_win_digital_v2(_id)
        
        if ck == True:  
            break                  
    return win

def sistema_sem_gale():
    while hora_minuto(lista) >= datetime.today().strftime('%H:%M'):
        
        for index, id in enumerate(lista):
            _sinal = lista[index].split(';')     
                    
            _hora_minuto = _sinal[2].split(':')
            
            hora_minutos = _hora_minuto[0] +':'+_hora_minuto[1]
            
            if hora_minutos == datetime.today().strftime('%H:%M'):
                
                bol, _id = api.buy_digital_spot(_sinal[1], amount, _sinal[3], time_frame(_sinal[0]))
                            
                if bol_ativo_fechado(_id, _sinal) == False:
                    print('---------------ORDEM EXECUTADA----------------')
                    print('--------------'+lista[index]+'----------------')
                    print('---------------VERIFICANDO WIN----------------')        
                    _res = resultado(_id)
                    if _res < 0:
                        print('Loss: ', _res)
                    else: 
                        print('Gain: ', _res)
            
                lista[index] = 'XX;XXXXXX;XX:XX:XX;XXX'
                print(lista[index])
                print('---------------ORDEM FINALIZADA----------------')
                print('\n \n')      
    else:
        print('============================================================')
        print('__________________SISTEMA FINALIZADO________________________')
        print('============================================================')
        bol_esperar_usuario_fechar()
            
def sistema_com_um_gale():
    while hora_minuto(lista) >= datetime.today().strftime('%H:%M'):
        
        for index, id in enumerate(lista):
            _sinal = lista[index].split(';')     
                    
            _hora_minuto = _sinal[2].split(':')
            
            hora_minutos = _hora_minuto[0] +':'+_hora_minuto[1]
            
            if hora_minutos == datetime.today().strftime('%H:%M'):
                
                bol, _id = api.buy_digital_spot(_sinal[1], amount, _sinal[3], time_frame(_sinal[0]))
                            
                if bol_ativo_fechado(_id,_sinal) == False: 
                    print('---------------ORDEM EXECUTADA----------------')
                    print('--------------'+lista[index]+'----------------')
                    print('---------------VERIFICANDO WIN----------------')        
                    _res = resultado(_id)
                    
                    if _res < 0:
                        print('---------------LOSS de '+str(_res)+', EXECUTANDO GALE 1----------------')
                        gale1 = amount * 2.2
                        _bol ,_id = api.buy_digital_spot(_sinal[1], gale1, _sinal[3], time_frame(_sinal[0]))
                        print('---------------VERIFICANDO GALE 1----------------')
                        
                        _res = resultado(_id)
                        if _res < 0:
                            print('_____________________HIT: -'+abs(amount+gale1)+'________________________')
                        else:
                            print('---------------WIN GALE 1 + '+str(_res)+'----------------')
                    else:
                        print('---------------WIN + '+str(_res)+'----------------')
                        
                lista[index] = 'XX;XXXXXX;XX:XX:XX;XXX'
                print(lista[index])
                print('---------------ORDEM FINALIZADA----------------')
                print('\n \n')
    else:
        print('============================================================')
        print('__________________SISTEMA FINALIZADO________________________')
        print('============================================================')
        os.system("pause")
        
def sistema_com_dois_gales():
    while hora_minuto(lista) >= datetime.today().strftime('%H:%M'):
        
        for index, id in enumerate(lista):
            _sinal = lista[index].split(';')     
                    
            _hora_minuto = _sinal[2].split(':')
            
            hora_minuto = _hora_minuto[0] +':'+_hora_minuto[1]
            
            if hora_minuto == datetime.today().strftime('%H:%M'):
                
                bol, _id = api.buy_digital_spot(_sinal[1], amount, _sinal[3], time_frame(_sinal[0]))
                            
                if bol_ativo_fechado(_id, _sinal) == False: 
                    print('---------------ORDEM EXECUTADA----------------')
                    print('--------------'+lista[index]+'----------------')
                    print('---------------VERIFICANDO WIN----------------')        
                    
                    _res = resultado(_id)
                    if _res < 0:
                        print('---------------LOSS de '+str(_res)+', EXECUTANDO GALE 1----------------')
                        gale1 = amount * 2.2
                        _bol ,_id = api.buy_digital_spot(_sinal[1], gale1, _sinal[3], time_frame(_sinal[0]))
                        print('---------------VERIFICANDO GALE 1----------------')
                        
                        _res = resultado(_id)
                        if _res < 0:
                            gale2 = gale1 * 2.2
                            _bol ,_id = api.buy_digital_spot(_sinal[1], gale2, _sinal[3], time_frame(_sinal[0]))
                            print('---------------LOSS de '+str(_res)+', EXECUTANDO GALE 2----------------')
                            print('---------------VERIFICANDO GALE 2----------------')
                            
                            _res = resultado(_id)
                            if _res < 0:
                                print('_____________________HIT: -'+abs(amount+gale1+gale2)+'________________________')
                            else:
                                print("Você ganhou "+str(_res)+"$ no GALE 2")
                        
                        else:
                            print("Você ganhou "+str(_res)+"$ no GALE 1") 
                    
                    else:
                        print("Você ganhou "+str(_res)+"$")                       
            
                lista[index] = 'XX;XXXXXX;XX:XX:XX;XXX'
                print('---------------ORDEM FINALIZADA----------------')
                print('\n \n')
    else:
        print('============================================================')
        print('__________________SISTEMA FINALIZADO________________________')
        print('============================================================')
        bol_esperar_usuario_fechar()       
#___________________________FUNÇÕES-FIM________________________________________

sistema_sem_gale()