# Como executar a bateria v1

Os quatro cenários estão implementados e conferidos por dois cálculos. O desenho já foi revisado por Tobias. Confira agora as trajetórias completas em `reports/calibration-v1-review-pt.md`; essa revisão é distinta da aprovação do desenho. Não envie esse relatório aos modelos.

## Sequência

Execute uma variante por vez nos dois modelos, sempre em conversas novas. Mantenha o modo de raciocínio escolhido de cada modelo ao longo da bateria e registre o nome exibido na interface; nomes semelhantes de modo não garantem recursos equivalentes entre serviços. O plano em `plans/calibration-v1-executions.json` reserva oito execuções, todas ainda não iniciadas.

| Ordem | Variante | ZIP na pasta packages | Modelos |
|---|---|---|---|
| 1 | Arredondamento | bb_rounding_003-v1.0/agent-package.zip | A e B, em conversas separadas |
| 2 | Concentração por cliente | bb_customer_004-v1.0/agent-package.zip | A e B, em conversas separadas |
| 3 | Amortização e mínimo de caixa | bb_cure_005-v1.0/agent-package.zip | A e B, em conversas separadas |
| 4 | Garantia zero com solvência | bb_release_006-v1.0/agent-package.zip | A e B, em conversas separadas |

A e B correspondem aos modelos dos pilotos, com seus nomes e configurações confirmados em cada execução. Não é necessário pagar por API. Se houver indisponibilidade ou mudança de modelo, registre a alteração sem atribuir a resposta ao modelo anterior.

## Em cada conversa

1. Abra uma conversa nova. Desative memória pessoal se a interface permitir; anote se não conseguir. Não use este chat de desenvolvimento para resolver os casos.
2. Envie apenas o ZIP correto. Caso o serviço não consiga abrir o ZIP, envie seus oito arquivos, preservando nomes e estrutura quando possível, e registre essa adaptação.
3. Peça para seguir `agent_instructions.md` dentro do ZIP, resolver `task.md` e entregar `forecast.json` e `analysis.md`. O ID da tarefa deve coincidir com o da variante. Não copie instruções de outro caso.
4. Não forneça gabarito, nota, dicas financeiras ou resposta de outro modelo. Ferramentas locais são permitidas; as instruções pedem que não use navegação. Depuração interna não conta como nova submissão, mas deve ser registrada quando conhecida.
5. Salve a primeira entrega em pasta identificada por variante e modelo. Se falhar, preserve a falha; uma repetição precisa de outro registro.
6. Traga os arquivos e os metadados abaixo para avaliação. Não edite o conteúdo antes de enviar.

## Informações que acompanham os arquivos

- Variante, serviço, nome exato do modelo e modo de raciocínio.
- Conversa nova: sim/não/desconhecido. Memória desativada: sim/não/indisponível/desconhecido.
- Uma única solução submetida: sim/não; intervenções ou dicas adicionais.
- Ferramentas observadas por você e, separadamente, ferramentas apenas relatadas pelo modelo.
- Navegação: solicitada como desativada; efetivamente observada; ou apenas declarada como não usada.
- Erros e correções internas, quando disponíveis; início/fim e custo apenas se conhecidos.

Não é obrigatório conhecer todos os campos. Registre desconhecidos em vez de inferir. Se perguntar depois como o modelo trabalhou, guarde a resposta como relato retrospectivo, não como histórico comprovado.

## Avaliação local

O avaliador novo recebe o ID escolhido pelo operador e usa um registro local confiável de referências. Exemplo:

```text
python scripts/grade_calibration.py bb_rounding_003 path/to/submission --report reports/new-run.json
```

O caminho do relatório deve ser novo e ficar fora da submissão. Não use o importador `scripts/run.py`, que continua específico do caso 001. O avaliador não concede aprovação humana automaticamente; 100 pontos com texto válido significa revisão da explicação pendente.

Os relatórios em `reports/calibration-smoke` usam os próprios gabaritos para testar o fluxo e não são resultados de modelos. Os testes do projeto somam 69 e incluem erros deliberados, igualdade dos cálculos completos, divisão de faturas e reordenação de registros. A separação dos oito arquivos do pacote foi verificada, mas não há isolamento de execução comprovado nos serviços externos.
