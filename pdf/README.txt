PDF render skill test results

Updated default rendering method:
- pdftocairo first
- pdftoppm fallback
- pdf2image legacy fallback

Included artifacts:
- updated_skill/: amended skill files
- test_pdfs/: validated sample PDFs used during testing
- render_samples/: rendered PNG contact sheets/crops used for QA

Validated scenarios:
- complex PDF with styled tables, charts, and images
- single-page table with very long wrapped text in cells
- multi-page stress test with many images and very long flowing text
- corrected image scaling to preserve aspect ratio in the test PDF
