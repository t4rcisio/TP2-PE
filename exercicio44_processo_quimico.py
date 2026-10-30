"""
Disciplina: TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES:
PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO
Aluno: Tarcisio Batista Prates
Instituição: Centro Federal de Educação Tecnológica de Minas Gerais
"""
from analise_comum import ROOT, executar, model, parts, table
import numpy as np
import pandas as pd

executar('Exercício 4.4: pressão × agitação',pd.read_csv(ROOT/'dados/processo_quimico.csv'),'Rendimento',['Pressao','Agitacao'],'1. Modelo: Rendimento ~ Pressao * Agitacao. O boxplot mostra o grupo Alta/200 bem acima dos demais.<br>2. A interação é significativa: F(2,12) = 875,7113; p = 9,93 × 10⁻¹⁴. Aumentar a agitação eleva o rendimento em 2,17 unidades nas pressões Baixa e Normal, mas em 30,07 na Alta.<br>3. O setpoint recomendado entre os níveis testados é Pressão Alta + 200 rpm, média 85,53. O Tukey aponta essa combinação como superior a todas as outras. A vantagem sobre a segunda maior média (Alta + 100 rpm, 55,47) é 30,07, IC95% 28,24 a 31,90. Ressalva: Shapiro-Wilk p = 0,0464 indica desvio de normalidade; confirmar a recomendação com mais repetições e análise de sensibilidade antes de aplicação industrial. A unidade do rendimento não está explicitada no CSV.')
