"""
Disciplina: TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES:
PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO
Aluno: Tarcisio Batista Prates
Instituição: Centro Federal de Educação Tecnológica de Minas Gerais
"""
from analise_comum import ROOT, executar, model, parts, table
import numpy as np
import pandas as pd

executar('Exercício 4.3: sistema operacional × processador',pd.read_csv(ROOT/'dados/exercicio3_servidores.csv'),'Throughput',['Sistema','Processador'],'1. Sistema, processador e interação são significativos a 5%. A interação apresenta F(1,8) = 145,2 e p = 2,08 × 10⁻⁶.<br>2. Com Sistema no eixo horizontal e uma linha por processador, as linhas não se cruzam, mas têm inclinações diferentes. Com Processador no eixo horizontal, a passagem ARM → x86 eleva a média em 70 no Linux e em 180 no Windows. Linhas não precisam se cruzar para haver interação.<br>3. Recomenda-se Linux + x86: throughput médio 925. Essa combinação supera Windows + x86 em 45, com IC95% de Tukey de 24,33 a 65,67. As unidades de throughput não são especificadas no CSV.')
