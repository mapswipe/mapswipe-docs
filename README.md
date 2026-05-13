# MapSwipe Docs!

This repository contains all the documents related to MapSwipe

- [Overview](/docs/overview.md)
- [About Data](/docs/about_data.md)
- [For project managers](/docs/for_project_managers.md)

## Getting Started

```bash
# Get the repository
git clone https://github.com/mapswipe/mapswipe-docs

# Install jekyll
gem install jekyll bundler --verbose

# Install dependencies
bundle install
```

> [!IMPORTANT]
> Run this after changing the Gemfile

## Run Docs in Dev Mode

```bash
bundle exec jekyll serve --livereload
```

## Refreshing the Sample Export Data

The point of this workflow is to keep the example exports under
`assets/docs/about_data/files/` consistent. Once exports are updated, the data
can also be used to keep the description for exports up-to-date.

Two helper scripts under `examples/` fetch the data from the MapSwipe GraphQL backend.

### Fetch Project Exports

```bash
uv run examples/fetch-project-data/run.py 2962 \
  --sample 10 \
  --out assets/docs/about_data/files/project_exports
```

### Fetch Global Exports

```bash
uv run examples/fetch-global-data/run.py \
  --sample 10 \
  --out assets/docs/about_data/files/global_exports
```

### Projects Mapping

| Name | id | firebaseId |
| --- | --- | --- |
| Find Features - Find Buildings - Mozambique Floods 2026 - Chibuto (1) HOT | 2962 | 01KMMX0C9MG396SCV8W8CZ8RY3 |


## Changing the Syntax Highlighting Theme

Fenced code blocks are colored by [Rouge](https://github.com/rouge-ruby/rouge),
wired into CommonMark via `syntax_highlighter: rouge` in `_config.yml`. The
active theme is generated to `assets/css/syntax.css`.

To switch themes, run the following commands:

```bash
# List every theme Rouge ships with
bundle exec rougify help style

# Regenerate the stylesheet
bundle exec rougify style gruvbox.dark > assets/css/syntax.css
```
