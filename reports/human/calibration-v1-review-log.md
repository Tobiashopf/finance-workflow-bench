# Registro operacional das revisões humanas — Calibration v1

**Data da consolidação:** 28 de novembro de 2026 (America/Sao_Paulo).  
**Revisor inicial:** Tobias Hopf de Souza.  
**Segundo revisor conforme informado:** Davi Hopf nos formulários 01–05; `Auditor(a) — Revisão 6` no formulário 06.  
**Decisão do operador:** adotar, sem alteração, os vereditos da auditoria externa como resultado adjudicado vigente.

## Resultado adjudicado

| Execução | Palavras | Nota numérica | Primeira revisão | Auditoria externa | Resultado adotado | Registros |
|---|---:|---:|---|---|---|---|
| bb_rounding_003-A | 545 | 100/100 | `explanation_fail` | `passed` | `passed` | [inicial](../../reviews/human/cal-v1-bb_rounding_003-A-review.json) · [externa](../../reviews/human/second/cal-v1-bb_rounding_003-A-review.json) · [relatório](adjudicated/bb_rounding_003-A-adjudicated.json) |
| bb_rounding_003-B | 802 | 100/100 | `incomplete_submission` | Não revisada | `incomplete_submission` | [grade](../../runs/cal-v1-bb_rounding_003-B/grade.json) |
| bb_customer_004-A | 636 | 100/100 | `explanation_fail` | `passed` | `passed` | [inicial](../../reviews/human/cal-v1-bb_customer_004-A-review.json) · [externa](../../reviews/human/second/cal-v1-bb_customer_004-A-review.json) · [relatório](adjudicated/bb_customer_004-A-adjudicated.json) |
| bb_customer_004-B | 751 | 100/100 | `explanation_fail` | `explanation_fail` | `explanation_fail` | [inicial](../../reviews/human/cal-v1-bb_customer_004-B-review.json) · [externa](../../reviews/human/second/cal-v1-bb_customer_004-B-review.json) · [relatório](adjudicated/bb_customer_004-B-adjudicated.json) |
| bb_cure_005-A | 561 | 100/100 | `explanation_fail` | `passed` | `passed` | [inicial](../../reviews/human/cal-v1-bb_cure_005-A-review.json) · [externa](../../reviews/human/second/cal-v1-bb_cure_005-A-review.json) · [relatório](adjudicated/bb_cure_005-A-adjudicated.json) |
| bb_cure_005-B | 789 | 100/100 | `explanation_fail` | `explanation_fail` | `explanation_fail` | [inicial](../../reviews/human/cal-v1-bb_cure_005-B-review.json) · [externa](../../reviews/human/second/cal-v1-bb_cure_005-B-review.json) · [relatório](adjudicated/bb_cure_005-B-adjudicated.json) |
| bb_release_006-A | 559 | 100/100 | `explanation_fail` | `passed`* | `passed`* | [inicial](../../reviews/human/cal-v1-bb_release_006-A-review.json) · [externa](../../reviews/human/second/cal-v1-bb_release_006-A-review.json) · [relatório](adjudicated/bb_release_006-A-adjudicated.json) |
| bb_release_006-B | 801 | 100/100 | `incomplete_submission` | Não revisada | `incomplete_submission` | [grade](../../runs/cal-v1-bb_release_006-B/grade.json) |

* O formulário externo de 006-A usa `Auditor(a) — Revisão 6`; a identidade real do revisor não está estabelecida. O valor foi preservado exatamente como recebido, conforme decisão do operador.

## Divergências e decisão

A primeira rodada reprovou `supported_drivers` nas seis entregas elegíveis por falta de referência explícita às fontes de dados. A auditoria externa aprovou o critério nas seis. O operador adotou os seis vereditos externos `pass`; a diferença de interpretação permanece registrada. Nenhuma das seis análises cita `receivables_snapshots.csv` pelo nome; as análises 01–02 também não citam `cash_events.csv`.

Em `bb_customer_004-B`, a primeira rodada aprovou `assumptions_and_limitations`, enquanto o auditor externo reprovou esse critério pela falta da ressalva de liquidez intrassemanal e pelo uso de “real liquidity covenant gaps”. O operador adotou o veredito externo `fail`. Em `bb_cure_005-B`, ambos os revisores reprovaram `assumptions_and_limitations`.

A decisão do operador resolve o status publicado em favor da segunda revisão, sem apagar nem reescrever a primeira. Ela não transforma as duas avaliações em consenso e não altera o texto da rubrica.

## Ressalvas de procedimento e integridade

- As seis notas externas informam que o auditor não teve acesso à referência protegida. A auditoria foi aceita como entregue por decisão do operador, mas essa etapa não seguiu integralmente o procedimento de referência descrito no [protocolo](../../docs/human-review-protocol-pt.md).
- O revisor aparece como Davi Hopf nos formulários 01–05. O formulário 06 contém apenas o rótulo genérico acima; não se afirma identidade verificada para essa revisão.
- Em `bb_customer_004-A`, `forecast_sha256` coincide com `reference_sha256`. O grader calcula o hash SHA-256 dos bytes brutos da submissão e compara com o hash de referência; a igualdade indica fortemente correspondência byte a byte. Os metadados disponíveis não esclarecem a origem.
- Os relatórios adjudicados foram gerados com a função oficial `assess_review`, preservando as grades numéricas e os hashes originais. Não houve nova execução numérica nem alteração dos artefatos submetidos.
- `bb_rounding_003-B` (802 palavras) e `bb_release_006-B` (801 palavras) permanecem `incomplete_submission` e não foram submetidas à segunda revisão.
- As notas originais do auditor foram preservadas em [second-review-notes](second-review-notes/).