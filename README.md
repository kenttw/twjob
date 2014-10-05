twjob
=====
Job Search Engine at TW

- how to execute for 66kjob
'''
python ${workspace_loc:twjob/src/twjobcrawler.py} --spider 66KJobSpider  --domains 66kjobs.tw --url http://66kjobs.tw/
'''
- how to execute for jobinside
'''
python ${workspace_loc:twjob/src/twjobcrawler.py} --spider InsideSpider --domains jobs.inside.com.tw --url http://jobs.inside.com.tw/
'''
