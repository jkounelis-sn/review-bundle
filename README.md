# vendor-corpus-tools

Validation and review tooling around the vendored abbreviation corpus
(`deps/corpus`, mirrored from the vendor-corpus dataset repo).

## Quickstart

    make setup test

## Reviewing a corpus refresh

The vendored corpus versions independently of this repo, so sync it
before reviewing or you'll diff stale content:

    make sync-corpus        # == git -C deps/corpus pull
    corpus-tool sync-status
    corpus-tool validate

See REVIEW_GUIDE.md for the full checklist.
