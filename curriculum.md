# Data Analysis Design by Example — Curriculum

Twenty hour-long lessons, each of which builds a small version of a real data
analysis pipeline — or one of a few synthetic data generators that later
lessons rely on. The lessons follow the same assumptions and use the same
tools as the [project README](./README.md), and a single running example — a
small clinic's patient and visit records — threads through all of them.

## The Lessons

1.  [Introduction](#1-introduction)
1.  [A Synthetic Data Generator](#2-a-synthetic-data-generator)
1.  [Reading Data](#3-reading-data)
1.  [Dataframes](#4-dataframes)
1.  [Cleaning Data](#5-cleaning-data)
1.  [Data Dictionaries and Provenance](#6-data-dictionaries-and-provenance)
1.  [Grouping and Aggregation](#7-grouping-and-aggregation)
1.  [Joining Tables](#8-joining-tables)
1.  [Reshaping Data](#9-reshaping-data)
1.  [Descriptive Statistics](#10-descriptive-statistics)
1.  [A Second Data Generator (Time Series)](#11-a-second-data-generator-time-series)
1.  [Visualization](#12-visualization)
1.  [SQL and DuckDB](#13-sql-and-duckdb)
1.  [Sampling and the Bootstrap](#14-sampling-and-the-bootstrap)
1.  [Simulation and Hypothesis Testing](#15-simulation-and-hypothesis-testing)
1.  [Linear Regression](#16-linear-regression)
1.  [Model Evaluation](#17-model-evaluation)
1.  [Fetching Data from the Web](#18-fetching-data-from-the-web)
1.  [A Reproducible Pipeline](#19-a-reproducible-pipeline)
1.  [Conclusion](#20-conclusion)

## In Detail

### 1. Introduction

The best way to learn data analysis is to study examples, so these lessons
build small versions of real analysis pipelines rather than memorizing
functions. This lesson defines what a pipeline is — ingest, clean, explore,
model, communicate — introduces the running example, and explains why
reproducibility, the ability to re-run an analysis and get the same answer, is
the through-line of the whole course.

-   A data analysis pipeline is a chain of small, checkable steps.
-   A worked example teaches mental models that memorizing syntax cannot.
-   Learners will code with AI tools, so the goal is good practices, not
    syntactic minutiae.
-   Reproducibility means recording every step so an analysis can be re-run
    and audited.

### 2. A Synthetic Data Generator

Build the clinic dataset: a table of patients with a few demographic
attributes, and a table of visits linked to them by patient ID. Seeded random
number generation makes the output reproducible, and writing it as CSV makes
it portable. This is the first of two generators; later lessons analyze its
output.

-   A seed makes pseudo-random numbers reproducible.
-   Synthetic data lets us know the "right answer" when testing a pipeline.
-   A generator documents the assumptions baked into the data.
-   CSV is a simple, portable exchange format.

### 3. Reading Data

Build a small CSV reader that turns text into a dataframe, guessing each
column's type and marking missing values. This is the first step of every
pipeline, and it is where data usually starts to go wrong.

-   Parsing is distinct from the data structure it produces.
-   Type inference is a guess, and it can be wrong.
-   Missing values need an explicit representation (for example, null or NaN).
-   Validate the read: count rows, check types, and look at a sample.

### 4. Dataframes

Build a minimal dataframe that supports select, filter, and equality, storing
data row-wise and then column-wise, using Narwhals over Polars as the engine.
Compare the two storage strategies the way a data engineer would.

-   A dataframe is a table with named columns and many rows.
-   Row-wise and column-wise storage suit different workloads (OLTP vs OLAP).
-   A shared interface lets us swap engines without rewriting analysis code.
-   Measure, don't guess, when choosing between implementations.

### 5. Cleaning Data

Build a cleaning pipeline: fill or drop missing values, normalize categorical
labels, flag or clip outliers, and standardize units. Every step is a small,
testable transformation with a record of what changed.

-   Cleaning is a pipeline of small transformations, not one big step.
-   Each transformation should be checkable in isolation.
-   Missing data is handled by an explicit, justified policy.
-   Document every change so cleaned data can be traced back to raw data.

### 6. Data Dictionaries and Provenance

Build a data dictionary — name, type, units, meaning, and allowed values for
each field — and a provenance log that records each transformation, its
inputs, and its outputs.

-   Metadata (data about data) is data too.
-   A data dictionary is a contract between producer and consumer.
-   Provenance lets someone reconstruct how a result was derived.
-   Reproducibility is impossible without provenance.

### 7. Grouping and Aggregation

Build group-by and summarize: split rows into groups by a key, apply an
aggregation function to each group, and combine the results into a new
dataframe.

-   Split-apply-combine is the core pattern of aggregation.
-   Aggregation functions are values that can be passed around.
-   A grouped summary is itself a dataframe and can be analyzed further.
-   Check aggregates against hand-computed values.

### 8. Joining Tables

Build inner and left joins to combine patients with their visits. Explains
keys, cardinality, and why an index makes a join fast.

-   Keys relate rows in one table to rows in another.
-   Cardinality (one-to-one, one-to-many, many-to-many) determines the
    result's shape.
-   A join is a nested search that an index can accelerate.
-   Check join results by counting rows before and after.

### 9. Reshaping Data

Build pivot (long to wide) and melt (wide to long) to move between "tidy" and
spreadsheet layouts.

-   Tidy data puts one observation per row and one variable per column.
-   Wide and long forms make different questions easy to ask.
-   Reshaping must not lose or invent data.

### 10. Descriptive Statistics

Build mean, median, variance, standard deviation, quantiles, and a histogram,
and show what each reveals — and hides — about a distribution.

-   A single summary number discards information.
-   The mean is sensitive to outliers; the median is robust.
-   A histogram shows the distribution that a summary cannot.
-   Plot the data before summarizing it.

### 11. A Second Data Generator (Time Series)

Build a generator that produces time-series measurements — daily values with
trend, seasonality, and noise — so later lessons can explore relationships
and uncertainty. This is the second generator; because we choose its
components, we know the true signal it hides.

-   A time series is trend plus seasonality plus noise.
-   Because we choose the components, we know the true signal.
-   Generated correlations let us test whether an analysis recovers a known
    relationship.

### 12. Visualization

Build charts with Vega-Altair using the grammar of graphics: scatter, line,
bar, and histogram plots that map data columns to visual channels.

-   A plot maps data columns to visual channels (x, y, color, size).
-   Different chart types answer different questions.
-   Anscombe's quartet shows why plotting beats summary statistics.
-   Visualization is a check on every other step of the pipeline.

### 13. SQL and DuckDB

Query the clinic data with SQL using DuckDB, translating the dataframe
operations from earlier lessons into declarative queries and seeing how a
columnar OLAP engine executes them.

-   SQL is declarative: say what you want, not how to compute it.
-   SELECT, WHERE, GROUP, and JOIN mirror the operations already learned.
-   Columnar engines such as DuckDB are optimized for analytical queries.
-   The same data can be approached with two different mental models.

### 14. Sampling and the Bootstrap

Build random sampling and the bootstrap to estimate the uncertainty around a
statistic such as a mean or median without needing formulas.

-   A sample estimates a population parameter with some error.
-   Resampling with replacement simulates drawing new samples.
-   The spread of bootstrap estimates approximates the statistic's
    uncertainty.
-   A confidence interval is read off the bootstrap distribution.

### 15. Simulation and Hypothesis Testing

Build a permutation test to compare two groups (for example, two treatments)
and estimate a p-value by simulation.

-   The null hypothesis is "no real difference."
-   Permuting group labels simulates what we would see under the null.
-   A p-value is how often random shuffles look as extreme as the real data.
-   Simulation replaces closed-form math we may not know.

### 16. Linear Regression

Build least-squares linear regression: fit a line to predict one numeric
column from another, compute residuals, and interpret the coefficients.

-   Least squares minimizes the sum of squared residuals.
-   Slope and intercept have concrete, checkable meanings.
-   Residuals show what the model fails to explain.
-   A fitted line is a claim, not a fact.

### 17. Model Evaluation

Build train/test split and cross-validation, and measure generalization with
RMSE (and accuracy for classification) to detect overfitting.

-   A model that memorizes the data fails on new data.
-   A holdout set estimates performance on unseen data.
-   Cross-validation uses data more efficiently.
-   The evaluation metric must match the question being asked.

### 18. Fetching Data from the Web

Build an HTTP client with httpx that fetches JSON from a public API, handling
pagination, rate limits, and caching, and test it against a mock server.

-   APIs return structured (usually JSON) data over HTTP.
-   Respect rate limits and pagination when reading from an API.
-   Cache responses so the analysis can be re-run without re-fetching.
-   A mock server makes network code testable offline.

### 19. A Reproducible Pipeline

Build a pipeline runner that records each step's inputs and outputs and
re-runs only the steps whose inputs changed, tying provenance and pipeline
together.

-   Pipeline steps form a directed graph of dependencies.
-   A runner re-executes only the steps that are stale.
-   A recorded pipeline is a reproducible pipeline.
-   This is how real tools (and build systems) manage analyses.

### 20. Conclusion

Recap the through-line: each lesson built a small version of a real tool, and
together they compose into a reproducible analysis. The habits — verify,
document, reproduce — matter more than any single technique, and are what to
carry into whatever comes next.
