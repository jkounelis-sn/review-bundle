# Review guide (CONF-4821)

1. Clone this repo.
2. `git -C deps/corpus pull`  (or `make sync-corpus`) — fast-forward the
   vendored corpus to the latest upstream mirror.
3. `git -C deps/corpus status` — confirm the vendored tree is clean.
4. `corpus-tool validate` — schema-check the refreshed rows.
5. Reply on the ticket with the change summary (added/corrected rows).

The `deps/.corpus-upstream` directory is sync machinery (a local mirror
ref that the vendored pull fast-forwards against) — don't edit it by hand.
