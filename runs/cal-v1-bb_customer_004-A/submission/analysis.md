# bb_customer_004 — análise da projeção

Valores em USD; quatro semanas de 2027-01-04 a 2027-01-31. Foram utilizados exclusivamente os cinco arquivos de entradas do pacote, aplicando as regras de task.md e a estrutura de forecast.schema.json, sem fontes externas.

## Colateral e mudanças de limite

| Snapshot | Elegível S | T por cliente | Reconhecido H | Base BB | Limite L |
|---|---:|---:|---:|---:|---:|
| 2027-01-10 | 240000.00 | 60000.00 | 180000.00 | 144000.00 | 144000.00 |
| 2027-01-17 | 240000.00 | 60000.00 | 160000.00 | 128000.00 | 128000.00 |
| 2027-01-24 | 360000.00 | 90000.00 | 330000.00 | 264000.00 | 200000.00 |
| 2027-01-31 | 240000.00 | 60000.00 | 240000.00 | 192000.00 | 192000.00 |

- **2027-01-10:** A-1, A-2 e A-3 somam 120000.00 para A. O teto compartilhado de 60000.00 gera dedução de 60000.00 para esse cliente. B-1, C-1 e D-1 contribuem com 40000.00 cada, sem deduções. O limite fica abaixo da dívida inicial de 150000.00.
- **2027-01-17:** D-1 passa a saldo zero e recebe o motivo `zero_balance`. D permanece no controle por cliente com valores elegível, reconhecido e deduzido iguais a zero, mas T de 60000.00. B-1 aumenta para 80000.00, gerando dedução de 20000.00. A mantém dedução de 60000.00. Embora S permaneça igual ao anterior, a maior concentração reduz H em 20000.00 e L em 16000.00.
- **2027-01-24:** C-1 e D-1 alcançam 80000.00 cada; B-1 mantém 80000.00. S sobe para 360000.00. Apenas A sofre dedução, agora de 30000.00. A base de 264000.00 excede o teto contratual: L fica limitado a 200000.00.
- **2027-01-31:** A-1, A-2 e A-3 valem 20000.00 cada; B-1, C-1 e D-1 valem 60000.00 cada. Todos os clientes totalizam exatamente T; não há dedução. A redução dos saldos leva BB e L a 192000.00.

Todos os vencimentos são 2027-02-28: atraso calculado igual a zero em todas as 24 observações. Não há disputas nem partes relacionadas. A única exclusão é D-1 em 2027-01-17. Aplicou-se a precedência contratual: disputa, parte relacionada, atraso superior a 60 dias, saldo zero; exatamente 60 dias permaneceria elegível. O teto de concentração usa simultaneamente o S original, sem recalcular denominadores.

## Financiamento e violações

| Fechamento | Juros | Cura paga | Saque | Amortização voluntária | Caixa final | Dívida final | Falta do mínimo |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2027-01-10 | 300.00 | 6000.00 | 0.00 | 0.00 | 43700.00 | 144000.00 | 6300.00 |
| 2027-01-17 | 288.00 | 16000.00 | 0.00 | 0.00 | 17412.00 | 128000.00 | 32588.00 |
| 2027-01-24 | 256.00 | 0.00 | 0.00 | 17156.00 | 50000.00 | 110844.00 | 0.00 |
| 2027-01-31 | 221.69 | 0.00 | 40221.69 | 0.00 | 50000.00 | 151065.69 | 0.00 |

As curas obrigatórias têm prioridade sobre o mínimo de 50000.00. Nas semanas 1 e 2 são integralmente pagas; o limite fica totalmente utilizado e impede saques para recompor o mínimo. Há violação do buffer, mas nenhum déficit de caixa, cura pendente ou dívida acima do limite nos quatro fechamentos.

Na semana 3, o caixa antes do financiamento de 67156.00 permite amortização voluntária. Na semana 4, o caixa de 9778.31 exige saque para atingir o mínimo. Crédito disponível final: 0.00, 0.00, 89156.00 e 40934.31, respectivamente. Juros usam dívida inicial e arredondamento half-up; concentração e base usam truncamento ao centavo.

## Evidência, premissas e limites

Os registros `bb_customer_004-W1-receipt` a `bb_customer_004-W4-receipt` fornecem recebimentos de 20000.00, 10000.00, 60000.00 e 10000.00. Os respectivos registros `bb_customer_004-W1-payment` a `bb_customer_004-W4-payment` fornecem pagamentos de 30000.00, 20000.00, 10000.00 e 50000.00; cada evento foi incluído uma vez.

Snapshots são saldos independentes após recebimentos. Variações dos títulos não geram recebimentos adicionais; deduções de concentração não são pagamentos ou baixas. Base de empréstimo não é caixa nem crédito disponível. Não foram presumidos refinanciamentos, dispensas, atrasos de pagamentos ou penalidades. A recuperação na semana 3 não elimina as violações anteriores. A projeção semanal não atesta liquidez intrassemanal.
