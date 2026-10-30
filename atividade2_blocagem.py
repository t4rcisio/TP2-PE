"""
Disciplina: TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES:
PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO
Aluno: Tarcisio Batista Prates
Instituição: Centro Federal de Educação Tecnológica de Minas Gerais
"""
from analise_comum import ROOT, executar, model, parts, table
import numpy as np
import pandas as pd

d=pd.DataFrame({'Tratamento':['T1','T2','T3']*4,'Bloco':np.repeat(['B1','B2','B3','B4'],3),'Resposta':[84.1,99.8,86.2,89.5,104.3,89.1,98.7,115.2,101.4,106.8,119.5,105.3]})
executar('Atividade prática 2: importância da blocagem',d,'Resposta',['Tratamento','Bloco'],'Utilizados os 12 valores fixos do exemplo Python do PDF. Com blocos, o efeito de tratamento é significativo; sem blocos não é significativo a 5%. O modelo aditivo assume ausência de interação tratamento × bloco; com uma observação por célula não é possível estimá-la separadamente do erro.',False)
an,*_=model(d,'Resposta',['Tratamento']);parts.append('<h3>Modelo sem blocos</h3>'+table(an)+'<p>Sem blocos: QME = 90,3942; F = 3,13384; p = 0,092707. Com blocos: QME = 1,19861; F = 236,3409; p = 1,9693 × 10⁻⁶. A redução do QME é 98,67%.</p><p>Matematicamente, F = QM(tratamento)/QME. Neste delineamento balanceado, a SQ de tratamento permanece 566,5617. A inclusão dos blocos retira 806,3558 da SQ residual, reduzindo-a de 813,5475 para 7,1917. Embora os graus de liberdade do erro caiam de 9 para 6, a redução da soma de quadrados é muito maior, fazendo o QME diminuir e F aumentar. Assim, a variabilidade sistemática entre blocos deixa de mascarar o efeito dos tratamentos. Isso depende da relevância dos blocos, não é garantido em todo conjunto de dados.</p>')

an.to_csv(ROOT/'resultados'/'Atividade_prática_2'/'anova_sem_blocos.csv', index=False)
print('Modelo sem blocos:'); print(an.to_string(index=False))
