# bb_rounding_003 — análise

Valores em USD. Foram usados exclusivamente os cinco arquivos de entrada, com aritmética decimal local. Os quatro snapshots são estados independentes após os recebimentos; seus saldos não são receitas. Cada um dos oito eventos de caixa foi incluído uma vez na semana de sua data.

## Garantias e limites

As 13 observações de faturas são elegíveis: todas vencem em 2027-02-28, têm zero dias de atraso nos snapshots, saldo positivo e ambas as flags falsas. Não há exclusões. A regra mantém elegibilidade aos 60 dias e exclui acima de 60, com precedência disputed, related_party, over_60_days, zero_balance. Nenhuma dessas exceções ocorre neste conjunto.

Em 2027-01-10, A-1, B-1 e C-1 somam 240000.06. O limite compartilhado por cliente é 60000.01, arredondado para baixo. A e B sofrem deduções de 40000.02 e 20000.01; C não sofre dedução. O reconhecido é 180000.03 e a base/limite efetivo é 144000.02. A regra de 25% aplica-se mesmo com apenas três clientes.

Em 2027-01-17, os mesmos registros somam 240000.12. O limite por cliente sobe a 60000.03; A perde 40000.04 e B perde 20000.00, enquanto C-1, de 60000.02, fica integralmente reconhecida. O reconhecido de 180000.08 gera base de 144000.06. A diferença de quatro centavos no limite libera apenas quatro centavos de saque.

Em 2027-01-24, D-1 aparece e A-1/B-1/C-1 têm novos saldos, totalizando 400000.10. O limite por cliente é 100000.02; C e D têm deduções de 0.01 e 0.02. Reconhecido: 400000.07; base: 320000.05. O teto contratual restringe o limite efetivo a 200000.00.

Em 2027-01-31, D-1 está ausente e contribui zero, sem inferir recebimento. A-1/B-1/C-1 totalizam 210000.06; limite por cliente: 52500.01. As deduções de A e B são 37500.00 e 17500.01; C permanece integral. Reconhecido: 155000.05; base/limite: 124000.04.

As deduções são simultâneas sobre o total original, não baixas contábeis nem pagamentos. Limites por cliente e bases foram truncados ao centavo; juros foram arredondados half-up, inclusive 300.005 para 300.01 na primeira semana.

## Caixa, financiamento e violações

| Fechamento | Juros | Cura paga | Saque | Amortização voluntária | Caixa final | Dívida final | Falta para caixa mínimo |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2027-01-10 | 300.01 | 6002.48 | 0.00 | 0.00 | 43697.51 | 144000.02 | 6302.49 |
| 2027-01-17 | 288.00 | 0.00 | 0.04 | 0.00 | 33409.55 | 144000.06 | 16590.45 |
| 2027-01-24 | 288.00 | 0.00 | 0.00 | 33121.55 | 50000.00 | 110878.51 | 0.00 |
| 2027-01-31 | 221.76 | 0.00 | 13121.53 | 0.00 | 22899.77 | 124000.04 | 27100.23 |

Na primeira semana, a dívida inicial excede o limite em 6002.48. A cura integral precede a reserva mínima e usa o caixa disponível de 49699.99. Nas demais semanas não há cura exigida. Os eventos bb_rounding_003-W3-receipt/payment geram fluxo operacional líquido de 50000.00, permitindo amortização voluntária. Já bb_rounding_003-W4-receipt/payment geram saída líquida de 40000.00; o saque disponível não restaura a reserva.

Há quebra da reserva nas semanas 1, 2 e 4, mas nenhum déficit de caixa não financiado, cura pendente ou dívida acima do limite no fechamento. Crédito não utilizado é 89121.49 na semana 3 e zero nas demais. A recuperação da reserva na semana 3 não elimina as quebras anteriores.

Não foram presumidos refinanciamentos, dispensas, adiamentos, receitas por desaparecimento de faturas ou penalidades. A projeção segue o fechamento semanal contratual e não demonstra suficiência de liquidez intrassemanal.
