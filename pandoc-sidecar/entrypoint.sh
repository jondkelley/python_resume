#!/bin/bash
# file: entrypoint.sh
# description: periodically regenerates the static resume for the shared volume with the resume container

# wait for flask app startup
sleep 5

count=1
sleepytime=30
stylesheet_name=markdown8.css

while(true); do
  echo "$(date -u) -- Wakeup!"

  # update JSON resume from github every 20 iterations
  # --------------------------------------------------
  if [[ $((++count%20)) -eq 0 ]];
  then
      echo "$(date -u) -- Updating latest resume.json from github"
      curl -s http://$MYRESUME_HOST/resume/update?secret=$UPDATE_SECRET | grep status
  fi

  # generate resume
  # ---------------
  echo "$(date -u) -- Generate resume"
  tmp_dir=$(mktemp -d -t ci-XXXXXXXXXX)
  pushd $tmp_dir
      # pull the latest resume from flask
      curl -s http://$MYRESUME_HOST/resume.md/ > resume.md
      # pull the markdown stylesheet if it doesn't exist
      if [ ! -f /tmp/$stylesheet_name ]; then
          curl -s http://$MYRESUME_HOST/static/css/markdown/$stylesheet_name > /tmp/$stylesheet_name
      fi
      echo -e "\n\n<br>Generation:" $(( count++ )) >> resume.md

      echo -e "\n\n<br>ContainerId: $(hostname) Load: $(cat /proc/loadavg | awk '{ print $1 , $2 , $3 }')" >> resume.md

      formats="html pdf docx epub odt rst man jira ipynb commonmark biblatex bibtex native"
      for format in $formats; do
        echo "EXEC: pandoc -s resume.md -c /tmp/markdown8.css -o /pandoc/resume.$format"
        pandoc --from=markdown --to=$format -s resume.md -c /tmp/markdown8.css -o /pandoc/resume.$format --metadata title=" "
      done
      # latex output
      pandoc --from=markdown --to=latex -s resume.md -c /tmp/markdown8.css -o /pandoc/resume.tex --metadata title=" "
      rm resume.md
  popd
  rm -rf $tmp_dir
  echo "$(date -u) -- Sleep $sleepytime seconds..."
  sleep $sleepytime
done