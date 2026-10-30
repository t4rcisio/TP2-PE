"""
Disciplina: TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES:
PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO
Aluno: Tarcisio Batista Prates
Instituição: Centro Federal de Educação Tecnológica de Minas Gerais
"""
from analise_comum import ROOT, executar, model, parts, table
import numpy as np
import pandas as pd

executar('Exercício 4.1: resistência do concreto',pd.read_csv(ROOT/'dados/exercicio1_concreto.csv'),'Resistencia',['Metodo'],'1. O boxplot mostra o grupo Centrifugado acima do Vibrado, que fica acima do Convencional, sugerindo diferenças de resistência.<br>2. ANOVA: F(2,12) = 185,4883; p = 9,46 × 10⁻¹⁰. O Q-Q plot é compatível com normalidade, sem desvio acentuado; Shapiro-Wilk p = 0,6009.<br>3. Recomenda-se Centrifugado para maximizar resistência: média 40,88 MPa. O Tukey identifica diferenças entre todos os métodos. A vantagem média sobre Vibrado é 5,14 MPa (IC95%: 3,73 a 6,55); sobre Convencional é 10,16 MPa (8,75 a 11,57). A recomendação considera resistência, sem avaliação de custo.')
