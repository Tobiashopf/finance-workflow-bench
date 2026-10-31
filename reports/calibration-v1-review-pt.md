# Bateria v1 — referências completas para revisão

Desenho revisado pelo responsável: confirmação ‘Revisados’. As trajetórias completas abaixo foram geradas depois dessa revisão; revisão humana detalhada ainda pendente.

Os quatro pacotes estão preparados, mas nenhum modelo foi executado nesta bateria. Os exemplos isolados do desenho não são uma sequência temporal.

## bb_rounding_003

Dívida inicial: USD 150002.50. Verificações numéricas: 126.

| Fechamento | Limite | Juros | Amort. obrigatória | Amort. voluntária | Saque | Caixa final | Dívida final | Falta para mínimo | Dívida acima do limite |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2027-01-10 | 144000.02 | 300.01 | 6002.48 | 0.00 | 0.00 | 43697.51 | 144000.02 | 6302.49 | 0.00 |
| 2027-01-17 | 144000.06 | 288.00 | 0.00 | 0.00 | 0.04 | 33409.55 | 144000.06 | 16590.45 | 0.00 |
| 2027-01-24 | 200000.00 | 288.00 | 0.00 | 33121.55 | 0.00 | 50000.00 | 110878.51 | 0.00 | 0.00 |
| 2027-01-31 | 124000.04 | 221.76 | 0.00 | 0.00 | 13121.53 | 22899.77 | 124000.04 | 27100.23 | 0.00 |

A-1, B-1 and C-1 carry cents. Floor the shared cap before applying it, and floor the advance separately. Opening debt 150002.50 produces 300.005 interest, rounded half up to 300.01. D-1 enters in week 3, increasing collateral capacity; its absence in week 4 is not a cash receipt.

## bb_customer_004

Dívida inicial: USD 150000.00. Verificações numéricas: 140.

| Fechamento | Limite | Juros | Amort. obrigatória | Amort. voluntária | Saque | Caixa final | Dívida final | Falta para mínimo | Dívida acima do limite |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2027-01-10 | 144000.00 | 300.00 | 6000.00 | 0.00 | 0.00 | 43700.00 | 144000.00 | 6300.00 | 0.00 |
| 2027-01-17 | 128000.00 | 288.00 | 16000.00 | 0.00 | 0.00 | 17412.00 | 128000.00 | 32588.00 | 0.00 |
| 2027-01-24 | 200000.00 | 256.00 | 0.00 | 17156.00 | 0.00 | 50000.00 | 110844.00 | 0.00 | 0.00 |
| 2027-01-31 | 192000.00 | 221.69 | 0.00 | 0.00 | 40221.69 | 50000.00 | 151065.69 | 0.00 | 0.00 |

A-1, A-2 and A-3 share customer A. In week 1 their total 120000 is capped at 60000, not capped separately per invoice. B-1 grows in week 2 while D-1 has zero balance and is excluded. In week 3 C-1 and D-1 grow, lifting capacity; week 4 the four customers each contribute 60000.

## bb_cure_005

Dívida inicial: USD 150000.00. Verificações numéricas: 128.

| Fechamento | Limite | Juros | Amort. obrigatória | Amort. voluntária | Saque | Caixa final | Dívida final | Falta para mínimo | Dívida acima do limite |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2027-01-10 | 104000.00 | 300.00 | 46000.00 | 0.00 | 0.00 | 43700.00 | 104000.00 | 6300.00 | 0.00 |
| 2027-01-17 | 200000.00 | 208.00 | 0.00 | 3492.00 | 0.00 | 50000.00 | 100508.00 | 0.00 | 0.00 |
| 2027-01-24 | 104000.00 | 201.02 | 0.00 | 0.00 | 3492.00 | 43290.98 | 104000.00 | 6709.02 | 0.00 |
| 2027-01-31 | 200000.00 | 208.00 | 0.00 | 63082.98 | 0.00 | 50000.00 | 40917.02 | 0.00 | 0.00 |

A-1 totals 120000 and B-1/C-1 each 40000 in weeks 1 and 3, giving a 104000 limit. In week 1 the full 46000 mandatory cure is paid but cash is 43700, below minimum by 6300. Debt equals the limit, so no draw can restore the buffer. The diversified week-2/week-4 portfolios increase capacity. Paid cure, buffer shortfall and cash deficit are separate conditions.

## bb_release_006

Dívida inicial: USD 150000.00. Verificações numéricas: 124.

| Fechamento | Limite | Juros | Amort. obrigatória | Amort. voluntária | Saque | Caixa final | Dívida final | Falta para mínimo | Dívida acima do limite |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2027-01-10 | 200000.00 | 300.00 | 0.00 | 0.00 | 0.00 | 50000.00 | 150000.00 | 0.00 | 0.00 |
| 2027-01-17 | 200000.00 | 300.00 | 0.00 | 0.00 | 0.00 | 50000.00 | 150000.00 | 0.00 | 0.00 |
| 2027-01-24 | 200000.00 | 300.00 | 0.00 | 0.00 | 0.00 | 50000.00 | 150000.00 | 0.00 | 0.00 |
| 2027-01-31 | 0.00 | 300.00 | 150000.00 | 0.00 | 0.00 | 69700.00 | 0.00 | 0.00 | 0.00 |

A-1 through D-1 support the facility in weeks 1–3. The explicit final snapshot has no invoices; do not reuse prior collateral. The week-4 receipt event is 210000 and payment is 40000. After 300 interest, cash before financing is 219700: the 150000 mandatory cure fully repays debt and leaves 69700 cash. Zero collateral need not imply a deficit.

