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

O GPT entregou 559 palavras e tem status explanation_review_pending. Em revisão preliminar por IA, ambos os textos atendem aos quatro critérios de conteúdo financeiro. A observação de sensibilidade temporal do Claude é qualitativa, não uma simulação intradiária. A revisão humana permanece pendente; overall_passed é falso em ambas as entregas.

Originais preservados byte a byte em runs/cal-v1-bb_release_006-A e runs/cal-v1-bb_release_006-B. Cada pasta contém grade.json, execution.json e parecer preliminar separado. Os arquivos de Downloads reutilizados não alteraram rodadas anteriores.

## Limitações da comparação

Nomes de modelos são informados pelo operador. No caso 004, o registro de Claude explicitou que a configuração claude-opus-5-5 não assegura a identidade do modelo que respondeu; a identidade efetiva continua não verificada. Ferramentas e ausência de navegação, quando documentadas, são relatos, sem histórico completo verificado. Modos de raciocínio e condições não foram uniformemente documentados. As condições de uma rodada não foram herdadas pelas demais.

São quatro cenários sintéticos públicos de desenvolvimento, com mecanismos correlacionados e um artefato por serviço em cada caso. Não são um teste secreto ou prova de capacidade geral. Aprovação humana das explicações não foi presumida a partir da revisão dos gabaritos. Quatro pilotos anteriores ficam separados desta bateria; seus resultados não foram descartados.

## Conclusão para o portfólio

O projeto demonstra construção de tarefas financeiras verificáveis, referência em Decimal conferida com centavos inteiros, avaliação determinística, testes de erros deliberados, rastreabilidade de artefatos e distinção entre acurácia numérica e cumprimento do contrato de entrega. Os 69 testes existentes passaram na implementação; não foram necessárias alterações de código para avaliar estas respostas.

O resultado honesto é: oito respostas numericamente corretas e duas explicações acima do limite. A próxima etapa é consolidar documentação e apresentação do repositório, concluir a revisão humana das explicações quando realizada e preparar a publicação. Não há necessidade de ampliar os casos para obter falhas artificiais.