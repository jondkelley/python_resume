#!/bin/bash
# file: entrypoint.sh
# description: periodically regenerate the static resume for the shared volume with the resume container

# wait for flask pod to start
sleep 5

count=1
sleeptime=30
stylesheet_name=markdown8.css

while(true); do
  echo "$(date -u) -- Waking up to generate resumes"
  tmp_dir=$(mktemp -d -t ci-XXXXXXXXXX)
  pushd $tmp_dir
      # pull latest resume down
      curl -s http://$MYRESUME_HOST/resume.md/ > resume.md
      # pull the markdown stylesheet if it doesn't exist
      if [ ! -f /tmp/$stylesheet_name ]; then
          curl -s http://$MYRESUME_HOST/static/css/markdown/$stylesheet_name > /tmp/$stylesheet_name
      fi
      echo -e "\n\n<br>Generation:" $(( count++ )) >> resume.md

      echo -e "\n\n<br>ContainerId: $(hostname) Load: $(cat /proc/loadavg | awk '{ print $1 , $2 , $3 }')" >> resume.md

      formats="html pdf docx tex epub odt rst man jira ipynb commonmark biblatex bibtex native"
      for format in $formats; do
        echo "EXEC: pandoc -s resume.md -c /tmp/markdown8.css -o /pandoc/resume.$format"
        pandoc --from=markdown --to=$format -s resume.md -c /tmp/markdown8.css -o /pandoc/resume.$format --metadata title=" "
      done
      rm resume.md
  popd
  rm -rf $tmp_dir
  echo "$(date -u) -- Sleep $sleeptime seconds..."
  sleep $sleeptime
done
