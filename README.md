# MapSwipe Docs!

This repository contains all the documents related to MapSwipe

- [Overview](/docs/overview.md)
- [About Data](/docs/about_data.md)
- [For project managers](/docs/for_project_managers.md)

## Getting started

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

## Run docs in dev mode

```bash
bundle exec jekyll serve --livereload
```

## Changing the syntax highlighting theme

Fenced code blocks are colored by [Rouge](https://github.com/rouge-ruby/rouge), wired into CommonMark via `syntax_highlighter: rouge` in `_config.yml`. The active theme is generated to `assets/css/syntax.css`.

To switch themes, run the following commands:

```bash
# List every theme Rouge ships with
bundle exec rougify help style

# Regenerate the stylesheet
bundle exec rougify style gruvbox.dark > assets/css/syntax.css
```
