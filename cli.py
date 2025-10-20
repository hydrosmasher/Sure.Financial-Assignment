import argparse, os, glob, json
from rich.console import Console
from rich.table import Table
from ccparser import parse_pdf

console = Console()

def parse_one(path: str):
    res = parse_pdf(path)
    return res

def print_pretty(res, path):
    table = Table(title=f"Parsed: {os.path.basename(path)}  [provider={res.meta.get('provider')}]")
    table.add_column("Field")
    table.add_column("Value")
    table.add_column("Confidence")
    for k in ["issuer","card_last4","billing_start","billing_end","due_date","statement_balance"]:
        field = getattr(res, k)
        table.add_row(k, str(field.value), f"{field.confidence:.2f}")
    console.print(table)

    if res.transactions:
        t = Table(title="Transactions")
        t.add_column("Date", justify="center")
        t.add_column("Description")
        t.add_column("Amount", justify="right")
        for tx in res.transactions:
            t.add_row(tx.date, tx.description, f"{tx.amount:.2f}")
        console.print(t)

def main():
    ap = argparse.ArgumentParser(description="Credit Card Statement Parser")
    ap.add_argument("path", help="PDF file or folder")
    ap.add_argument("--pattern", default="*.pdf", help="glob pattern when path is a folder")
    ap.add_argument("--json", help="write single result JSON to file (file input only)")
    ap.add_argument("--outdir", help="write JSON files next to PDFs (folder input)")
    ap.add_argument("--show", action="store_true", help="print pretty tables")
    args = ap.parse_args()

    if os.path.isdir(args.path):
        pdfs = glob.glob(os.path.join(args.path, args.pattern))
        os.makedirs(args.outdir or "parsed", exist_ok=True)
        for p in pdfs:
            res = parse_one(p)
            if args.show:
                print_pretty(res, p)
            outp = os.path.join(args.outdir or "parsed", os.path.splitext(os.path.basename(p))[0] + ".json")
            with open(outp, "w") as f:
                f.write(res.model_dump_json(indent=2))
        console.print(f"[green]Wrote {len(pdfs)} JSON files to {args.outdir or 'parsed'}[/green]")
    else:
        res = parse_one(args.path)
        if args.show:
            print_pretty(res, args.path)
        if args.json:
            with open(args.json, "w") as f:
                f.write(res.model_dump_json(indent=2))
        else:
            console.print_json(res.model_dump())

if __name__ == "__main__":
    main()
