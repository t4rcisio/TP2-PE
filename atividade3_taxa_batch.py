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
d=pd.DataFrame([(t,b,v) for t in [.01,.05,.1] for b in [32,64] for v in np.random.normal(60 if t==.1 and b==32 else {.01:90,.05:93,.1:94}[t],1,5)],columns=['Taxa','Batch','Acuracia'])
executar('Atividade prática 3: taxa de aprendizado × batch',d,'Acuracia',['Taxa','Batch'],'Experimento 3 × 2, com cinco repetições por combinação, desvio padrão 1 ponto percentual e semente 42. A interação é significativa: F(2,24) = 1455,0003; p = 8,97 × 10⁻²⁶. As linhas apresentam forte mudança de inclinação. Em batch 32, a taxa 0,1 reduz a média a 59,87%; em batch 64, a média é 93,69%. Esta é a maior média observada, mas o Tukey não a distingue da taxa 0,05 com batch 64. O efeito da taxa depende do batch.')
