# Adjudicação da auditoria externa — Calibration v1

**Status:** revisão encerrada com ressalvas em 28 de novembro de 2026.

**Decisão do operador:** 28 de novembro de 2026. Os vereditos da auditoria externa são adotados sem alteração para determinar o status vigente. Os registros da primeira rodada permanecem preservados.

## Status vigente

| Execução | Veredito externo | Status adotado |
|---|---|---|
| `bb_rounding_003-A` | `passed` | `passed` |
| `bb_customer_004-A` | `passed` | `passed` |
| `bb_customer_004-B` | `explanation_fail` | `explanation_fail` |
| `bb_cure_005-A` | `passed` | `passed` |
| `bb_cure_005-B` | `explanation_fail` | `explanation_fail` |
| `bb_release_006-A` | `passed`* | `passed`* |

* A revisão de 006-A conserva o campo de revisor informado: `Auditor(a) — Revisão 6`; a identidade não foi confirmada.

## Como a decisão foi aplicada

A primeira rodada registrou `supported_drivers=fail` nos seis casos. O auditor externo marcou `pass` nos seis, e esse veredito foi adotado em todos. Em `bb_customer_004-B`, a primeira rodada aprovou `assumptions_and_limitations`; o auditor externo reprovou pelo texto não reconhecer a limitação intrassemanal, e o operador adotou esse `fail`. Em `bb_cure_005-B`, as duas rodadas reprovaram `assumptions_and_limitations`.

Os relatórios em `adjudicated/` mantêm os números e hashes do grader original, aplicando a avaliação humana externa com a função oficial de validação de revisão. Os formulários recebidos e as notas do auditor estão arquivados separadamente; os registros da primeira rodada não foram alterados.

## Limitações registradas

- As seis notas do auditor informam que a referência protegida não estava disponível. O operador decidiu seguir com os resultados sem consulta posterior à referência. Esta é uma exceção documentada ao procedimento descrito em `docs/human-review-protocol-pt.md`; os resultados são publicados com essa ressalva.
- O nome real do revisor de 006-A não consta do formulário recebido.
- Em `bb_customer_004-A`, o hash da previsão submetida coincide com o hash registrado da referência. A causa dessa coincidência permanece desconhecida, e a execução não deve ser tratada como evidência independente de desempenho até que sua origem seja esclarecida.
- As duas submissões acima do limite de 800 palavras permanecem incompletas e sem revisão final.

Consulte o [registro operacional](calibration-v1-review-log.md), os [formulários externos](../../reviews/human/second/) e os [relatórios adjudicados](adjudicated/).