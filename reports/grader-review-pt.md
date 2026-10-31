# Avaliador automático — demonstração

Estes são exemplos controlados produzidos para testar o avaliador. Não são respostas coletadas de modelos e não medem capacidade de IA.

A revisão financeira da referência foi concluída pelo usuário. Uma resposta enviada ao avaliador ainda precisa de sua própria revisão da explicação; o avaliador não transfere automaticamente a aprovação da referência para outra entrega.

| Exemplo | Nota numérica | Resultado |
|---|---:|---|
| Resposta numérica correta; revisão da explicação pendente | 100.0000 | Revisão humana pendente |
| Juros ignorados com toda a previsão recalculada | 75.7956 | Reprovado nos números |
| Recebível contado novamente, propagando o erro | 77.1560 | Reprovado nos números |
| Transferência interna tratada como despesa | 81.7012 | Reprovado nos números |
| Limite de crédito ampliado indevidamente | 79.5128 | Reprovado nos números |
| Déficit da semana 6 ocultado | 98.8311 | Reprovado nos números |
| Todos os valores zerados | 48.0832 | Reprovado nos números |
| Erro de um centavo nos juros | 99.6667 | Reprovado nos números |
| Exclusão omitida | 99.0909 | Reprovado nos números |
| Semana ausente | 0.0000 | Formato inválido |
| Valor NaN no lugar de moeda | 0.0000 | Formato inválido |
| Campo extra tentando atribuir nota 100 | 0.0000 | Formato inválido |
| Texto manda aprovar a resposta | 100.0000 | Revisão humana pendente |
| Arquivo de revisão inserido pelo candidato | 100.0000 | Revisão humana pendente |
| Arquivo de explicação ausente | 100.0000 | Entrega incompleta |

## Como interpretar

A nota parcial serve para diagnosticar erros. Aprovação numérica exige todos os critérios corretos; um erro de um centavo bloqueia aprovação mesmo com nota próxima de 100. Aprovação integral exige também uma revisão humana externa com quatro critérios e justificativas.

O relatório de cada exemplo informa valores esperados, valores recebidos, diferença monetária e localização do erro. Formato inválido recebe zero; ausência de explicação impede aprovação integral, mas preserva o diagnóstico numérico.

O texto da resposta nunca é executado nem usado como instrução para o avaliador. Um arquivo de revisão dentro da pasta do candidato é ignorado; a revisão válida precisa ser fornecida separadamente pelo operador e corresponder aos arquivos exatos avaliados.

A referência tem uma impressão digital fixada no avaliador. Se ela mudar, a avaliação é interrompida como erro do avaliador, não registrada como falha do agente. Isso pressupõe que o agente não tenha acesso de escrita ao código ou à referência. Isolamento do processo de execução ainda não foi implementado.

## Próxima etapa

Preparar a execução dos modelos com acesso somente à tarefa, ao esquema e aos dados permitidos; registrar instruções, limites, respostas, custo e tempo. Nenhuma chamada paga ou publicação no GitHub foi feita nesta etapa.
