twjob
=====
Job Search Engine at TW

- how to execute for 66kjob
```sh
python ${workspace_loc:twjob/src/twjobcrawler.py} --spider 66KJobSpider  --domains 66kjobs.tw --url http://66kjobs.tw/
```
- how to execute for jobinside
```sh
python ${workspace_loc:twjob/src/twjobcrawler.py} --spider InsideSpider --domains jobs.inside.com.tw --url http://jobs.inside.com.tw/
```