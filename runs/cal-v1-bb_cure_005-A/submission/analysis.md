# bb_cure_005 — análise

Valores em USD. A projeção aplica exclusivamente as regras contratuais do pacote, com juros sobre a dívida de abertura, arredondamento half-up a centavos e arredondamento para baixo no cálculo do limite de concentração e da base de crédito.

| Fechamento | Elegível | Reconhecido | Base de crédito | Limite efetivo | Caixa final | Dívida final | Falta para reserva mínima |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2027-01-10 | 200000.00 | 130000.00 | 104000.00 | 104000.00 | 43700.00 | 104000.00 | 6300.00 |
| 2027-01-17 | 400000.00 | 400000.00 | 320000.00 | 200000.00 | 50000.00 | 100508.00 | 0.00 |
| 2027-01-24 | 200000.00 | 130000.00 | 104000.00 | 104000.00 | 43290.98 | 104000.00 | 6709.02 |
| 2027-01-31 | 400000.00 | 400000.00 | 320000.00 | 200000.00 | 50000.00 | 40917.02 | 0.00 |

## Evidências sobre o colateral

Em 2027-01-10, A-1, do cliente A, tem 120000.00; B-1 e C-1 têm 40000.00 cada. O limite compartilhado por cliente é 50000.00, calculado sobre o total original de 200000.00. A sofre dedução de concentração de 70000.00; B e C não sofrem deduções. A mesma regra vale com apenas três clientes, resultando em 130000.00 reconhecidos e limite de 104000.00.

Em 2027-01-17, A-1, B-1, C-1 e D-1 têm 100000.00 cada. O limite de concentração é 100000.00 e nenhuma dedução ocorre. A base aumenta para 320000.00, mas o teto contratual limita a linha a 200000.00.

Em 2027-01-24, D-1 está ausente e contribui zero; A-1 volta a 120000.00 e B-1/C-1 a 40000.00 cada. Reaparecem a dedução de 70000.00 em A e o limite de 104000.00. Em 2027-01-31, os quatro registros retornam a 100000.00 cada, restaurando o limite efetivo de 200000.00.

Todas as 14 observações vencem em 2027-02-28, têm zero dias de atraso, saldo positivo e flags falsas: não há exclusões por inelegibilidade. A precedência aplicada é disputa, parte relacionada, atraso superior a 60 dias e saldo zero; exatamente 60 dias seria elegível. As 14 observações de clientes estão incluídas, sem eliminar identidades repetidas em datas distintas.

## Financiamento e violações

Na semana 1, os eventos bb_cure_005-W1-receipt/payment somam 70000.00/40000.00. Após juros de 300.00, o caixa é 89700.00. A cura obrigatória de 46000.00 tem prioridade sobre a reserva de 50000.00, deixando 43700.00. A dívida fica no limite, sem cura pendente, mas há violação da reserva.

Na semana 2, os eventos W2-receipt/payment, com o mesmo prefixo bb_cure_005-, somam 10000.00/0.00. Juros de 208.00 deixam 53492.00 antes do financiamento; amortizam-se voluntariamente 3492.00.

Na semana 3, W3-receipt/payment somam 10000.00/20000.00. Juros de 201.02 deixam 39798.98. A dívida inicial de 100508.00 está abaixo do novo limite, portanto não há cura obrigatória. O saque fica restrito à disponibilidade de 3492.00, deixando insuficiência de reserva de 6709.02.

Na semana 4, W4-receipt/payment somam 80000.00/10000.00. Após juros de 208.00, amortizam-se voluntariamente 63082.98. O crédito não utilizado nos quatro fechamentos é, respectivamente, 0.00, 99492.00, 0.00 e 159082.98.

Não há caixa negativo, déficit de caixa não financiado, cura pendente ou dívida acima do limite em nenhum fechamento. A insuficiência da reserva nas semanas 1 e 3 é uma violação distinta.

## Premissas e limites

Os snapshots são estados independentes após recebimentos. Saldos, deduções e desaparecimento de faturas não geram caixa; somente cash_events.csv determina recebimentos e pagamentos. Não foram presumidos refinanciamentos, dispensas ou adiamentos. A projeção semanal não demonstra liquidez intrassemanal. Os dados passaram por validação de datas, valores, flags e duplicidade; o JSON foi validado contra o esquema fornecido.
