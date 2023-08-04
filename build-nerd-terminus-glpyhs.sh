#!/bin/bash

set -e

echo "Build mkfont_bdf"
make mkfont_bdf

echo "Build regular glpyhs"
./glyph_builder.sh terminus u14n >/dev/null
mv glyph.h glyph.base.h

echo "Build nerd fonts"
otf2bdf -n -p 14 -rh 84 -rv 74 Terminess/TerminessNerdFontMono-Regular.ttf -w Normal -o regular.nerd.bdf >/dev/null || true
otf2bdf -n -p 14 -rh 84 -rv 74 Terminess/TerminessNerdFontMono-Bold.ttf -w Bold -o bold.nerd.bdf >/dev/null || true
otf2bdf -n -p 14 -rh 84 -rv 74 Terminess/TerminessNerdFontMono-Italic.ttf -w Normal -s I -o italic.nerd.bdf >/dev/null || true
./mkfont_bdf table/alias regular.nerd.bdf bold.nerd.bdf italic.nerd.bdf >glyph.nerd.h

echo "Merge glyphs"
./merge-glyphs.py glyph.base.h glyph.nerd.h >glyph.h
# rm glyph.base.h glyph.nerd.h

echo "Build yaft"
make
