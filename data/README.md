# Data

The original `event_log.xes` file is not included in this portfolio repository.

To reproduce the analysis, place the assignment dataset here as:

```text
data/event_log.xes
```

The analysis expects at least these columns after PM4Py imports the XES log:

- `case_id`
- `activity`
- `time:timestamp`

The optional `resource` field is used for descriptive statistics when available.

Do not publish a university-provided or third-party dataset unless its license or assignment terms allow redistribution.
