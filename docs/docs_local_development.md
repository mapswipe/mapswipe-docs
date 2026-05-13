---
title: Local Development
nav_order: 99
permalink: /docs/docs_local_development/
---

# Local Development

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
