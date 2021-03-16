#!/bin/sh

for c in *.css
do
    echo "[$c](${c/.css/.html}) | "
done > list.md

for p in *.css
do
    echo "<link rel='stylesheet' href='$p'/>" > ${p/.css/.html}
    echo "<h1>Markdown css themes</h1>" >> ${p/.css/.html}
    cat list.md sample.md | markdown >> ${p/.css/.html}
done

cp ${p/.css/.html} index.html




