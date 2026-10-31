# Segundo caso — dados, solução e avaliação

## Estado da entrega

As regras financeiras foram revisadas pelo usuário. Foram construídos cinco arquivos de entrada, 33 observações de faturas, 8 movimentos de caixa, uma solução numérica e uma explicação de referência. O esquema de saída e o avaliador específico estão implementados. Ainda não houve execução de um modelo neste caso. A revisão humana dos dados detalhados e da explicação de referência não é presumida a partir da revisão anterior das regras.

## Resultados que você pode conferir

Todos os valores em USD. As semanas encerram em 10, 17, 24 e 31 de janeiro de 2027.

| Semana | Total elegível | Garantia após concentração | Limite efetivo | Amortização obrigatória paga | Caixa final | Dívida final | Dívida acima do limite |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 300.000,00 | 210.000,00 | 168.000,00 | 0,00 | 50.000,00 | 150.300,00 | 0,00 |
| 2 | 200.000,00 | 130.000,00 | 104.000,00 | 39.699,40 | 0,00 | 110.600,60 | 6.600,60 |
| 3 | 400.000,00 | 380.000,00 | 200.000,00 | 0,00 | 50.000,00 | 100.821,80 | 0,00 |
| 4 | 0,00 | 0,00 | 0,00 | 0,00 | -20.201,64 | 100.821,80 | 100.821,80 |

Na semana 2, o caixa é totalmente utilizado na amortização obrigatória. Permanecem USD 6.600,60 de dívida acima do limite, mas não existe caixa negativo. Na semana 4, existem simultaneamente déficit de caixa de USD 20.201,64 e dívida acima do limite de USD 100.821,80. A falta para recompor o caixa mínimo é uma terceira medida: USD 70.201,64.

## Registros que demonstram as regras

- `A-EDGE`, em 10 de janeiro, tem exatamente 60 dias de atraso e é elegível. Na observação de 17 de janeiro, tem 67 dias e deixa de ser elegível. A identidade da fatura permanece a mesma, mas sua situação muda.
- `Z-OLD` já tem 61 dias de atraso na primeira observação e é excluída.
- `X-MULTI` tem disputa, vínculo com parte relacionada e atraso; o motivo registrado deve ser disputa, conforme a precedência definida.
- `Y-MULTI` é de parte relacionada, está atrasada e tem saldo zero; o motivo registrado deve ser parte relacionada.
- Clientes X, Y e Z aparecem nos registros por cliente mesmo com valor elegível zero. Isso permite verificar que foram examinados.
- A data de 31 de janeiro está presente em `snapshot_dates.csv`, mas não há faturas nessa fotografia. O modelo precisa registrar garantia zero, sem reutilizar a carteira anterior nem presumir recebimento das faturas ausentes.

## Verificação da solução

O cálculo com aritmética decimal coincidiu com uma implementação separada em centavos inteiros. Foram comparados os quatro registros semanais completos, as 33 decisões por fatura e os 19 registros por cliente. A segunda implementação usa uma formulação diferente para o financiamento, baseada na posição de caixa menos dívida.

As duas implementações foram produzidas nesta sessão com auxílio de IA; isso é conferência computacional, não auditoria por outro especialista. A solução detalhada está em `reference/borrowing_base_002/forecast.json` e a explicação em `reference/borrowing_base_002/analysis.md`.

## Avaliação

O caso possui 152 verificações para a resposta de referência:

| Categoria | Peso | Verificações |
|---|---:|---:|
| Elegibilidade por fatura e total semanal | 20 | 37 |
| Concentração por cliente e limites semanais | 20 | 35 |
| Caixa, juros e financiamento | 40 | 52 |
| Obrigações pendentes, insuficiências e alertas | 20 | 28 |

A aprovação numérica exige todas as verificações corretas. Notas parciais servem ao diagnóstico e não permitem compensar erros relevantes. Formato inválido recebe zero. Texto vazio ou ausente impede aprovação integral. Uma resposta numérica correta recebe o status de revisão da explicação pendente; o avaliador atual não registra aprovação humana automaticamente.

Foram preparados exemplos controlados com juros incorretos, concentração ignorada, garantia tratada como caixa, limite anterior reutilizado, dívida apagada, erros nos limites de 60/61 dias, precedência incorreta, campos extras e instruções de aprovação no texto. Esses exemplos testam o avaliador; não são resultados de modelos.

## Sua próxima ação

Confira os números acima e a explicação de referência. O pacote da segunda rodada já está preparado em `packages/borrowing_base_002-v0.2/agent-package.zip`, separado deste relatório. Quando estiver confortável com a referência, abra uma conversa nova no modelo e envie somente esse ZIP e as instruções de `prompts/borrowing_base_002_instructions.md`.

Use uma tentativa sem dicas; preserve os arquivos `forecast.json` e `analysis.md` exatamente como produzidos. Informe o modelo e as ferramentas utilizadas. O modelo pode usar PowerShell ou Python: o protocolo permite ferramentas de cálculo e não depende de uma implementação específica.

Não envie este relatório, a solução, os exemplos controlados ou a pasta inteira do projeto. O pacote contém apenas os oito arquivos necessários ao agente. O primeiro caso e seu resultado permanecem preservados.

## Limitações

O segundo caso ainda não tem dificuldade calibrada empiricamente, nem há comparação controlada entre modelos. A separação dos arquivos do pacote não equivale a isolamento do sistema operacional. O importador `scripts/run.py` permanece específico do caso 001: os resultados do caso 002 devem ser avaliados com `scripts/grade_borrowing_base.py` e registrados separadamente, sem usar a referência errada.
