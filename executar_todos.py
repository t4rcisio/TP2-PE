"""
Disciplina: TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES:
PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO
Aluno: Tarcisio Batista Prates
Instituição: Centro Federal de Educação Tecnológica de Minas Gerais
"""
from pathlib import Path
import subprocess
import sys
BASE = Path(__file__).resolve().parent
CASOS = ['atividade1_quatro_tratamentos', 'atividade2_blocagem', 'atividade3_taxa_batch', 'exercicio41_concreto', 'exercicio42_logistica', 'exercicio43_servidores', 'exercicio44_processo_quimico']
if __name__ == '__main__':
    for caso in CASOS:
        subprocess.run([sys.executable, str(BASE / (caso + '.py'))], check=True)
    subprocess.run([sys.executable, str(BASE / 'gerar_relatorio.py')], check=True)
    print('Todos os casos executados e relatório completo gerado.')
