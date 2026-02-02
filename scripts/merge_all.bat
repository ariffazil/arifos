@echo off
set GIT="C:\Program Files\Git\cmd\git.exe"
echo Starting Merge Process > merge_log.txt

echo Checkout main... >> merge_log.txt
%GIT% checkout main >> merge_log.txt 2>&1

echo Merging dev-v56... >> merge_log.txt
%GIT% merge --no-edit dev-v56 >> merge_log.txt 2>&1

echo Merging loving-almeida... >> merge_log.txt
%GIT% merge --no-edit loving-almeida >> merge_log.txt 2>&1

echo Merging sleepy-booth... >> merge_log.txt
%GIT% merge --no-edit sleepy-booth >> merge_log.txt 2>&1

echo Merging reconstruction/v52... >> merge_log.txt
%GIT% merge --no-edit reconstruction/v52 >> merge_log.txt 2>&1

echo Merging refactor/great-purge-canonicalization... >> merge_log.txt
%GIT% merge --no-edit refactor/great-purge-canonicalization >> merge_log.txt 2>&1

echo Done. >> merge_log.txt
