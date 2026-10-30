"""
Disciplina: TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES:
PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO
Aluno: Tarcisio Batista Prates
Instituição: Centro Federal de Educação Tecnológica de Minas Gerais
"""
from pathlib import Path
import numpy as np,pandas as pd,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from io import BytesIO
import base64,html
ROOT=Path(__file__).resolve().parent
(ROOT/'output').mkdir(exist_ok=True)
parts=['''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Resolução de ANOVA</title><style>body{font:16px/1.6 system-ui;max-width:1050px;margin:45px auto;padding:0 25px;color:#213044}h1,h2{color:#123d57}h2{margin-top:45px}table{border-collapse:collapse;width:100%;margin:20px 0;font-size:14px}td,th{padding:8px;border-bottom:1px solid #cbd5df;text-align:right}th:first-child,td:first-child{text-align:left}img{width:100%}pre{white-space:pre-wrap;font-size:12px;background:#f4f6f8;padding:20px}p{max-width:950px}@media print{h2{break-before:page}table,img{break-inside:avoid}}</style><p><strong>Centro Federal de Educação Tecnológica de Minas Gerais</strong><br><strong>Disciplina:</strong> TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES: PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO<br><strong>Aluno:</strong> Tarcisio Batista Prates</p><h1>Planejamento de experimentos e ANOVA</h1><p>Resolução das atividades práticas 1, 2 e 3 e dos exercícios 4.1 a 4.4 do PDF enviado. Nível de significância: 5%. Dados reais dos CSVs anexados; dados simulados identificados explicitamente. Os arquivos de baterias são exemplos guiados, não exercícios adicionais.</p><p>Regra de decisão: rejeitar H₀ quando p &lt; 0,05. Na ANOVA de um fator, H₀ afirma que todas as médias populacionais são iguais. Nos modelos fatoriais, cada efeito e a interação têm seu próprio teste. Não rejeitar H₀ não demonstra equivalência. A independência depende da execução e da aleatorização do experimento.</p>''']
def table(d):return d.to_html(index=False,border=0,float_format=lambda x:f'{x:.6g}')
def model(d,y,fac,interaction=True):
 gm=d[y].mean();pred=np.full(len(d),gm);terms=[]
 for a in fac:
  av=d.groupby(a)[y].transform('mean');terms.append((a,float(((av-gm)**2).sum()),d[a].nunique()-1));pred+=av-gm
 if len(fac)==2 and interaction:
  cell=d.groupby(fac)[y].transform('mean');terms.append((' × '.join(fac),float(((cell-pred)**2).sum()),terms[0][2]*terms[1][2]));pred=cell
 resid=d[y]-pred;df=len(d)-1-sum(t[2] for t in terms);sq=float((resid**2).sum());mse=sq/df
 rows=[(a,s,k,s/k,s/k/mse,stats.f.sf(s/k/mse,k,df)) for a,s,k in terms];rows.append(('Erro',sq,df,mse,np.nan,np.nan))
 return pd.DataFrame(rows,columns=['Fonte','SQ','GL','QM','F','p']),np.asarray(pred),resid,mse,df

def section(title,d,y,fac,answer,inter=True):
 an,pred,res,mse,df=model(d,y,fac,inter);parts.append('<h2>'+title+'</h2><p>'+answer+'</p>')
 parts.append('<h3>Médias observadas</h3>'+table(d.groupby(fac)[y].agg(['count','mean','std']).reset_index()))
 parts.append('<h3>ANOVA</h3>'+table(an))
 fig,axs=plt.subplots(2,2,figsize=(12,8));groups=list(d.groupby(fac));labels=[' / '.join(map(str,k if isinstance(k,tuple) else (k,))) for k,g in groups]
 axs[0,0].boxplot([g[y] for k,g in groups],tick_labels=labels);axs[0,0].tick_params(axis='x',labelrotation=35);axs[0,0].set_title('Boxplot por combinação');axs[0,0].set_ylabel(y)
 if len(fac)==2:
  for level,g in d.groupby(fac[1]):
   m=g.groupby(fac[0])[y].mean();axs[0,1].plot(m.index.astype(str),m.values,'o-',label=str(level))
  axs[0,1].legend(title=fac[1]);axs[0,1].set_xlabel(fac[0]);axs[0,1].set_title('Gráfico de interação (médias)')
 else:
  m=d.groupby(fac[0])[y].mean();axs[0,1].bar(m.index.astype(str),m.values);axs[0,1].set_title('Médias por tratamento')
 axs[1,0].scatter(pred,res);axs[1,0].axhline(0,color='gray',ls='--');axs[1,0].set(xlabel='Valores ajustados',ylabel='Resíduos',title='Resíduos versus ajustados')
 stats.probplot(res,plot=axs[1,1]);axs[1,1].set_title('Q-Q plot dos resíduos');fig.tight_layout();buf=BytesIO();fig.savefig(buf,format='png',dpi=130);plt.close(fig)
 parts.append('<img alt="Gráficos exploratórios e diagnóstico" src="data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()+'">')
 sp=stats.shapiro(res).pvalue;parts.append(f'<p>Shapiro-Wilk dos resíduos: p = {sp:.6g}. '+('Não se detectou desvio de normalidade; isso não prova que os resíduos sejam normais.' if sp>=.05 else 'Há indício de desvio de normalidade ao nível de 5%. Interpretar a inferência paramétrica com cautela; apenas três observações por célula limitam a validação.')+'</p>')
 if len(fac)==1 or inter:
  tk=stats.tukey_hsd(*[g[y].to_numpy() for k,g in groups]);ci=tk.confidence_interval();rows=[]
  for i in range(len(groups)):
   for j in range(i+1,len(groups)):
    rows.append((labels[i]+' − '+labels[j],tk.statistic[i,j],ci.low[i,j],ci.high[i,j],tk.pvalue[i,j],'Sim' if tk.pvalue[i,j]<.05 else 'Não'))
  parts.append('<h3>Tukey: diferenças entre médias e IC simultâneos de 95%</h3>'+table(pd.DataFrame(rows,columns=['Comparação','Diferença','IC inferior','IC superior','p ajustado','Significativo'])))
  parts.append('<p>Um intervalo que inclui zero não indica diferença significativa; um intervalo inteiramente positivo indica que a primeira média é maior. Letras de grupos devem ser interpretadas apenas como ausência/presença de diferenças detectadas, não como equivalência comprovada.</p>')
 return an
np.random.seed(42)
d=pd.DataFrame({'Tratamento':np.repeat(['T1','T2','T3','T4'],50),'Resposta':np.concatenate([np.random.normal(mu,5,50) for mu in [50,50,65,75]])})
section('Atividade prática 1: quatro tratamentos simulados',d,'Resposta',['Tratamento'],'Foram geradas 50 observações por grupo, com médias populacionais 50, 50, 65 e 75 e desvio padrão 5 (semente 42). F(3,196) = 371,395; p = 1,44 × 10⁻⁸⁰. Rejeita-se a igualdade global. T1 e T2 não diferem significativamente (p = 0,560); T3 e T4 superam ambos e também diferem entre si. Ordem: T4 > T3 > T2 ≈ T1. A igualdade populacional de T1 e T2 foi definida na simulação; o teste não comprova equivalência.')
d=pd.DataFrame({'Tratamento':['T1','T2','T3']*4,'Bloco':np.repeat(['B1','B2','B3','B4'],3),'Resposta':[84.1,99.8,86.2,89.5,104.3,89.1,98.7,115.2,101.4,106.8,119.5,105.3]})
section('Atividade prática 2: importância da blocagem',d,'Resposta',['Tratamento','Bloco'],'Utilizados os 12 valores fixos do exemplo Python do PDF. Com blocos, o efeito de tratamento é significativo; sem blocos não é significativo a 5%. O modelo aditivo assume ausência de interação tratamento × bloco; com uma observação por célula não é possível estimá-la separadamente do erro.',False)
an,*_=model(d,'Resposta',['Tratamento']);parts.append('<h3>Modelo sem blocos</h3>'+table(an)+'<p>Sem blocos: QME = 90,3942; F = 3,13384; p = 0,092707. Com blocos: QME = 1,19861; F = 236,3409; p = 1,9693 × 10⁻⁶. A redução do QME é 98,67%.</p><p>Matematicamente, F = QM(tratamento)/QME. Neste delineamento balanceado, a SQ de tratamento permanece 566,5617. A inclusão dos blocos retira 806,3558 da SQ residual, reduzindo-a de 813,5475 para 7,1917. Embora os graus de liberdade do erro caiam de 9 para 6, a redução da soma de quadrados é muito maior, fazendo o QME diminuir e F aumentar. Assim, a variabilidade sistemática entre blocos deixa de mascarar o efeito dos tratamentos. Isso depende da relevância dos blocos, não é garantido em todo conjunto de dados.</p>')
np.random.seed(42)
d=pd.DataFrame([(t,b,v) for t in [.01,.05,.1] for b in [32,64] for v in np.random.normal(60 if t==.1 and b==32 else {.01:90,.05:93,.1:94}[t],1,5)],columns=['Taxa','Batch','Acuracia'])
section('Atividade prática 3: taxa de aprendizado × batch',d,'Acuracia',['Taxa','Batch'],'Experimento 3 × 2, com cinco repetições por combinação, desvio padrão 1 ponto percentual e semente 42. A interação é significativa: F(2,24) = 1455,0003; p = 8,97 × 10⁻²⁶. As linhas apresentam forte mudança de inclinação. Em batch 32, a taxa 0,1 reduz a média a 59,87%; em batch 64, a média é 93,69%. Esta é a maior média observada, mas o Tukey não a distingue da taxa 0,05 com batch 64. O efeito da taxa depende do batch.')
section('Exercício 4.1: resistência do concreto',pd.read_csv(ROOT/'dados/exercicio1_concreto.csv'),'Resistencia',['Metodo'],'1. O boxplot mostra o grupo Centrifugado acima do Vibrado, que fica acima do Convencional, sugerindo diferenças de resistência.<br>2. ANOVA: F(2,12) = 185,4883; p = 9,46 × 10⁻¹⁰. O Q-Q plot é compatível com normalidade, sem desvio acentuado; Shapiro-Wilk p = 0,6009.<br>3. Recomenda-se Centrifugado para maximizar resistência: média 40,88 MPa. O Tukey identifica diferenças entre todos os métodos. A vantagem média sobre Vibrado é 5,14 MPa (IC95%: 3,73 a 6,55); sobre Convencional é 10,16 MPa (8,75 a 11,57). A recomendação considera resistência, sem avaliação de custo.')
d=pd.read_csv(ROOT/'dados/exercicio2_logistica.csv')
section('Exercício 4.2: transportadoras e regiões',d,'Tempo_Entrega',['Transportadora','Regiao'],'1. Modelo: Tempo_Entrega ~ Transportadora + Regiao. Transportadora: F(2,6) = 28,8447; p = 0,000836.<br>2. A região é significativa: F(3,6) = 32,8155; p = 0,000406. A blocagem foi útil: sem região, QME = 2,9883; com região, QME = 0,2575, redução de 91,38%.<br>3. Os resíduos não apresentam um funil evidente, mas os maiores desvios ocorrem na região Norte. Com 12 observações, a avaliação de variância constante é limitada. Existe uma observação por transportadora/região; o modelo pressupõe aditividade. Tempos médios: X = 10,075; Y = 11,400; Z = 8,675. Recomenda-se Z, que tem o menor tempo médio.',False)
section('Exercício 4.3: sistema operacional × processador',pd.read_csv(ROOT/'dados/exercicio3_servidores.csv'),'Throughput',['Sistema','Processador'],'1. Sistema, processador e interação são significativos a 5%. A interação apresenta F(1,8) = 145,2 e p = 2,08 × 10⁻⁶.<br>2. Com Sistema no eixo horizontal e uma linha por processador, as linhas não se cruzam, mas têm inclinações diferentes. Com Processador no eixo horizontal, a passagem ARM → x86 eleva a média em 70 no Linux e em 180 no Windows. Linhas não precisam se cruzar para haver interação.<br>3. Recomenda-se Linux + x86: throughput médio 925. Essa combinação supera Windows + x86 em 45, com IC95% de Tukey de 24,33 a 65,67. As unidades de throughput não são especificadas no CSV.')
section('Exercício 4.4: pressão × agitação',pd.read_csv(ROOT/'dados/processo_quimico.csv'),'Rendimento',['Pressao','Agitacao'],'1. Modelo: Rendimento ~ Pressao * Agitacao. O boxplot mostra o grupo Alta/200 bem acima dos demais.<br>2. A interação é significativa: F(2,12) = 875,7113; p = 9,93 × 10⁻¹⁴. Aumentar a agitação eleva o rendimento em 2,17 unidades nas pressões Baixa e Normal, mas em 30,07 na Alta.<br>3. O setpoint recomendado entre os níveis testados é Pressão Alta + 200 rpm, média 85,53. O Tukey aponta essa combinação como superior a todas as outras. A vantagem sobre a segunda maior média (Alta + 100 rpm, 55,47) é 30,07, IC95% 28,24 a 31,90. Ressalva: Shapiro-Wilk p = 0,0464 indica desvio de normalidade; confirmar a recomendação com mais repetições e análise de sensibilidade antes de aplicação industrial. A unidade do rendimento não está explicitada no CSV.')
parts.append('</html>')
(ROOT/'output/resolucao_anova.html').write_text(''.join(parts),encoding='utf-8')
print('Relatório gerado', (ROOT/'output/resolucao_anova.html').stat().st_size)
