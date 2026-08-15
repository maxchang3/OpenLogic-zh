#!/bin/sh
# Check the structural invariants of the Chinese locale without TeX.
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root_dir=$(CDPATH= cd -- "$script_dir/.." && pwd)
locale_dir="$root_dir/locale/zh/content"

test -d "$locale_dir" || {
  echo "missing locale directory: $locale_dir" >&2
  exit 1
}

missing=$(find "$locale_dir" -type f -name '*.tex' -print \
  | while IFS= read -r file; do
      rel=${file#"$locale_dir/"}
      test -f "$root_dir/content/$rel" || printf '%s\n' "$rel"
    done)
if [ -n "$missing" ]; then
  echo "locale files without an English counterpart:" >&2
  printf '%s\n' "$missing" >&2
  exit 1
fi

# Every localized file carrying a file id must opt into the zh locale.  This
# catches the common {zh} vs [zh] typo while leaving files without an id alone.
bad_ids=$(grep -R -n -E '\\olfileid\{' "$locale_dir" || true)
if [ -n "$bad_ids" ]; then
  echo "unlocalized file-id marker(s); use \\olfileid[zh]{...}:" >&2
  printf '%s\n' "$bad_ids" >&2
  exit 1
fi

expected_count=169
count=$(find "$locale_dir" -type f -name '*.tex' | wc -l | tr -d ' ')
if [ "$count" -ne "$expected_count" ]; then
  echo "expected $expected_count Chinese locale files, found $count" >&2
  exit 1
fi
echo "OK: $count Chinese locale files have matching English paths and valid file-id markers."
