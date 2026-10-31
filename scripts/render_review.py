"""Create a Portuguese review table directly from the computed reference."""
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
forecast = json.loads((ROOT / "reference/cash_forecast_001/forecast.json").read_text(encoding="utf-8"))


def br(value):
    return f"{Decimal(value):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


lines = [
    "# Revisão financeira — primeiro caso",
    "",
    "Estado: dados e solução calculada disponíveis; conferência por dois métodos concluída. O usuário confirmou a revisão financeira da solução. Nenhum modelo de IA foi avaliado.",
    "",
    "## O cenário",
    "",
    "A Meridian Distribution é uma distribuidora fictícia. Abre o período com USD 80.000,00 disponíveis em duas contas e USD 60.000,00 de dívida. Pagamentos de fornecedores concentram-se nas semanas 4 a 6; os recebimentos previstos crescem nas semanas 7 e 8. Essa combinação permite observar amortizações, saques, esgotamento de crédito e recuperação posterior.",
    "",
    "Os dados são inteiramente sintéticos. A recuperação após um déficit é uma projeção diagnóstica com os fluxos informados; não presume que a empresa conseguiria operar sem uma medida real de financiamento ou renegociação.",
    "",
    "## Previsão das 13 semanas",
    "",
    "Todos os valores em USD. Saídas excluem juros e principal. O caixa inicial da semana 1 é 80.000,00; nas seguintes, é o fechamento da anterior.",
    "",
    "| Semana | Período | Entradas | Saídas | Juros | Saque | Amortização | Caixa final | Dívida final |",
    "|---|---|---:|---:|---:|---:|---:|---:|---:|",
]
payment_fields = ["supplier_payments", "tax_payments", "other_external_payments", "payroll_payments", "rent_payments", "other_recurring_payments"]
for w in forecast["weeks"]:
    total = sum(Decimal(w[k]) for k in payment_fields)
    values = [w["receipts"], str(total), w["interest_paid"], w["credit_draw"], w["principal_repayment"], w["closing_cash"], w["closing_principal"]]
    lines.append(f"| {w['week']} | {w['start_date']} a {w['end_date']} | " + " | ".join(br(v) for v in values) + " |")
lines.extend([
    "", "## Resultados para conferir", "",
    "- Semana 5 (1–7 de fevereiro): caixa final de USD 48.454,20, abaixo do mínimo em USD 1.545,80. Não há déficit efetivo de caixa nesta semana.",
    "- Semana 6 (8–14 de fevereiro): caixa final projetado de USD -39.945,80. São necessários USD 39.945,80 para chegar a zero ou USD 89.945,80 para recompor o caixa mínimo; são medidas diferentes.",
    "- A dívida chega ao limite de USD 200.000,00 na semana 5 e permanece nesse nível na semana 6. É quitada na semana 11.",
])
payments = sum(Decimal(w[k]) for w in forecast["weeks"] for k in payment_fields)
lines.append(f"- Total recebido: USD {br(sum(Decimal(w['receipts']) for w in forecast['weeks']))}. Total de pagamentos operacionais: USD {br(payments)}.")
for field, label in [("credit_draw", "Saques totais"), ("principal_repayment", "Amortizações totais"), ("interest_paid", "Juros totais")]:
    lines.append(f"- {label}: USD {br(sum(Decimal(w[field]) for w in forecast['weeks']))}.")
lines.extend([
    "", "## Três conferências pequenas, independentes do caso completo", "",
    "**Saque.** Com caixa de 50.000, dívida de 60.000, entradas de 10.000 e saídas de 20.000: juros de 120; caixa antes do financiamento de 39.880; saque de 10.120; caixa final de 50.000 e dívida de 70.120.",
    "",
    "**Amortização.** Com caixa de 50.000, dívida de 60.000, entradas de 40.000 e saídas de 10.000: juros de 120; caixa antes do financiamento de 79.880; amortização de 29.880; caixa final de 50.000 e dívida de 30.120.",
    "",
    "**Crédito insuficiente.** Com caixa de 50.000, dívida de 190.000, entradas de 10.000 e saídas de 80.000: juros de 380; caixa antes do financiamento de -20.380; saque limitado a 10.000; caixa final de -10.380. A falta para o mínimo é 60.380, mas o déficit efetivo é 10.380.",
    "", "## Registros que merecem atenção", "",
    "- `receivables.csv / AR-03-A`: fatura de 42.500, com 10.000 já recebidos. Entram somente 32.500 na semana 3; as duas cópias extras são descartadas.",
    "- `receivables.csv / AR-01-A` e `AR-01-B`: duas faturas distintas de 22.500 na mesma data. Ambas entram no cálculo.",
    "- `payables.csv / AP-04`: obrigação de 95.000, com 15.000 já pagos; desembolso futuro de 80.000.",
    "- `payables.csv / AP-05`: pagamento de fornecedor de 120.000 na semana 5, que contribui para esgotar o crédito.",
    "- `payables.csv / TRANSFER-01`: transferência interna de 25.000; efeito consolidado zero.",
    "- `receivables.csv / AR-13-A` e `AR-13-B`: recebimentos em 4 de abril incluídos; `AR-FUTURE`, em 5 de abril, excluído.",
    "", "## Duplicatas removidas", "", "| Arquivo | Registro | Cópias extras removidas |", "|---|---|---:|",
])
for item in forecast["duplicates_removed"]:
    lines.append(f"| {item['source_file']} | {item['record_id']} | {item['discarded_count']} |")
lines.extend(["", "## Exclusões", "", "| Arquivo | Registro | Motivo |", "|---|---|---|"])
labels = dict(internal_transfer="Transferência interna", zero_outstanding="Já integralmente pago", outside_horizon="Fora do horizonte")
for item in forecast["exclusions"]:
    lines.append(f"| {item['source_file']} | {item['record_id']} | {labels[item['reason']]} |")
lines.extend([
    "", "## O que já foi verificado", "",
    "Os 13 registros semanais completos coincidiram entre um cálculo com aritmética decimal e outro com centavos inteiros, agregação por dia e cálculo da dívida pela posição líquida de caixa menos dívida. As sete exclusões e cinco cópias duplicadas removidas também coincidiram. O segundo verificador não importa o código da solução de referência; ambos foram produzidos nesta mesma sessão, portanto isso não constitui revisão independente por outro especialista.",
    "",
    "Os dez testes da solução cobrem exemplos manuais, arredondamento, registros inválidos, identidades de negócio repetidas, rastreabilidade e continuidade dos saldos. A suíte completa agora também inclui os testes do avaliador; consulte `test-results.json` para o registro da execução e `grader-review-pt.md` para os exemplos controlados.",
    "", "## Roteiro da revisão financeira concluída", "",
    "1. Confira os três exemplos pequenos para validar a interpretação da política financeira.",
    "2. Observe as semanas 5 e 6: confirme a distinção entre caixa abaixo do mínimo e déficit efetivo.",
    "3. Avalie se a concentração de pagamentos e a recuperação de recebimentos formam um cenário que você consegue explicar em entrevista.",
    "4. Aponte ajustes de realismo ou apresentação. Não é necessário executar código nem editar os CSVs.",
    "",
    "O esquema formal de resposta e o avaliador já foram implementados. A próxima etapa é preparar execuções de modelos em ambiente separado. Os dados são um exemplo público de desenvolvimento, não um teste secreto nem uma validação geral de capacidade financeira.",
])
(ROOT / "reports/case-review-pt.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print("Portuguese financial review written.")
