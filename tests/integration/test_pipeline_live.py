from .twitter_api import run_pipeline

def test_run_pipeline_sevdesk_live():
    run_pipeline(keyword="sevdesk", page_max=3)

def test_run_pipeline_accounting_live():
    run_pipeline(keyword="accounting", page_max=3, max_results=0)

def test_run_pipeline_invoice_live():
    run_pipeline(keyword="invoice", page_max=2, max_results=10)

def test_run_pipeline_ksedves_live():
    run_pipeline(keyword="ksedves", page_max=3)
