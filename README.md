# MLOps Data Pipeline Write-Up

## Pipeline Steps
My `etl.py` script does three things:
1. **Ingestion**: Grabs `data/raw/transactions.csv` and loads it into a pandas DataFrame.
2. **Cleaning**: Drops rows with missing values. In the `experiment-feature` branch, it also skips rows where `quantity` isn’t above 0.
3. **Feature Engineering**: Adds a `total_amount` column by multiplying `quantity` and `price`.

The cleaned data lands in `data/processed/transactions_clean.csv`.

## DVC for Data Tracking
I used DVC to keep track of data:
- Added `data/raw/transactions.csv` with `dvc add`, which made `transactions.csv.dvc`.
- Tracked `data/processed/transactions_clean.csv` after running `etl.py`.
- Added a new row to `transactions.csv` and updated it with `dvc add`.
- To test rollback, I used `git checkout` to go back to an earlier commit and `dvc checkout` to restore the original 5-row `transactions.csv`.

## Challenges and Fixes
- **Issue**: Python 3.13 didn’t have pandas and threw errors due to some system restriction.
- **Fix**: Switched to Python 3.11, which had pandas ready to go.
- **Issue**: DVC complained that `.dvc` files were ignored by Git.
- **Fix**: Tweaked `.gitignore` to allow `.dvc` and `.gitignore` files in `data/`.
- **Issue**: The ETL script crashed because `data/processed/` didn’t exist.
- **Fix**: Made the folder with `mkdir -p data/processed`.

## Notes
The `experiment-feature` branch tests a new cleaning rule (`quantity > 0`). Everything’s stored locally, no remote needed. Python 3.11 kept things simple.

## Discussion Questions
1. **What if the dataset was huge (GBs or TBs) and updated daily?**  
I’d store data on S3 using `dvc remote add` since local storage would choke. Daily updates would need a script to auto-run `dvc add` and `git commit`, maybe on a schedule.

2. **How could you check data quality before adding it?**  
I’d add checks in `etl.py` to spot duplicates, negative values, or missing columns. Printing `df.info()` could catch issues early.

3. **How to handle conflicts with multiple collaborators?**  
Everyone would work on separate Git branches to avoid stepping on toes. For data, one person would handle `dvc add` to keep it consistent. For `etl.py`, we’d use Git to merge changes and test the pipeline together.