# Segundo caso: limite de crédito condicionado aos recebíveis

## Por que este caso

O primeiro caso foi resolvido integralmente na tentativa recebida. Ele permanece como referência básica de correção. O segundo testa uma competência diferente: relacionar a qualidade e a concentração dos recebíveis à capacidade de financiamento, sem confundir garantia com caixa.

Não estamos mudando o gabarito do primeiro caso nem afirmando que o segundo já é mais difícil para modelos. Sua dificuldade será medida somente após criar, revisar e executar o novo caso.

## Regras propostas

- Horizonte de quatro semanas para concentrar a análise na mecânica financeira, sem aumentar o volume artificialmente.
- Caixa inicial de USD 60 mil, dívida de USD 150 mil, caixa mínimo de USD 50 mil e teto contratual de USD 200 mil.
- A carteira de recebíveis é fornecida em fotografias semanais após os recebimentos. Entradas de caixa vêm de outro arquivo; saldo de recebíveis não é recebimento.
- Faturas em disputa, de partes relacionadas ou com mais de 60 dias de atraso não são elegíveis. Exatamente 60 dias permanece elegível.
- Cada cliente pode contribuir com até 25% do total elegível antes dos limites de concentração. Todos os clientes usam a mesma base; não há recálculo circular.
- O limite efetivo corresponde a 80% do valor reconhecido após concentração, respeitando o teto contratual. Os cálculos de garantia são arredondados para baixo em centavos.
- Se a dívida superar o limite efetivo, há amortização obrigatória, com prioridade sobre o caixa mínimo. Ela usa somente caixa disponível depois dos pagamentos e juros.
- A parte da amortização obrigatória que não puder ser paga continua como dívida acima do limite. O modelo não pode apagar a dívida nem inventar financiamento.

São regras contratuais fictícias, explicitadas para que exista uma resposta verificável. Não pretendem representar todos os contratos de crédito reais.

## Exemplos de conferência

Valores em USD. Os exemplos são sequenciais; cada semana começa com os saldos finais da anterior.

| Semana | Recebíveis elegíveis por cliente | Limite efetivo | Amortização obrigatória paga | Caixa final | Dívida final | Dívida acima do limite |
|---|---|---:|---:|---:|---:|---:|
| 1 | 150.000; 90.000; 60.000 | 168.000,00 | 0,00 | 50.000,00 | 150.300,00 | 0,00 |
| 2 | 120.000; 40.000; 40.000 | 104.000,00 | 39.699,40 | 0,00 | 110.600,60 | 6.600,60 |
| 3 | 120.000; 100.000; 100.000; 80.000 | 200.000,00 | 0,00 | 50.000,00 | 100.821,80 | 0,00 |
| 4 | Nenhum recebível elegível | 0,00 | 0,00 | -20.201,64 | 100.821,80 | 100.821,80 |

**Semana 1 — concentração.** O total elegível é 300 mil. O limite por cliente é 75 mil; reconhecemos 75 + 75 + 60 = 210 mil. Com adiantamento de 80%, o limite efetivo é 168 mil. Com entradas de 20 mil, pagamentos de 30 mil e juros de 300, o caixa antes do crédito é 49.700. Um saque de 300 recompõe o mínimo.

**Semana 2 — prioridade da obrigação.** O novo limite é 104 mil e a dívida de abertura é 150.300. A amortização exigida é 46.300. O caixa de abertura de 50 mil, mais entradas de 30 mil, menos saídas de 40 mil e juros de 300,60, deixa apenas 39.699,40. Esse valor é pago, o caixa termina em zero e sobram 6.600,60 de dívida acima do limite. Não há déficit efetivo de caixa, embora o caixa esteja abaixo do mínimo e a obrigação não tenha sido integralmente atendida.

**Semana 3 — recuperação.** O limite volta a 200 mil. Entradas de 80 mil, pagamentos de 20 mil e juros de 221,20 deixam 59.778,80. Há amortização voluntária de 9.778,80. A recuperação do limite não é uma entrada de caixa.

**Semana 4 — ausência de garantia.** Entradas de 20 mil, pagamentos de 90 mil e juros de 201,64 geram caixa antes do financiamento de -20.201,64. Sem caixa e com limite zero, não há como amortizar nem sacar. Toda a dívida de 100.821,80 permanece acima do limite e o déficit de caixa é reportado separadamente.

## O que está pronto e o que falta

As regras deste documento foram revisadas pelo usuário. Agora estão prontos os dados por fatura, a solução, a explicação de referência, o esquema e o avaliador específico. Consulte `reports/borrowing-base-review-pt.md` para a entrega atual. Ainda não há execução de modelos no caso 002; o avaliador do caso 001 não deve ser usado para ele.

## Sua revisão nesta etapa

Concentre-se em três escolhas: usar o total elegível anterior aos ajustes como denominador da concentração; dar prioridade à amortização obrigatória sobre o caixa mínimo; manter explícita a dívida acima do limite quando o caixa não permite pagá-la.

Essas escolhas foram aceitas como regras do contrato fictício. Os exemplos acima contêm respostas de desenvolvimento e não pertencem ao pacote do agente. Use o relatório da entrega atual para conferir a solução detalhada antes da tentativa externa.
