# Bateria v1 — resultados finais exploratórios

As oito execuções planejadas foram avaliadas. Não há novas execuções previstas nesta bateria.

| Caso | GPT: nota / palavras | Claude: nota / palavras | Cumprimento do limite textual |
|---|---|---|---|
| 003 — arredondamento | 100/100; 545 | 100/100; 802 | GPT sim; Claude não |
| 004 — concentração por cliente | 100/100; 636 | 100/100; 751 | Ambos sim |
| 005 — amortização e caixa mínimo | 100/100; 561 | 100/100; 789 | Ambos sim |
| 006 — garantia zero | 100/100; 559 | 100/100; 801 | GPT sim; Claude não |

Todas as oito entregas acertaram os critérios numéricos. Os casos têm respectivamente 126, 140, 128 e 124 verificações. Essas verificações são campos de artefatos, não amostras estatísticas independentes. Não houve discriminação de correção financeira numérica nesta bateria. Houve duas violações do limite de explicação nas entregas identificadas como Claude. São observações desta amostra, não uma estimativa de confiabilidade nem um ranking geral.

## Último caso: bb_release_006

Ambos acertaram 124/124 verificações: limite zero no último snapshot, amortização obrigatória paga de USD 150.000,00, dívida final zero e caixa final de USD 69.700,00. Nenhuma violação permanece nos fechamentos. O desaparecimento dos recebíveis não foi tratado como recebimento de caixa.

O usuário relatou que Claude usou somente Python local, decimal e jsonschema, sem navegação, em uma submissão, sem falhas ou intervenção adicional. Relatou também encurtamento de uma versão inicial com 802 palavras. O arquivo final recebido contém 801 palavras pelo critério publicado de separação por espaços, incluindo títulos e elementos de tabelas. O rascunho não foi recebido; não se pode verificar sua contagem. A entrega final é incomplete_submission, embora a nota numérica seja 100/100. Não houve edição pelo avaliador ou substituição do resultado.

A submissão A (559 palavras) passou 124/124 verificações numéricas, mas a revisão humana formal registrou `explanation_fail` em `supported_drivers` porque não cita `receivables_snapshots.csv` como fonte dos saldos de colateral. A submissão B contém 801 palavras e permanece `incomplete_submission`; não recebeu revisão humana formal. O parecer preliminar por IA classificou os critérios de conteúdo como aprovados, mas não substitui o resultado humano nem supera o limite de palavras.

Originais preservados byte a byte em runs/cal-v1-bb_release_006-A e runs/cal-v1-bb_release_006-B. Cada pasta contém grade.json, execution.json e parecer preliminar separado. Os arquivos de Downloads reutilizados não alteraram rodadas anteriores.


## Revisão humana formal

Em 26 de novembro de 2026, as seis explicações dentro do limite receberam revisão formal. Todas ficaram em `explanation_fail`, apesar da aprovação numérica de 100/100. Os dois textos acima de 800 palavras permanecem incompletos e não foram submetidos à aprovação humana.

| Execução | Palavras | Resultado humano | Registro | Relatório final |
|---|---:|---|---|---|
| 003-A | 545 | `explanation_fail` | [revisão](../reviews/human/cal-v1-bb_rounding_003-A-review.json) | [relatório](human/bb_rounding_003-A-reviewed.json) |
| 003-B | 802 | `incomplete_submission` | Não elegível | [grade](../runs/cal-v1-bb_rounding_003-B/grade.json) |
| 004-A | 636 | `explanation_fail` | [revisão](../reviews/human/cal-v1-bb_customer_004-A-review.json) | [relatório](human/bb_customer_004-A-reviewed.json) |
| 004-B | 751 | `explanation_fail` | [revisão](../reviews/human/cal-v1-bb_customer_004-B-review.json) | [relatório](human/bb_customer_004-B-reviewed.json) |
| 005-A | 561 | `explanation_fail` | [revisão](../reviews/human/cal-v1-bb_cure_005-A-review.json) | [relatório](human/bb_cure_005-A-reviewed.json) |
| 005-B | 789 | `explanation_fail` | [revisão](../reviews/human/cal-v1-bb_cure_005-B-review.json) | [relatório](human/bb_cure_005-B-reviewed.json) |
| 006-A | 559 | `explanation_fail` | [revisão](../reviews/human/cal-v1-bb_release_006-A-review.json) | [relatório](human/bb_release_006-A-reviewed.json) |
| 006-B | 801 | `incomplete_submission` | Não elegível | [grade](../runs/cal-v1-bb_release_006-B/grade.json) |

Tobias Hopf de Souza consta como revisor nos seis registros. Não há segunda revisão independente registrada. O parecer preliminar de IA para 006-A marcou `supported_drivers` como aprovado; a revisão formal reprovou o critério pela ausência do nome do arquivo de snapshots de recebíveis. A decisão formal está no registro humano.

Os relatórios finais foram preservados em `reports/human/`. Para 004-A, 004-B e 006-A, a reavaliação foi executada em cópias isoladas com finais de linha LF; para 005-B, os finais de linha dos arquivos locais foram normalizados para corresponder aos hashes previamente registrados. Nenhum conteúdo financeiro ou explicativo foi alterado.

## Limitações da comparação

Nomes de modelos são informados pelo operador. No caso 004, o registro de Claude explicitou que a configuração claude-opus-5-5 não assegura a identidade do modelo que respondeu; a identidade efetiva continua não verificada. Ferramentas e ausência de navegação, quando documentadas, são relatos, sem histórico completo verificado. Modos de raciocínio e condições não foram uniformemente documentados. As condições de uma rodada não foram herdadas pelas demais.

São quatro cenários sintéticos públicos de desenvolvimento, com mecanismos correlacionados e um artefato por serviço em cada caso. Não são um teste secreto ou prova de capacidade geral. Aprovação humana das explicações não foi presumida a partir da revisão dos gabaritos. Quatro pilotos anteriores ficam separados desta bateria; seus resultados não foram descartados.

## Conclusão para o portfólio

O projeto demonstra construção de tarefas financeiras verificáveis, referência em Decimal conferida com centavos inteiros, avaliação determinística, testes de erros deliberados, rastreabilidade de artefatos e distinção entre acurácia numérica e cumprimento do contrato de entrega. Os 69 testes existentes passaram na implementação; não foram necessárias alterações de código para avaliar estas respostas.

O resultado honesto é: oito respostas numericamente corretas, seis revisões humanas formais em explicações elegíveis — todas com `explanation_fail` — e duas submissões incompletas por excesso de palavras. Os registros e relatórios foram arquivados; a tarefa restante é manter a apresentação do repositório atualizada e preparar a publicação. Não há necessidade de ampliar os casos para obter falhas artificiais.