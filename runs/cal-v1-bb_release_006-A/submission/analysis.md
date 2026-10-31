# bb_release_006 — Análise da previsão

Valores em USD. A previsão segue exclusivamente os cinco arquivos de entrada e as regras contratuais do pacote.

| Fechamento | Colateral elegível / reconhecido | Base de empréstimo | Limite efetivo | Caixa final | Dívida final | Crédito não utilizado |
|---|---:|---:|---:|---:|---:|---:|
| 2027-01-10 | 400.000,00 | 320.000,00 | 200.000,00 | 50.000,00 | 150.000,00 | 50.000,00 |
| 2027-01-17 | 400.000,00 | 320.000,00 | 200.000,00 | 50.000,00 | 150.000,00 | 50.000,00 |
| 2027-01-24 | 400.000,00 | 320.000,00 | 200.000,00 | 50.000,00 | 150.000,00 | 50.000,00 |
| 2027-01-31 | 0,00 | 0,00 | 0,00 | 69.700,00 | 0,00 | 0,00 |

## Colateral e concentração

Em 2027-01-10, 2027-01-17 e 2027-01-24, A-1, B-1, C-1 e D-1 apresentam, cada uma, 100.000,00 pendentes para os clientes A, B, C e D. Todas vencem em 2027-02-28: atraso zero, sem disputa ou parte relacionada. As doze observações são elegíveis; a repetição de identificadores entre datas não constitui duplicidade.

Em cada um desses snapshots, S = 400.000,00 e o limiar simultâneo de 25% é 100.000,00. Cada cliente está exatamente no limiar, portanto não há dedução por concentração. H = 400.000,00; o adiantamento de 80% produz 320.000,00, mas o teto contratual restringe o limite a 200.000,00.

2027-01-31 consta expressamente em snapshot_dates.csv e não contém faturas. Esse snapshot vazio é válido: S, T, H, base e limite passam a zero. Nenhuma fatura ou cliente foi inventado, nem o colateral de 24/01 foi transportado. A ausência das quatro faturas não representa exclusão por inadimplência ou prova de recebimento.

A classificação respeita a precedência disputa, parte relacionada, atraso superior a sessenta dias e saldo zero; exatamente sessenta dias seriam elegíveis. Nenhuma dessas exclusões ocorre nos dados. Clientes com todas as faturas excluídas seriam mantidos com valores zero; não existem neste pacote.

## Fluxos, prioridades e violações

O pagamento bb_release_006-W1-payment de 9.700,00 e os juros de 300,00 reduzem o caixa inicial de 60.000,00 a 50.000,00. Nas semanas seguintes, bb_release_006-W2-receipt e bb_release_006-W3-receipt, de 300,00 cada, cobrem exatamente os respectivos juros. Não há saque, amortização obrigatória ou voluntária nas três primeiras semanas.

Em 31/01, bb_release_006-W4-receipt fornece 210.000,00 e bb_release_006-W4-payment consome 40.000,00. Os juros ainda são 300,00, calculados sobre a dívida inicial de 150.000,00. Assim, o caixa antes do financiamento é 219.700,00. O limite zero exige amortização de 150.000,00, integralmente paga antes de proteger o caixa mínimo. Restam 69.700,00 em caixa e nenhuma dívida. A amortização voluntária é zero, pois a dívida já foi liquidada; nenhum saque é possível com limite zero.

Em todos os fechamentos, insuficiência de caixa mínimo, déficit de caixa não financiado, cura pendente e dívida acima do limite são separadamente zero. Todos os indicadores de violação são falsos. A necessidade de cura na quarta semana não equivale a uma violação remanescente no fechamento.

## Método e limites

Foram usados cálculos decimais locais, juros com arredondamento half-up e limites com truncamento ao centavo. Os oito eventos de caixa foram incluídos uma vez, em suas semanas. Datas, campos, valores, flags e chaves foram verificados; o JSON foi validado localmente contra as restrições do esquema fornecido.

Recebimentos provêm exclusivamente de cash_events.csv. Colateral não é dinheiro, receita adicional ou crédito automaticamente disponível. Os snapshots são estados independentes após recebimentos. Não foram presumidas cobranças, refinanciamentos, dispensas de cura ou pagamentos adiados. A análise é semanal, não assegura liquidez intradiária e depende dos fluxos contratuais informados.
