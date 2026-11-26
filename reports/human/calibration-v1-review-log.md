# Registro operacional das revisões humanas — Calibration v1

**Data da consolidação:** 26 de novembro de 2026 (America/Sao_Paulo).  
**Revisor identificado:** Tobias Hopf de Souza.  
**Revisão independente:** não há segundo revisor registrado.

| Execução | Palavras | Nota numérica | Resultado final | Revisão | Relatório |
|---|---:|---:|---|---|---|
| bb_rounding_003-A | 545 | 100/100 | `explanation_fail` | [registro](../../reviews/human/cal-v1-bb_rounding_003-A-review.json) | [relatório](bb_rounding_003-A-reviewed.json) |
| bb_rounding_003-B | 802 | 100/100 | `incomplete_submission` | Não elegível | [grade](../../runs/cal-v1-bb_rounding_003-B/grade.json) |
| bb_customer_004-A | 636 | 100/100 | `explanation_fail` | [registro](../../reviews/human/cal-v1-bb_customer_004-A-review.json) | [relatório](bb_customer_004-A-reviewed.json) |
| bb_customer_004-B | 751 | 100/100 | `explanation_fail` | [registro](../../reviews/human/cal-v1-bb_customer_004-B-review.json) | [relatório](bb_customer_004-B-reviewed.json) |
| bb_cure_005-A | 561 | 100/100 | `explanation_fail` | [registro](../../reviews/human/cal-v1-bb_cure_005-A-review.json) | [relatório](bb_cure_005-A-reviewed.json) |
| bb_cure_005-B | 789 | 100/100 | `explanation_fail` | [registro](../../reviews/human/cal-v1-bb_cure_005-B-review.json) | [relatório](bb_cure_005-B-reviewed.json) |
| bb_release_006-A | 559 | 100/100 | `explanation_fail` | [registro](../../reviews/human/cal-v1-bb_release_006-A-review.json) | [relatório](bb_release_006-A-reviewed.json) |
| bb_release_006-B | 801 | 100/100 | `incomplete_submission` | Não elegível | [grade](../../runs/cal-v1-bb_release_006-B/grade.json) |

As seis entregas elegíveis foram reprovadas em pelo menos um critério explicativo; nenhuma recebeu aprovação integral. As submissões 003-B e 006-B ultrapassam o limite publicado de 800 palavras e permanecem incompletas, sem revisão humana final.

Uma divergência entre triagem e revisão formal foi registrada em 006-A: a revisão preliminar por IA aprovou `supported_drivers`, enquanto a revisão humana reprovou esse critério porque a análise não nomeia `receivables_snapshots.csv` como fonte dos saldos de colateral. Os registros humanos oficiais contêm a justificativa completa de cada critério.

Os relatórios finais foram arquivados junto dos registros humanos. Nas reavaliações de 004-A, 004-B e 006-A, CRLF foi normalizado para LF somente em cópias isoladas; os arquivos de origem permaneceram intactos. Na reavaliação anterior de 005-B, os finais de linha dos arquivos locais foram normalizados para corresponder aos hashes já registrados. Nenhum conteúdo financeiro ou explicativo foi alterado.
