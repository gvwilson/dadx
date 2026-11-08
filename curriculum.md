# Data Analysis Design by Example — Curriculum

Twenty hour-long lessons, each of which builds a small version of a real data
analysis pipeline — a pipeline of a *qualitatively different kind* from the one
before — or one of two synthetic data generators that later lessons rely on.
The generators simulate software development and operations, the lessons use
mature tools rather than rebuilding them, they follow the same assumptions as
the [project README](./README.md), and they thread a single running example — a
web service and the software that builds and operates it — through all of them.

## The Lessons

1.  [Introduction](intro)
1.  [An Event Log Generator](gen-eventlog)
1.  [Your First Pipeline](pipeline)
1.  [Data Dictionaries and Provenance](management)
1.  [A Data Cleaning Pipeline](cleaning)
1.  [An Operational Metrics Generator](operational-gen)
1.  [A Cohort and Retention Pipeline](retention)
1.  [A Funnel Pipeline](funnel)
1.  [An A/B Test Pipeline](ab-test)
1.  [A Forecasting Pipeline](forecasting)
1.  [A Linear Regression Pipeline](regression)
1.  [A Classification Pipeline](classification)
1.  [A Similarity Pipeline](similarity)
1.  [A Text Analysis Pipeline](text-analysis)
1.  [A SQL Pipeline with DuckDB](db-pipe)
1.  [An ETL Pipeline from the Web](etl)
1.  [An Anomaly and Monitoring Pipeline](anomaly)
1.  [A Clustering Pipeline](clustering)
1.  [A Reproducible Pipeline](reproducible)
1.  [Conclusion](finale)

## In Detail

### 1. Introduction

The best way to learn data analysis is to study examples, so these lessons
build small versions of real analysis pipelines — each of a different kind —
rather than reimplementing the tools those pipelines use. This lesson defines
what a pipeline is (ingest, clean, explore, model, communicate), introduces the
running example — a web service and its operations — and sets the through-line:
we use mature tools and build analyses, not libraries.

-   A data analysis pipeline is a chain of small, checkable steps.
-   There are many kinds of analysis; this course samples them rather than
    drilling one.
-   We use mature tools (Polars, DuckDB, Vega-Altair, httpx) instead of
    rebuilding them.
-   Reproducibility means recording every step so an analysis can be re-run
    and audited.

### 2. An Event Log Generator

Build the primary dataset: a web service's event stream — a table of users and
a table of events (requests, signups, deployments, errors) linked to them by
user ID, generated from seeded randomness and written as CSV. This is the first
of two generators; later lessons analyze its output and can check their answers
against the truth it encodes.

-   A seed makes pseudo-random numbers reproducible.
-   Synthetic events let us know the "right answer" (for example, which version
    was slower).
-   A generator documents the assumptions baked into the data.
-   CSV is a simple, portable exchange format.

### 3. Your First Pipeline

Build a small end-to-end exploratory pipeline: read the event log, clean the
obvious problems, summarize it (requests per endpoint, latency, error rate),
and plot the result. Along the way, meet the tools this course relies on —
reading CSV, selecting and filtering columns, grouping and joining, reshaping,
and computing basic statistics — as libraries to call, not things to
reimplement.

-   A pipeline is ingest → clean → explore → summarize → communicate.
-   Polars reads CSVs and does select, filter, group, join, and reshape for us.
-   Basic descriptive statistics come from the library, not hand-rolled code.
-   Every pipeline ends by checking its answer, ideally against known truth.

### 4. Data Dictionaries and Provenance

Build the metadata layer of a pipeline: a data dictionary that records each
field's name, type, units, meaning, and allowed values — for fields such as
`timestamp`, `endpoint`, `status_code`, and `latency_ms` — and a provenance log
that records each step's inputs and outputs.

-   Metadata (data about data) is data too.
-   A data dictionary is a contract between producer and consumer.
-   Provenance lets someone reconstruct how a result was derived.
-   Reproducibility is impossible without provenance.

### 5. A Data Cleaning Pipeline

Build a cleaning pipeline that profiles the raw event log, deduplicates
records, normalizes status codes and endpoint names, fills missing values, and
validates the result — emitting a clean dataset and a data-quality report.
Cleaning is its own kind of analysis: quality assurance.

-   Cleaning is a pipeline of small, testable transformations.
-   Profiling first (types, ranges, missingness) tells you what needs fixing.
-   Deduplication needs a notion of "same record".
-   Every change is documented so clean data can be traced to raw data.

### 6. An Operational Metrics Generator

Build a generator that produces time-series metrics for the service — request
rate, error rate, latency percentiles, CPU, and memory — with trend,
seasonality, noise, and a few injected anomalies, so the forecasting and
monitoring lessons have known targets to find.

-   A time series is trend plus seasonality plus noise.
-   Because we choose the components, we know the true signal.
-   Injected anomalies give the monitoring lesson known targets to recover.

### 7. A Cohort and Retention Pipeline

Build a pipeline that groups users into cohorts by signup month and computes
how many of each cohort return in each later month — the retention curve. A
distinct kind of analysis: behavior over time, by group.

-   A cohort shares a defining event; retention tracks its members over time.
-   Grouping by cohort and period is a table joined to itself.
-   Retention answers "do users come back?", not just "how many signed up?".
-   Check counts against hand-computed small examples.

### 8. A Funnel Pipeline

Build a pipeline that traces users through a sequence of stages — signup,
activation, first deploy, paid plan — and reports the drop-off at each one. A
distinct kind of analysis: funnel and conversion analysis.

-   A funnel orders stages and measures conversion between them.
-   Each stage is a filter; drop-off is the complement.
-   Funnels reveal where a process loses users.
-   Stage order and definition change the answer — document them.

### 9. An A/B Test Pipeline

Build a pipeline that compares two feature variants (for example, a redesigned
page or a backend change) with a permutation test and a bootstrap confidence
interval for the effect on latency or conversion. A distinct kind of analysis:
experimentation and inference.

-   The null hypothesis is "no real difference"; shuffling labels simulates it.
-   A p-value is how often shuffles look as extreme as the real data.
-   The bootstrap puts a confidence interval around an effect size.
-   Simulated inference replaces closed-form math we may not know.

### 10. A Forecasting Pipeline

Build a pipeline that fits simple trend and seasonal models to operational
metrics and evaluates them by forecasting the held-out recent past
(backtesting). A distinct kind of analysis: forecasting.

-   A forecast is an extrapolation, and its error grows with the horizon.
-   Naive and seasonal baselines give a floor to beat.
-   Backtesting holds out the recent past to judge a model.
-   Forecast uncertainty matters as much as the point forecast.

### 11. A Linear Regression Pipeline

Build a least-squares regression pipeline: fit a line to predict a numeric
outcome — request latency from load and payload size, or build time from code
size — inspect the residuals, and evaluate the fit on held-out data. A distinct
kind of analysis: predictive modeling with a continuous outcome.

-   Least squares minimizes the sum of squared residuals.
-   Coefficients have concrete, checkable meanings.
-   Residuals reveal what the model misses.
-   A fitted line is a claim, not a fact — evaluate it on unseen data.

### 12. A Classification Pipeline

Build a pipeline that predicts a category — will this request fail with a 5xx,
or will this build fail? — from its features, and judge it with a confusion
matrix and the right metric. A distinct kind of analysis: predictive modeling
with a categorical outcome.

-   Classification predicts a label, not a number.
-   A confusion matrix shows the kinds of errors a classifier makes.
-   Accuracy alone misleads when classes are imbalanced.
-   The right metric depends on the cost of each kind of error.

### 13. A Similarity Pipeline

Build a pipeline that finds the records most like a given one — similar error
reports, similar services, or similar users — under some distance on chosen
features. A distinct kind of analysis: nearest-neighbor and similarity analysis.

-   "Similar" means close under some distance on chosen features.
-   Feature choice and scaling decide what similarity means.
-   Nearest neighbors generalize from "equal" to "nearby".
-   Similarity underpins recommendation and record linkage.

### 14. A Text Analysis Pipeline

Build a pipeline that tokenizes commit messages or issue titles, counts terms,
and scores documents with TF-IDF to find what distinguishes them. A distinct
kind of analysis: text mining.

-   Tokenization and normalization turn free text into countable units.
-   Term frequency is a start; TF-IDF down-weights common terms.
-   A document becomes a vector of term weights.
-   Text pipelines need the same cleaning and validation as numeric ones.

### 15. A SQL Pipeline with DuckDB

Build the same analytical workflow over the event log and users in declarative
SQL using DuckDB, and see how a columnar engine differs from dataframe code. A
distinct kind of analysis: relational and declarative.

-   SQL says what you want; the engine decides how to compute it.
-   SELECT, WHERE, GROUP, and JOIN mirror the dataframe operations already
    used.
-   DuckDB's columnar engine is optimized for analytical queries.
-   Two mental models — dataframe and relational — solve the same problems.

### 16. An ETL Pipeline from the Web

Build an ingestion pipeline that fetches a repository's issues or commits (or a
CI status feed) from a public API with httpx, transforms it, and loads it into
DuckDB — handling pagination, rate limits, and caching. A distinct kind of
analysis: extract, transform, load.

-   ETL is ingest → transform → load, and the ingest step is often the web.
-   httpx fetches; we add pagination, rate limits, and caching around it.
-   Cache responses so re-runs don't re-fetch (or re-bill) the source.
-   A mock server lets us test the pipeline offline.

### 17. An Anomaly and Monitoring Pipeline

Build a pipeline that flags unusual values and detects drift in operational
metrics using z-scores and simple control rules. A distinct kind of analysis:
monitoring and anomaly detection.

-   An anomaly is an observation far from what a model expects.
-   Z-scores and rolling statistics define "expected" and "far".
-   Drift means the data's baseline itself is moving.
-   Monitoring runs continuously, so it must be cheap and logged.

### 18. A Clustering Pipeline

Build a pipeline that groups records into segments — services by traffic
pattern, or users by behavior — with a simple k-means routine and interprets
what each cluster means. A distinct kind of analysis: unsupervised
segmentation.

-   Clustering groups records without predefined labels.
-   k-means alternates assignment and centroid updates until stable.
-   The algorithm finds structure, not meaning — interpret the clusters.
-   Validate by asking whether clusters are stable and useful.

### 19. A Reproducible Pipeline

Build a runner that records each step's inputs and outputs and re-runs only the
steps whose inputs changed, tying provenance and orchestration together. The
meta-pipeline that manages the others.

-   Pipeline steps form a directed graph of dependencies.
-   A runner re-executes only the steps that are stale.
-   A recorded pipeline is a reproducible pipeline.
-   This is how real tools manage analyses end-to-end.

### 20. Conclusion

Recap the through-line: each lesson built a small version of a real pipeline of
a different kind, using mature tools rather than rebuilding them. The habits —
verify, document, reproduce — matter more than any single technique, and are
what to carry into whatever comes next.
