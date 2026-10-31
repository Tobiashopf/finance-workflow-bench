# Revisão da especificação — cash_forecast_001

## Entrega desta etapa

As regras financeiras da especificação e a solução de referência foram revisadas pelo usuário. O contrato de saída v0.2 em `cases/cash_forecast_001/task.md` explicita limites de formato e pontuação, sem alterar essas regras financeiras. O projeto agora inclui dados sintéticos, solução, testes, conferência por dois métodos e avaliador automático. Não há resultados de modelos. Consulte `reports/case-review-pt.md` para os números e `reports/grader-review-pt.md` para a demonstração do avaliador.

## Decisões adotadas

- Empresa e dados fictícios; USD para apresentação internacional.
- Horizonte fixo de 4 de janeiro a 4 de abril de 2027, dividido em 13 semanas.
- Caixa mínimo de USD 50 mil, crédito de USD 200 mil e dívida inicial de USD 60 mil.
- Juros contratuais de 0,2% por semana sobre a dívida de abertura, arredondados para centavos. A taxa é uma premissa didática, não uma estimativa de mercado.
- Recebimentos usam datas fornecidas: esta versão mede execução e análise, não previsão estatística de inadimplência.
- Uso automático de crédito para recompor o caixa mínimo e amortização automática do excedente.
- Insuficiência de crédito permanece explícita; caixa negativo representa déficit projetado sem financiamento.
- Nota numérica e qualidade da explicação são avaliadas separadamente. Aprovação integral depende da revisão humana da explicação.

## Pontos para sua revisão como especialista

Verifique se esse cenário representa um trabalho que você gostaria de apresentar e defender em entrevista. Dê atenção à política automática de financiamento, ao tratamento diagnóstico de déficits e à simplificação de juros semanais. São escolhas deliberadas de escopo, não convenções universais de tesouraria.

## Sequência de construção dos dados e da solução

1. Criar os cinco arquivos de entrada conforme os campos da especificação.
2. Incluir recebíveis parcialmente pagos, duplicatas exatas, transferências internas e registros fora do horizonte.
3. Construir uma trajetória com uso de crédito, amortização e pelo menos uma semana de crédito insuficiente, verificando que os números produzam esses eventos de fato.
4. Criar um exemplo pequeno de conferência manual antes da solução completa.
5. Produzir a solução de referência e verificar as identidades de caixa, dívida e juros por um caminho de cálculo independente.
6. Implementar o esquema de saída e o avaliador somente após estabilizar o contrato e conferir a solução.

## Critérios de qualidade para a implementação

- Testar primeira e última data do horizonte e mudanças de semana.
- Testar que saldo inicial já incorpora valores pagos anteriormente.
- Testar deduplicação por identidade, sem remover eventos legítimos de valores iguais.
- Testar que transferências internas não afetam caixa consolidado.
- Testar juros na semana do saque e da amortização.
- Testar esgotamento do limite, caixa abaixo do mínimo mas positivo e déficit efetivo.
- Testar continuidade por 13 semanas e ausência de saque e amortização simultâneos.
- Rejeitar valores não finitos, campos inesperados e respostas incompletas.
- Manter solução e avaliador fora do ambiente acessível ao agente.

## Estado de publicação

Arquivos locais preparados para iniciar o projeto. Nenhum repositório remoto foi criado ou alterado nesta etapa.
