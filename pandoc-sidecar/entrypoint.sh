#!/bin/bash

# wait for flask pod to start
sleep 5

while(true); do
  echo "$(date -u) -- Waking up"
  tmp_dir=$(mktemp -d -t ci-XXXXXXXXXX)
  pushd $tmp_dir
      curl http://$MYRESUME_HOST/resume.md/ > resume.md
      styleformats="html pdf docx"
      for format in $styleformats; do
        pandoc -s resume.md -c /root/markdown8.css -o /pandoc/resume.$format --metadata title="resume"
      done

      txtformats="tex epub odt rst man jira ipynb commonmark biblatex bibtex native"
      for format in $txtformats; do
        pandoc -s resume.md -o /pandoc/resume.$format.txt --metadata title="resume"
      done
      rm resume.md
  popd
  rm -rf $tmp_dir
  echo "$(date -u) -- Sleeping 10 seconds to regenerate resume(s)"
  sleep 10
done