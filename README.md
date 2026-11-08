# Data Analysis Design by Example

The best way to learn design in any field is to study examples.
These lessons therefore build small versions of real data analysis pipelines
to introduce some fundamental ideas in data science
and show how experienced data scientists think.

## Assumptions

-   Learners are going to learn and code with AI tools
    -   So focus on mental models and good practices rather than syntactic minutiae
-   Learners have high-school understanding of mathematics and statistics
-   Learners have CS-1 undertanding of Python (loops, conditionals, functions, lists, dictionaries)
-   Learners are *not* familiar with a command-line shell or version control

## Pedagogy

-   Each hour-long lesson builds a different kind of data analysis pipeline
-   *Or* a synthetic data generator to use in subsequent lessons
    -   Only have a few of these: multiple lessons may rely on a single data generator
-   Show how to verify and validate data analysis pipelines
-   Show how to manage data (e.g., provenance, data dictionaries)

## Tooling

-   [Bram][bram]: mindful harness for managing AI interactions
-   [Git][git]: version control is our friend
-   [Python][python]: more widely used than R
-   [uv][uv]: Python package and environment management
-   [ruff][ruff]: Python code checks and formatting
-   [doit][doit]: dependency-driven task runner used in lessons (not for managing this site)
-   [Narwhals][narwhals]: common operations on data frames
-   [Polars][polars]: underlying dataframe engine
-   [DuckDB][duckdb]: optimized for OLAP rather than OLTP
-   [Vega-Altair][vega-altair]: data visualization
-   [httpx][httpx]: HTTP client

[bram]: https://judell.github.io/bram/
[doit]: https://pydoit.org/
[duckdb]: https://duckdb.org/
[git]: https://git-scm.com/
[httpx]: https://www.python-httpx.org/
[narwhals]: https://narwhals-dev.github.io/narwhals/
[polars]: https://pola.rs/
[python]: https://www.python.org/
[ruff]: https://docs.astral.sh/ruff/
[uv]: https://docs.astral.sh/uv/
[vega-altair]: https://altair-viz.github.io/
