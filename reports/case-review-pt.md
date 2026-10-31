# Revisão financeira — primeiro caso

Estado: dados e solução calculada disponíveis; conferência por dois métodos concluída. O usuário confirmou a revisão financeira da solução. Nenhum modelo de IA foi avaliado.

## O cenário

A Meridian Distribution é uma distribuidora fictícia. Abre o período com USD 80.000,00 disponíveis em duas contas e USD 60.000,00 de dívida. Pagamentos de fornecedores concentram-se nas semanas 4 a 6; os recebimentos previstos crescem nas semanas 7 e 8. Essa combinação permite observar amortizações, saques, esgotamento de crédito e recuperação posterior.

Os dados são inteiramente sintéticos. A recuperação após um déficit é uma projeção diagnóstica com os fluxos informados; não presume que a empresa conseguiria operar sem uma medida real de financiamento ou renegociação.

## Previsão das 13 semanas

Todos os valores em USD. Saídas excluem juros e principal. O caixa inicial da semana 1 é 80.000,00; nas seguintes, é o fechamento da anterior.

| Semana | Período | Entradas | Saídas | Juros | Saque | Amortização | Caixa final | Dívida final |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2027-01-04 a 2027-01-10 | 45.000,00 | 45.000,00 | 120,00 | 0,00 | 29.880,00 | 50.000,00 | 30.120,00 |
| 2 | 2027-01-11 a 2027-01-17 | 55.000,00 | 66.000,00 | 60,24 | 11.060,24 | 0,00 | 50.000,00 | 41.180,24 |
| 3 | 2027-01-18 a 2027-01-24 | 65.000,00 | 59.000,00 | 82,36 | 0,00 | 5.917,64 | 50.000,00 | 35.262,60 |
| 4 | 2027-01-25 a 2027-01-31 | 40.000,00 | 111.000,00 | 70,53 | 71.070,53 | 0,00 | 50.000,00 | 106.333,13 |
| 5 | 2027-02-01 a 2027-02-07 | 35.000,00 | 130.000,00 | 212,67 | 93.666,87 | 0,00 | 48.454,20 | 200.000,00 |
| 6 | 2027-02-08 a 2027-02-14 | 30.000,00 | 118.000,00 | 400,00 | 0,00 | 0,00 | -39.945,80 | 200.000,00 |
| 7 | 2027-02-15 a 2027-02-21 | 180.000,00 | 37.000,00 | 400,00 | 0,00 | 52.654,20 | 50.000,00 | 147.345,80 |
| 8 | 2027-02-22 a 2027-02-28 | 160.000,00 | 66.000,00 | 294,69 | 0,00 | 93.705,31 | 50.000,00 | 53.640,49 |
| 9 | 2027-03-01 a 2027-03-07 | 90.000,00 | 67.000,00 | 107,28 | 0,00 | 22.892,72 | 50.000,00 | 30.747,77 |
| 10 | 2027-03-08 a 2027-03-14 | 80.000,00 | 76.000,00 | 61,50 | 0,00 | 3.938,50 | 50.000,00 | 26.809,27 |
| 11 | 2027-03-15 a 2027-03-21 | 75.000,00 | 42.000,00 | 53,62 | 0,00 | 26.809,27 | 56.137,11 | 0,00 |
| 12 | 2027-03-22 a 2027-03-28 | 100.000,00 | 83.000,00 | 0,00 | 0,00 | 0,00 | 73.137,11 | 0,00 |
| 13 | 2027-03-29 a 2027-04-04 | 95.000,00 | 42.000,00 | 0,00 | 0,00 | 0,00 | 126.137,11 | 0,00 |

## Resultados para conferir

- Semana 5 (1–7 de fevereiro): caixa final de USD 48.454,20, abaixo do mínimo em USD 1.545,80. Não há déficit efetivo de caixa nesta semana.
- Semana 6 (8–14 de fevereiro): caixa final projetado de USD -39.945,80. São necessários USD 39.945,80 para chegar a zero ou USD 89.945,80 para recompor o caixa mínimo; são medidas diferentes.
- A dívida chega ao limite de USD 200.000,00 na semana 5 e permanece nesse nível na semana 6. É quitada na semana 11.
- Total recebido: USD 1.050.000,00. Total de pagamentos operacionais: USD 942.000,00.
- Saques totais: USD 175.797,64.
- Amortizações totais: USD 235.797,64.
- Juros totais: USD 1.862,89.

## Três conferências pequenas, independentes do caso completo

**Saque.** Com caixa de 50.000, dívida de 60.000, entradas de 10.000 e saídas de 20.000: juros de 120; caixa antes do financiamento de 39.880; saque de 10.120; caixa final de 50.000 e dívida de 70.120.

**Amortização.** Com caixa de 50.000, dívida de 60.000, entradas de 40.000 e saídas de 10.000: juros de 120; caixa antes do financiamento de 79.880; amortização de 29.880; caixa final de 50.000 e dívida de 30.120.

**Crédito insuficiente.** Com caixa de 50.000, dívida de 190.000, entradas de 10.000 e saídas de 80.000: juros de 380; caixa antes do financiamento de -20.380; saque limitado a 10.000; caixa final de -10.380. A falta para o mínimo é 60.380, mas o déficit efetivo é 10.380.

## Registros que merecem atenção

- `receivables.csv / AR-03-A`: fatura de 42.500, com 10.000 já recebidos. Entram somente 32.500 na semana 3; as duas cópias extras são descartadas.
- `receivables.csv / AR-01-A` e `AR-01-B`: duas faturas distintas de 22.500 na mesma data. Ambas entram no cálculo.
- `payables.csv / AP-04`: obrigação de 95.000, com 15.000 já pagos; desembolso futuro de 80.000.
- `payables.csv / AP-05`: pagamento de fornecedor de 120.000 na semana 5, que contribui para esgotar o crédito.
- `payables.csv / TRANSFER-01`: transferência interna de 25.000; efeito consolidado zero.
- `receivables.csv / AR-13-A` e `AR-13-B`: recebimentos em 4 de abril incluídos; `AR-FUTURE`, em 5 de abril, excluído.

## Duplicatas removidas

| Arquivo | Registro | Cópias extras removidas |
|---|---|---:|
| receivables.csv | AR-03-A | 2 |
| receivables.csv | AR-FUTURE | 1 |
| payables.csv | TAX-03 | 1 |
| recurring_expenses.csv | OTHER_RECURRING-01 | 1 |

## Exclusões

| Arquivo | Registro | Motivo |
|---|---|---|
| receivables.csv | AR-PAID | Já integralmente pago |
| receivables.csv | AR-FUTURE | Fora do horizonte |
| payables.csv | TRANSFER-01 | Transferência interna |
| payables.csv | TRANSFER-FUTURE | Transferência interna |
| payables.csv | AP-PAID | Já integralmente pago |
| payables.csv | AP-FUTURE | Fora do horizonte |
| recurring_expenses.csv | RENT-FUTURE | Fora do horizonte |

## O que já foi verificado

Os 13 registros semanais completos coincidiram entre um cálculo com aritmética decimal e outro com centavos inteiros, agregação por dia e cálculo da dívida pela posição líquida de caixa menos dívida. As sete exclusões e cinco cópias duplicadas removidas também coincidiram. O segundo verificador não importa o código da solução de referência; ambos foram produzidos nesta mesma sessão, portanto isso não constitui revisão independente por outro especialista.

Os dez testes da solução cobrem exemplos manuais, arredondamento, registros inválidos, identidades de negócio repetidas, rastreabilidade e continuidade dos saldos. A suíte completa agora também inclui os testes do avaliador; consulte `test-results.json` para o registro da execução e `grader-review-pt.md` para os exemplos controlados.

## Roteiro da revisão financeira concluída

1. Confira os três exemplos pequenos para validar a interpretação da política financeira.
2. Observe as semanas 5 e 6: confirme a distinção entre caixa abaixo do mínimo e déficit efetivo.
3. Avalie se a concentração de pagamentos e a recuperação de recebimentos formam um cenário que você consegue explicar em entrevista.
4. Aponte ajustes de realismo ou apresentação. Não é necessário executar código nem editar os CSVs.

O esquema formal de resposta e o avaliador já foram implementados. A próxima etapa é preparar execuções de modelos em ambiente separado. Os dados são um exemplo público de desenvolvimento, não um teste secreto nem uma validação geral de capacidade financeira.
