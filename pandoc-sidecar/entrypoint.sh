#!/bin/bash

# wait until flask pod starts
sleep 5

while(true); do
  echo "----"
  echo Waking up -- $(date -u)
  echo "----"
  tmp_dir=$(mktemp -d -t ci-XXXXXXXXXX)
  pushd $tmp_dir
      curl http://$MYRESUME_HOST/resume.md/ > resume.md
      styleformats="html pdf docx"
      for format in $styleformats; do
        pandoc -s resume.md -c /root/markdown8.css -o /pandoc/resume.$format
      done

      formats="tex epub odt rst"
      for format in $formats; do
        pandoc -s resume.md -o /pandoc/resume.$format
      done

      txtformats="man jira ipynb commonmark biblatex bibtex native"
      for format in $txtformats; do
        pandoc -s resume.md -o /pandoc/resume.$format.txt
      done
      rm resume.md
  popd
  rm -rf $tmp_dir
  echo "Waiting 10 seconds to regenerate resume(s)"
  sleep 10
done