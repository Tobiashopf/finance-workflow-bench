# Borrowing Base 002: reference financial analysis

Status: reference explanation for owner review; not a model response. All amounts are USD.

The effective facility limits at the four weekly closes are 168,000.00, 104,000.00, 200,000.00 and zero. Closing cash is 50,000.00, zero, 50,000.00 and -20,201.64 respectively. Closing debt is 150,300.00, 110,600.60, 100,821.80 and 100,821.80. The minimum cash buffer is breached in weeks 2 and 4. Only week 4 has an unfunded cash deficit. Debt exceeds its effective limit in weeks 2 and 4, by 6,600.60 and 100,821.80.

## Collateral changes and financing decisions

On January 10, `receivables_snapshots.csv` records A-CORE (100,000.00) and A-EDGE (50,000.00) for customer A, B-CORE (90,000.00), and C-CORE (60,000.00). A-EDGE is exactly 60 days past due and remains eligible; Z-OLD is 61 days past due and is excluded. Eligible balances total 300,000.00. The simultaneous customer cap is 75,000.00. Recognized amounts of 75,000.00, 75,000.00 and 60,000.00 sum to 210,000.00, giving an 80% borrowing base of 168,000.00. Cash events CASH-R-1 and CASH-P-1 contribute 20,000.00 and 30,000.00. Interest of 300.00 leaves cash of 49,700.00 before financing; a draw of 300.00 restores the minimum.

On January 17, A-EDGE is 67 days past due and no longer eligible. A-CORE and A-NEW contribute 120,000.00; B-CORE and C-CORE contribute 40,000.00 each. The eligible pool is 200,000.00 and each customer's cap is 50,000.00. Recognized collateral of 130,000.00 supports 104,000.00 of debt. Opening debt of 150,300.00 requires a 46,300.00 cure. CASH-R-2 of 30,000.00 and CASH-P-2 of 40,000.00, together with 300.60 interest, leave only 39,699.40. All of that cash pays the mandatory cure. Closing cash is zero, debt is 110,600.60 and the unpaid cure is 6,600.60. Preserving the cash minimum would violate the mandatory-repayment priority.

On January 24, eligible balances of A 120,000.00, B 100,000.00, C 100,000.00 and D-NEW 80,000.00 total 400,000.00. After the 100,000.00 per-customer cap, recognized collateral is 380,000.00 and the borrowing base is 304,000.00. The contractual ceiling limits available capacity to 200,000.00. CASH-R-3 of 80,000.00, CASH-P-3 of 20,000.00 and interest of 221.20 leave 59,778.80 before financing. No cure or draw is required; 9,778.80 repays debt voluntarily.

January 31 is explicitly listed in `snapshot_dates.csv` but has no invoice observations. Its collateral and effective limit are zero; the prior snapshot must not be reused. CASH-R-4 of 20,000.00, CASH-P-4 of 90,000.00 and interest of 201.64 produce a 20,201.64 cash deficit. No cash exists for the required 100,821.80 cure, and new borrowing is prohibited. Debt remains outstanding. The buffer shortfall is 70,201.64, distinct from both the cash deficit and the overadvance.

## Exclusions and limitations

Across the first three snapshots, X-DISPUTE is disputed, Y-RELATED is related-party, Z-OLD is over 60 days late and Z-ZERO has no outstanding balance. X-MULTI is classified as disputed ahead of its other exclusion conditions; Y-MULTI is classified as related-party ahead of age and zero balance. Repeated invoice identities across different snapshots are legitimate observations.

Collateral snapshots are post-collection balances, not receipts. Missing collateral does not establish collection or erase debt. All dates, rates, caps and financing priorities are supplied synthetic assumptions. Negative cash and subsequent recovery are diagnostic projections, not authorization for an overdraft or proof of operational feasibility. No external financing, waiver, payment deferral or penalty has been introduced.
