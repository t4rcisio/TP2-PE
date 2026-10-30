"""
Disciplina: TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES:
PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO
Aluno: Tarcisio Batista Prates
Instituição: Centro Federal de Educação Tecnológica de Minas Gerais
"""
from analise_comum import ROOT, executar, model, parts, table
import numpy as np
import pandas as pd

np.random.seed(42)
d=pd.DataFrame({'Tratamento':np.repeat(['T1','T2','T3','T4'],50),'Resposta':np.concatenate([np.random.normal(mu,5,50) for mu in [50,50,65,75]])})
executar('Atividade prática 1: quatro tratamentos simulados',d,'Resposta',['Tratamento'],'Foram geradas 50 observações por grupo, com médias populacionais 50, 50, 65 e 75 e desvio padrão 5 (semente 42). F(3,196) = 371,395; p = 1,44 × 10⁻⁸⁰. Rejeita-se a igualdade global. T1 e T2 não diferem significativamente (p = 0,560); T3 e T4 superam ambos e também diferem entre si. Ordem: T4 > T3 > T2 ≈ T1. A igualdade populacional de T1 e T2 foi definida na simulação; o teste não comprova equivalência.')
