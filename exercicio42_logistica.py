"""
Disciplina: TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES:
PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO
Aluno: Tarcisio Batista Prates
Instituição: Centro Federal de Educação Tecnológica de Minas Gerais
"""
from analise_comum import ROOT, executar, model, parts, table
import numpy as np
import pandas as pd

d=pd.read_csv(ROOT/'dados/exercicio2_logistica.csv')
executar('Exercício 4.2: transportadoras e regiões',d,'Tempo_Entrega',['Transportadora','Regiao'],'1. Modelo: Tempo_Entrega ~ Transportadora + Regiao. Transportadora: F(2,6) = 28,8447; p = 0,000836.<br>2. A região é significativa: F(3,6) = 32,8155; p = 0,000406. A blocagem foi útil: sem região, QME = 2,9883; com região, QME = 0,2575, redução de 91,38%.<br>3. Os resíduos não apresentam um funil evidente, mas os maiores desvios ocorrem na região Norte. Com 12 observações, a avaliação de variância constante é limitada. Existe uma observação por transportadora/região; o modelo pressupõe aditividade. Tempos médios: X = 10,075; Y = 11,400; Z = 8,675. Recomenda-se Z, que tem o menor tempo médio.',False)
