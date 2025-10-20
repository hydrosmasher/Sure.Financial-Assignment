from ccparser import parse_pdf
import os

def test_samples_parse():
    here = os.path.dirname(__file__)
    samples = os.path.join(os.path.dirname(here), "samples")
    for name in ["chase_sample.pdf","amex_sample.pdf","citi_sample.pdf","capitalone_sample.pdf","discover_sample.pdf"]:
        p = os.path.join(samples, name)
        res = parse_pdf(p)
        assert res.issuer.value
        assert res.due_date.value
        assert res.statement_balance.value
