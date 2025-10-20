from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime, timedelta
import random, os

ISSUERS = [
    ("chase_sample.pdf", "Chase", ["Chase Sapphire Preferred"], "1234"),
    ("amex_sample.pdf", "American Express", ["AMEX Gold"], "5678"),
    ("citi_sample.pdf", "Citi", ["Citi Rewards"], "9012"),
    ("capitalone_sample.pdf", "Capital One", ["Capital One Venture"], "3456"),
    ("discover_sample.pdf", "Discover", ["Discover it"], "7890"),
]

def mk_pdf(path, issuer, product, last4, start, end, due, balance, n_tx=8):
    c = canvas.Canvas(path, pagesize=LETTER)
    W, H = LETTER
    c.setFont("Helvetica-Bold", 16); c.drawString(72, H-72, f"{issuer}")
    c.setFont("Helvetica", 11)
    c.drawString(72, H-90, f"Product: {product}")
    c.drawString(72, H-108, f"Account Ending {last4}")
    c.drawString(72, H-126, f"Statement Period: {start.strftime('%b %d, %Y')} to {end.strftime('%b %d, %Y')}")
    c.drawString(72, H-144, f"Payment Due Date: {due.strftime('%b %d, %Y')}")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(72, H-171, f"Statement Balance: ${balance:,.2f}")

    y = H-198
    c.setFont("Helvetica-Bold", 11); c.drawString(72, y, "Date"); c.drawString(166, y, "Description"); c.drawString(468, y, "Amount")
    y -= 18
    c.setFont("Helvetica", 10)
    for i in range(n_tx):
        tdate = start + timedelta(days=random.randint(0, (end-start).days))
        desc = random.choice(["COFFEE SHOP", "ONLINE STORE", "GROCERY MART", "FUEL STATION", "APP SUBSCRIPTION", "BOOKS"])
        amt = round(random.uniform(3.5, 120.0), 2) * random.choice([1,1,1,-1])
        c.drawString(72, y, tdate.strftime('%m/%d/%Y'))
        c.drawString(166, y, desc)
        c.drawRightString(560, y, f"${amt:,.2f}")
        y -= 16
        if y < 72:
            c.showPage(); y = H-90
    c.showPage(); c.save()

if __name__ == "__main__":
    now = datetime(2025, 10, 1)
    start = now.replace(day=1)
    end = now.replace(day=30)
    due = now.replace(day=25)
    base = os.path.dirname(__file__)
    for fname, issuer, products, last4 in ISSUERS:
        bal = round(random.uniform(250.0, 2500.0), 2)
        mk_pdf(os.path.join(base, fname), issuer, products[0], last4, start, end, due, bal)
