# Trabalho de Planejamento de Experimentos

Instituição: Centro Federal de Educação Tecnológica de Minas Gerais

Disciplina: TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES: PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO

Aluno: Tarcisio Batista Prates

## Execução

Requer Python 3.10 ou superior. Extraia o ZIP preservando as pastas.

```bash
python -m pip install -r requirements.txt
python executar_todos.py
```

Para um caso isolado:

```bash
python exercicio41_concreto.py
```

Cada caso gera dados.csv, anova.csv, gráficos PNG e resolucao.html na pasta resultados. Quando aplicável, gera também tukey.csv. O relatório completo é gerado em output/resolucao_anova.html. Os gráficos são salvos sem abrir janelas. Os caminhos independem da pasta de onde o comando é executado.

## Arquivos

- atividade1_quatro_tratamentos.py: simulação de quatro tratamentos, 50 repetições, ANOVA e Tukey.
- atividade2_blocagem.py: comparação do modelo com e sem blocos; usa os 12 dados fixos do exemplo Python do enunciado.
- atividade3_taxa_batch.py: fatorial 3 × 2, cinco repetições por célula.
- exercicio41_concreto.py: ANOVA e Tukey dos métodos de cura.
- exercicio42_logistica.py: ANOVA aditiva com região como bloco.
- exercicio43_servidores.py: sistema × processador com interação.
- exercicio44_processo_quimico.py: pressão × agitação com interação e Tukey.
- analise_comum.py: funções compartilhadas de ANOVA, Tukey e gráficos; deve ficar junto dos scripts.
- gerar_relatorio.py: versão portátil do código usado para gerar a resolução completa, com identificação acadêmica.
- dados/: CSVs originais fornecidos.

## Método e limites

Nível de significância de 5%. Os scripts preservam as sementes (42), as médias e os dados da resolução anterior. As somas de quadrados são calculadas explicitamente com NumPy/pandas para delineamentos balanceados, e os valores p e Tukey com SciPy. Não é necessário statsmodels.

A rotina compartilhada se destina aos delineamentos balanceados e completos destes casos, não a dados arbitrários desbalanceados ou com células ausentes. No DBC não se ajusta interação, pois há apenas uma observação por célula; assume-se aditividade. Não se aplica Tukey aos valores brutos de transportadora ignorando os blocos. Nos fatoriais completos balanceados com repetição, o Tukey sobre combinações usa o mesmo erro residual do modelo completo. Não significância não prova equivalência. No processo químico, Shapiro-Wilk p ≈ 0,0464 sugere desvio de normalidade e requer cautela.

Os CSVs de baterias são exemplos guiados do enunciado e estão incluídos como material de apoio. Os sete scripts de casos correspondem às atividades solicitadas.
