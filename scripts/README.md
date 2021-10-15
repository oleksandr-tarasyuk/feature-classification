# Scripts documentation

## Tagging review tool

### Instructions:

- Copy the file at ```/fileserver1/ces/files/products.pkl``` to your environment
- Replace ```PKL_PATH``` variable at db_selection.py main to your new location
- Run from Repo root:
```bash
streamlit run scripts/db_selection.py
```

### TO DO

- More efficient loops when processing the order:
  - [Aggregation on pipeline](https://github.com/GoldenspearLLC/feature-classification/pull/1#discussion_r727795895)
  - [Join different loops](https://github.com/GoldenspearLLC/feature-classification/pull/1#discussion_r724755395)