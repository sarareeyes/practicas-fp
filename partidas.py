from typing import NamedTuple,List,Counter
from datetime import datetime
import csv
from collections import defaultdict

Partida = NamedTuple("Partida", [
    ("pj1", str),
    ("pj2", str),
    ("puntuacion", int),
    ("tiempo", float),
    ("fecha_hora", datetime),
    ("golpes_pj1", List[str]),
    ("golpes_pj2", List[str]),
    ("movimiento_final", str),
    ("combo_finish", bool),
    ("ganador", str),
    ])

def lee_partidas(ruta)->List[Partida]:
    res=[]
    with open(ruta,ending='Utf-8') as f:
        lector=csv.reader(f)
        for pj1,pj2,puntuacion,tiempo,fecha_hora,golpes_pj1,golpes_pj2,movimiento_final,combo_finish,ganador in lector:
            puntuacion=int(puntuacion)
            tiempo=float(tiempo)
            fecha_hora=datetime.strptime(fecha_hora,'%Y-%m-%d %H:%M:%S')
            golpes_pj1=parsea_lista(golpes_pj1)
            golpes_pj2=parsea_lista(golpes_pj2)
            combo_finish=combierte_booleano(combo_finish)
            res.append(pj1,pj2,puntuacion,tiempo,fecha_hora,golpes_pj1,golpes_pj2,movimiento_final,combo_finish,ganador)
    return res

def parsea_lista(lista):
    lista=lista.replace("[","")
    lista=lista.replace("]","")
    res=lista.split(",")
    return [elem.strip() for elem in res]

def combierte_booleano(combo_finish:str):
    return combo_finish.strip()=='1'
    
def victoria_mas_rapida(lista:List[Partida]):
    mas_rapida=None
    for partidas in lista:
        if partidas.tiempo<mas_rapida.tiempo or mas_rapida is None:
            mas_rapida=partidas
    return (mas_rapida.pj1,mas_rapida.pj2,mas_rapida.tiempo)

def top_ratio_medio_personajes(lista:List[Partida],n):
    valores=dict()
    for partidas in lista:
        if partidas.ganador not in valores:
            valores[partidas.ganador]=[partidas.puntuacion/partidas.tiempo]
        else:
            valores[partidas.ganador].append(partidas.puntuacion/partidas.tiempo)
    for nombre,ratio in valores.items():
        valores[nombre]=sum(ratio)/len(ratio)
    
    valores_ordenados=sorted(valores.items(),key=lambda x:x[1])
    
    return [(nombre for nombre,ratio in valores_ordenados) for _ in range(n)]

def enemigos_mas_debiles(lista:List[Partida],cadena:str):
    c=Counter()
    for partida in lista:
        if partida.ganador==cadena: 
            if partida.ganador==partida.pj1:
                c[partida.pj2]+=1
            else:
                c[partida.pj1]+=1
    max_victorias=max(c.values())
    oponentes_max = [oponente for oponente, count in c.items() if count == max_victorias]
    return  (oponentes_max,max_victorias)

def movimientos_mas_comunes(lista:List[Partida],personaje1,personaje2):
    mov1=[]
    mov2=[]
    for partida in lista:
        if personaje1==partida.pj1:
            mov1.extend(partida.golpes_pj1)
        elif personaje1==partida.pj2:
            mov1.extend(partida.golpes_pj2)
        if personaje2==partida.pj1:
            mov2.extend(partida.golpes_pj1)
        elif personaje2==partida.pj2:
            mov2.extend(partida.golpes_pj2)
    solucion=[valor for valor in mov1 if valor in mov2]
    return solucion

def dia_mas_combo_finish(lista:List[Partida]):
    c=Counter()
    for partida in lista:
        if partida.combo_finish is True:
            c[partida.date.weekday()]+=1
    solucion=dia_de_la_semana(c.most_common(1)[0][0])
    return solucion

def dia_de_la_semana(dia:int):
    if dia==0:
        return "lunes"
    elif dia==1:
        return "martes"
    elif dia==2:
        return "miércoles"
    elif dia==3:
        return "jueves"
    elif dia==4:
        return "viernes"
    elif dia==5:
        return "sábado"
    else:
        return "domingo"