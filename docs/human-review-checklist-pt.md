# Checklist operacional — revisão humana

Use este checklist junto de [human-review-protocol-pt.md](human-review-protocol-pt.md). Ele não substitui o arquivo JSON oficial gerado pelo grader.

## Antes de revisar

- [ ] Confirmei o caso, a execução e a versão do grader.
- [ ] Preservei os arquivos originais sem edição.
- [ ] Executei o grader e guardei o relatório numérico.
- [ ] Confirmei que a entrega está elegível para aprovação final.
- [ ] Abri a tarefa e os dados de entrada correspondentes.
- [ ] Li a explicação integralmente antes de consultar pareceres de IA.

## Revisão dos quatro critérios

| Critério | Pass | Fail | Evidência / justificativa |
|---|:---:|:---:|---|
| `correct_summary` | [ ] | [ ] | |
| `supported_drivers` | [ ] | [ ] | |
| `complete_exceptions` | [ ] | [ ] | |
| `assumptions_and_limitations` | [ ] | [ ] | |

Cada critério precisa de exatamente um veredito e de justificativa específica no JSON oficial. Não deixe critérios como `pending`.

## Encerramento

- [ ] O nome no campo `reviewer` identifica a pessoa que realmente realizou a revisão.
- [ ] O JSON foi copiado do `human_review_template` desta execução.
- [ ] Os hashes e a versão do grader foram preservados sem alteração.
- [ ] O arquivo de revisão está fora da pasta da submissão.
- [ ] O relatório final foi gerado em um caminho novo.
- [ ] Conferi `overall_passed`, `status` e `numerical_passed`.
- [ ] Registrei separadamente data, divergências e limitações relevantes.
- [ ] Não confundi parecer preliminar de IA com aprovação humana.

**Resultado:**  
- [ ] Aprovação final (`overall_passed: true`)  
- [ ] Reprovado numericamente  
- [ ] Reprovado na revisão explicativa  
- [ ] Incompleto / não elegível  
- [ ] Avaliação pendente / erro do avaliador

**Revisor:**  
**Data da revisão:**  
**Observações / divergências:**
