# Caso 003 — primeira comparação da bateria

| Entrega | Nota numérica | Verificações | Palavras | Estado oficial |
|---|---:|---:|---:|---|
| GPT-6 Astra | 100/100 | 126/126 | 545 | explanation_review_pending |
| Claude | 100/100 | 126/126 | 802 | incomplete_submission |

Os dois JSONs estão estruturalmente válidos e todos os cálculos conferem. Ambos acertaram juros de 300,01 na primeira semana, o saque de apenas 0,04 na segunda, o teto de crédito na terceira e a restrição de caixa na quarta. Não houve divergência financeira numérica entre os resultados.

## Diferença de cumprimento do contrato

O contrato limita `analysis.md` a 800 palavras separadas por espaços, incluindo títulos. O mesmo avaliador contou 545 no GPT e 802 no Claude. Títulos e elementos da tabela entram na contagem conforme a regra publicada; não foi adotada uma regra nova após observar as respostas.

O Claude excedeu o limite em duas palavras. A nota numérica permanece 100/100, mas a entrega é incompleta. Esse é um descumprimento de formato, não um erro de cálculo. Os arquivos foram preservados; não se removeu texto nem se substituiu a primeira entrega por uma correção.

Na revisão preliminar por IA, os quatro critérios de conteúdo financeiro parecem atendidos por ambas as explicações. Isso não elimina a violação de tamanho nem concede aprovação humana. `overall_passed` permanece falso nas duas avaliações.

## Condições conhecidas

O usuário confirmou conversas novas, ausência de dicas, memória desativada e ausência de ferramentas de navegação para ambas as respostas. São informações declaradas pelo operador, sem histórico completo de execução. Modo de raciocínio, quantidade de tentativas e ferramentas locais não foram confirmados separadamente.

Os nomes informados nesta entrega foram GPT-6 Astra e Claude. Nas rodadas anteriores o segundo modelo foi identificado como Claude Code Opus 5.5; essa versão não foi reconfirmada nesta entrega. Afirmações contidas nos textos sobre cálculos locais ou validações não são evidência independente de ferramentas utilizadas.

## Rastreabilidade

- GPT: `runs/cal-v1-bb_rounding_003-A` — arquivos recebidos `forecast3` e `analysis3`.
- Claude: `runs/cal-v1-bb_rounding_003-B` — arquivos recebidos `forecast4.json` e `analysis4.md`.
- Em cada pasta: originais copiados sem alteração de bytes, `grade.json`, `execution.json` e parecer preliminar separado em `ai-explanation-review.json`.

O plano registra duas execuções avaliadas e seis ainda não iniciadas. Esta observação não estabelece superioridade geral ou maior competência financeira de um modelo. Ambos resolveram a tarefa numérica; somente o cumprimento do limite textual os distinguiu nesta rodada.

## Próximo passo

Executar `bb_customer_004` nos dois modelos, em conversas novas, com o pacote e as instruções internas correspondentes. Não acrescentar advertências especiais sobre o limite de palavras apenas a um modelo, nem fornecer resultados anteriores como dicas. O resultado original do caso 003 permanece preservado.
