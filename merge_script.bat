@echo off
cd /d c:\Users\User\arifOS
echo "--- START ---" > merge_log.txt

echo "--- LISTING FILES ---" >> merge_log.txt
dir >> merge_log.txt 2>&1

echo "--- REMOVING ORPHAN ---" >> merge_log.txt
del "=5.0.0" >> merge_log.txt 2>&1
git rm --ignore-unmatch "=5.0.0" >> merge_log.txt 2>&1
git commit -m "chore: remove orphan file =5.0.0" >> merge_log.txt 2>&1

echo "--- SWITCHING TO MAIN ---" >> merge_log.txt
git checkout main >> merge_log.txt 2>&1

echo "--- MERGING DEV-V56 ---" >> merge_log.txt
git merge dev-v56 >> merge_log.txt 2>&1

echo "--- PUSHING ---" >> merge_log.txt
git push origin main >> merge_log.txt 2>&1

echo "--- DONE ---" >> merge_log.txt
