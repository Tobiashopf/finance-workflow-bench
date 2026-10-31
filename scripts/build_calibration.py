"""Build frozen calibration v1 inputs, references and allowlisted packages."""
import csv
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from finance_workflow_bench.borrowing_base import DATES, solve, schema
from verify_borrowing_base import compute

NAMES = ("opening_position.json", "cash_events.csv", "receivables_snapshots.csv", "snapshot_dates.csv", "facility.json")
CONFIGS = {
    "bb_rounding_003": dict(debt="150002.50", portfolios=[
        ["100000.03", "80000.02", "60000.01"],
        ["100000.07", "80000.03", "60000.02"],
        ["100000.01", "100000.02", "100000.03", "100000.04"],
        ["90000.01", "70000.02", "50000.03"]], flows=[(20000,30000),(10000,20000),(60000,10000),(10000,50000)]),
    "bb_customer_004": dict(debt="150000.00", portfolios=[
        ["120000.00","40000.00","40000.00","40000.00"],
        ["120000.00","80000.00","40000.00","0.00"],
        ["120000.00","80000.00","80000.00","80000.00"],
        ["60000.00","60000.00","60000.00","60000.00"]], flows=[(20000,30000),(10000,20000),(60000,10000),(10000,50000)]),
    "bb_cure_005": dict(debt="150000.00", portfolios=[
        ["120000.00","40000.00","40000.00"],
        ["100000.00"]*4,
        ["120000.00","40000.00","40000.00"],
        ["100000.00"]*4], flows=[(70000,40000),(10000,0),(10000,20000),(80000,10000)]),
    "bb_release_006": dict(debt="150000.00", portfolios=[["100000.00"]*4]*3+[[]],
                           flows=[(0,9700),(300,0),(300,0),(210000,40000)]),
}


def encoded(obj):
    return (json.dumps(obj, indent=2, ensure_ascii=False)+"\n").encode("utf-8")


def frozen(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != data:
        raise RuntimeError(f"Frozen artifact differs; create a new version: {path}")
    path.write_bytes(data)


def csv_bytes(headers, rows):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(headers.split())
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def build():
    registry, verification = {}, []
    review = ["# Bateria v1 — referências completas para revisão", "",
              "Desenho revisado pelo responsável: confirmação ‘Revisados’. As trajetórias completas abaixo foram geradas depois dessa revisão; revisão humana detalhada ainda pendente.",
              "", "Os quatro pacotes estão preparados, mas nenhum modelo foi executado nesta bateria. Os exemplos isolados do desenho não são uma sequência temporal.", ""]
    for case_id, config in CONFIGS.items():
        opening = dict(as_of_date="2027-01-03", currency="USD", cash="60000.00", debt=config["debt"])
        payload = {"opening_position.json": encoded(opening),
                   "facility.json": (ROOT/"cases/borrowing_base_002/inputs/facility.json").read_bytes(),
                   "snapshot_dates.csv": csv_bytes("snapshot_date", [[d] for d in DATES])}
        events, invoices = [], []
        for i, (snapshot, portfolio, flows) in enumerate(zip(DATES, config["portfolios"], config["flows"]), 1):
            for direction, amount in zip(("receipt", "payment"), flows):
                events.append([f"{case_id}-W{i}-{direction}", snapshot, direction, f"{amount:.2f}", f"Scheduled operating {direction}"])
            for j, amount in enumerate(portfolio):
                customer = chr(65+j)
                # A has three distinct invoices; concentration must aggregate them.
                amounts = [f"{int(amount.split('.')[0])//3:.2f}"]*3 if case_id == "bb_customer_004" and j == 0 else [amount]
                for part, value in enumerate(amounts, 1):
                    invoices.append([snapshot, f"{customer}-{part}", customer, "2027-02-28", value, "false", "false"])
        payload["cash_events.csv"] = csv_bytes("record_id cash_date direction amount description", events)
        payload["receivables_snapshots.csv"] = csv_bytes("snapshot_date invoice_id customer_id due_date outstanding_amount disputed related_party", invoices)
        folder = ROOT/"cases"/case_id/"inputs"
        for name, data in payload.items():
            frozen(folder/name, data)
        forecast = solve(folder, case_id=case_id, opening_contract=opening)
        if forecast != compute(folder, case_id):
            raise RuntimeError(f"Integer-cent disagreement: {case_id}")
        reference = ROOT/"reference"/case_id
        frozen(reference/"forecast.json", encoded(forecast))
        counts = dict(eligibility=4+len(invoices), concentration=16+len(forecast["customer_checks"]), financing=52, violations=28)
        task = (ROOT/"cases/borrowing_base_002/task.md").read_text(encoding="utf-8")
        task = task[:task.index("## Design acceptance criteria")]
        task = task.replace("# Borrowing Base 002: Collateral-Constrained Treasury Decisions", f"# {case_id}: Collateral-Constrained Treasury Decisions")
        start, end = task.index("Status:"), task.index("## Assignment")
        task = task[:start]+"Status: calibration task/output contract v1.0. Synthetic development case.\n\n"+task[end:]
        task = task.replace("borrowing_base_002", case_id).replace("opening debt USD 150,000.00", f"opening debt USD {float(config['debt']):,.2f}")
        task = task.replace("37 eligibility, 35 concentration, 52 financing and 28 violation checks (152 total)",
                            f"{counts['eligibility']} eligibility, {counts['concentration']} concentration, 52 financing and 28 violation checks ({sum(counts.values())} total)")
        frozen(ROOT/"cases"/case_id/"task.md", task.encode("utf-8"))
        contract = schema(case_id)
        contract["title"] = case_id
        frozen(ROOT/"schemas"/f"{case_id}.schema.json", encoded(contract))
        instructions = (ROOT/"prompts/borrowing_base_002_instructions.md").read_text(encoding="utf-8").replace("Borrowing Base 002", case_id)
        frozen(ROOT/"prompts"/f"{case_id}_instructions.md", instructions.encode("utf-8"))
        agent = {f"inputs/{name}": payload[name] for name in NAMES}
        agent.update({"task.md": task.encode("utf-8"), "forecast.schema.json": encoded(contract), "agent_instructions.md": instructions.encode("utf-8")})
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_STORED) as archive:
            for name, data in sorted(agent.items()):
                info = zipfile.ZipInfo(name, (2027,1,1,0,0,0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
        package = stream.getvalue()
        with zipfile.ZipFile(io.BytesIO(package)) as archive:
            if len(archive.namelist()) != 8 or any(archive.read(name) != value for name, value in agent.items()):
                raise RuntimeError("Package verification failed")
        package_dir = ROOT/"packages"/f"{case_id}-v1.0"
        frozen(package_dir/"agent-package.zip", package)
        manifest = dict(case_id=case_id, version="1.0", package_sha256=hashlib.sha256(package).hexdigest(),
                        files={k: hashlib.sha256(v).hexdigest() for k,v in sorted(agent.items())})
        frozen(package_dir/"manifest.json", encoded(manifest))
        registry[case_id] = dict(reference_sha256=hashlib.sha256(encoded(forecast)).hexdigest(),
                                 package_sha256=manifest["package_sha256"], opening_contract=opening, checks=counts)
        verification.append(dict(case_id=case_id, status="passed", weeks=4, invoice_observations=len(invoices),
                                 customer_observations=len(forecast["customer_checks"]), input_sha256={k:hashlib.sha256(v).hexdigest() for k,v in payload.items()}))
        prose = [f"# {case_id} reference explanation", "", "Synthetic four-week contractual forecast. Snapshots size collateral; only cash_events.csv supplies receipts and payments.", ""]
        review += [f"## {case_id}", "", f"Dívida inicial: USD {config['debt']}. Verificações numéricas: {sum(counts.values())}.", "",
                   "| Fechamento | Limite | Juros | Amort. obrigatória | Amort. voluntária | Saque | Caixa final | Dívida final | Falta para mínimo | Dívida acima do limite |",
                   "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
        for w in forecast["weeks"]:
            review.append("| "+" | ".join(w[k] for k in ("snapshot_date","effective_limit","interest","actual_cure","voluntary_repayment","draw","closing_cash","closing_debt","buffer_shortfall","overadvance"))+" |")
            prose.append(f"On {w['snapshot_date']}, eligible receivables total {w['eligible']}, the customer cap is {w['concentration_threshold']}, recognized collateral is {w['recognized']} and the effective limit is {w['effective_limit']}. Events {case_id}-W{w['week']}-receipt and {case_id}-W{w['week']}-payment supply {w['receipts']} and {w['payments']}. Interest is {w['interest']}. Required/paid cure: {w['required_cure']}/{w['actual_cure']}; draw {w['draw']}; voluntary repayment {w['voluntary_repayment']}. Closing cash/debt: {w['closing_cash']}/{w['closing_debt']}; buffer gap {w['buffer_shortfall']}; overadvance {w['overadvance']}; unfunded deficit {w['cash_deficit']}.")
        notes = {
            "bb_rounding_003": "A-1, B-1 and C-1 carry cents. Floor the shared cap before applying it, and floor the advance separately. Opening debt 150002.50 produces 300.005 interest, rounded half up to 300.01. D-1 enters in week 3, increasing collateral capacity; its absence in week 4 is not a cash receipt.",
            "bb_customer_004": "A-1, A-2 and A-3 share customer A. In week 1 their total 120000 is capped at 60000, not capped separately per invoice. B-1 grows in week 2 while D-1 has zero balance and is excluded. In week 3 C-1 and D-1 grow, lifting capacity; week 4 the four customers each contribute 60000.",
            "bb_cure_005": "A-1 totals 120000 and B-1/C-1 each 40000 in weeks 1 and 3, giving a 104000 limit. In week 1 the full 46000 mandatory cure is paid but cash is 43700, below minimum by 6300. Debt equals the limit, so no draw can restore the buffer. The diversified week-2/week-4 portfolios increase capacity. Paid cure, buffer shortfall and cash deficit are separate conditions.",
            "bb_release_006": "A-1 through D-1 support the facility in weeks 1–3. The explicit final snapshot has no invoices; do not reuse prior collateral. The week-4 receipt event is 210000 and payment is 40000. After 300 interest, cash before financing is 219700: the 150000 mandatory cure fully repays debt and leaves 69700 cash. Zero collateral need not imply a deficit.",
        }
        prose += ["", notes[case_id], "", "All nonzero invoices are future-due and neither disputed nor related-party. Concentration deductions are not write-offs or cash movements. No refinancing, waiver or discretionary deferral is assumed. Weekly closing balances do not establish intraday liquidity; negative cash, if present, is diagnostic rather than an authorized overdraft."]
        frozen(reference/"analysis.md", ("\n\n".join(prose)+"\n").encode("utf-8"))
        review += ["", notes[case_id], ""]
    frozen(ROOT/"reference/calibration-v1-registry.json", encoded(registry))
    frozen(ROOT/"reference/calibration-design-review.json", encoded(dict(status="design_review_confirmed", reviewer="Tobias Hopf", confirmation="Revisados", scope="Design document and isolated examples only; complete references generated subsequently require separate review.")))
    frozen(ROOT/"reports/calibration-v1-verification.json", encoded(dict(kind="reference_crosscheck_not_model_results", cases=verification, method="Decimal reference versus integer-cent eligibility and net-position financing; full JSON equality", limitations="AI-assisted implementations, not an independent audit. Full human reference review pending.")))
    frozen(ROOT/"reports/calibration-v1-review-pt.md", ("\n".join(review)+"\n").encode("utf-8"))
    print(json.dumps(dict(cases_built=len(registry), packages_verified=len(registry))))


if __name__ == "__main__":
    build()
