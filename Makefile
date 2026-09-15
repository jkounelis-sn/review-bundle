.PHONY: setup test lint sync-corpus review

setup:
	python3 -m venv .venv && .venv/bin/pip install -e ".[dev]"

test:
	python3 -m pytest tests/ -q

lint:
	python3 -m compileall -q src tests

# Vendored corpus sync: the corpus versions independently, so pull the
# vendored mirror before validating or you will review stale content.
sync-corpus:
	git -C deps/corpus pull

review: sync-corpus test
	python3 -m corpus_tools.cli validate
