#!/bin/bash -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_success() {
    echo -e "${GREEN}$1${NC}"
}

log_error() {
    echo -e "${RED}$1${NC}"
}

log_warning() {
    echo -e "${YELLOW}$1${NC}"
}


if ! command -v pre-commit &>/dev/null; then
  log_error "pre-commit is not installed."
  log_error "Follow https://pre-commit.com/#installation"
  exit 1
fi

if ! command -v lychee &>/dev/null; then
  log_error "lychee is not installed."
  log_error "Follow https://github.com/lycheeverse/lychee#installation"
  exit 1
fi

echo "▶️ Running pre-commit"
pre-commit run --color=always --all-files

echo "▶️ Running lychee"
lychee --root-dir $(pwd)/ ./

log_success "✅ All good"
