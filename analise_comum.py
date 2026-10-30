"""
Disciplina: TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES:
PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO
Aluno: Tarcisio Batista Prates
Instituição: Centro Federal de Educação Tecnológica de Minas Gerais
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
from io import BytesIO
import base64
ROOT = Path(__file__).resolve().parent
parts = []
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

def executar(nome, dados, resposta, fatores, interpretacao, interacao=True):
    """Gera ANOVA, médias, Tukey aplicável, diagnósticos e relatório do caso."""
    parts.clear()
    anova = section(nome, dados, resposta, fatores, interpretacao, interacao)
    destino = ROOT / 'resultados' / nome.split(':')[0].replace(' ', '_')
    destino.mkdir(parents=True, exist_ok=True)
    dados.to_csv(destino / 'dados.csv', index=False)
    anova.to_csv(destino / 'anova.csv', index=False)
    pagina = '<!doctype html><meta charset="utf-8"><style>body{font:16px system-ui;max-width:1100px;margin:30px auto}img{max-width:100%}td,th{padding:7px}table{border-collapse:collapse}</style>'
    pagina += '<p>Centro Federal de Educação Tecnológica de Minas Gerais<br>TÓPICOS ESPECIAIS EM SISTEMAS INTELIGENTES: PLANEJAMENTO DE EXPERIMENTOS EM COMPUTAÇÃO<br>Aluno: Tarcisio Batista Prates</p>'
    (destino / 'resolucao.html').write_text(pagina + ''.join(parts), encoding='utf-8')
    import re
    for i, encoded in enumerate(re.findall(r'src="data:image/png;base64,([^"]+)"', ''.join(parts)), 1):
        (destino / f'graficos_{i}.png').write_bytes(base64.b64decode(encoded))
    grupos = list(dados.groupby(fatores))
    if len(fatores) == 1 or interacao:
        tukey = stats.tukey_hsd(*[g[resposta].to_numpy() for _, g in grupos])
        ic = tukey.confidence_interval()
        linhas = []
        for i in range(len(grupos)):
            for j in range(i + 1, len(grupos)):
                linhas.append([str(grupos[i][0]), str(grupos[j][0]), tukey.statistic[i,j], ic.low[i,j], ic.high[i,j], tukey.pvalue[i,j]])
        pd.DataFrame(linhas, columns=['grupo_1','grupo_2','diferenca_1_menos_2','ic95_inferior','ic95_superior','p_ajustado']).to_csv(destino / 'tukey.csv', index=False)
    print('\n' + nome)
    print(anova.to_string(index=False))
    print('Resultados:', destino)
    return anova
