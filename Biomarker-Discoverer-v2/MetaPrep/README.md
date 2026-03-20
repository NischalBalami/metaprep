# MetaPrep

A Python pipeline for processing raw mass spectrometry peaklist data. Built to handle the messy output from tools like Compound Discoverer and turn it into a clean, aligned feature table ready for statistical analysis.

## What it does

Takes raw `.xlsx` peaklist files (one per sample) and runs them through four steps:

1. **Clean** — drops missing values, standardizes column names, cleans up retention time formatting
2. **Group** — merges duplicate peaks that fall within m/z and RT thresholds, sums their intensities
3. **Combine** — stacks all grouped files into one dataset with sample tracking
4. **Align** — builds a feature table comparing every molecule's intensity across all samples

The final output is a single spreadsheet where rows = unique molecules and columns = intensity per sample. From there you can run stats, make plots, or look things up in HMDB.

## How to use

Install dependencies:
```
pip install -r requirements.txt
```

Put your raw `.xlsx` files in `data/raw/`, then:
```
cd scripts
python run_pipeline.py
```

Or use the interactive menu for step-by-step control:
```
cd scripts
python main.py
```

### Thresholds

The grouping and alignment steps use two thresholds you can adjust:

- **m/z threshold** (default 0.001) — how close two m/z values need to be to count as the same molecule
- **RT threshold** (default 30 seconds) — how close retention times need to be

## Requirements

- Python 3.8+
- pandas
- numpy
- openpyxl