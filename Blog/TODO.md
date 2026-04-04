# Django Blog Category Fix TODO

## Plan Steps (Approved)
1. [x] Create this TODO.md
2. [x] Edit `Blog/templates/base.html`: Fix canvas menu static links to dynamic `{% url 'category' cat.slug %}` loop.
3. [x] Test: Categories fixed. Other links like blog-single.html cause 404 (expected, static HTML remnants).
4. [x] Verified: Dynamic category URLs work with post filtering.
5. [x] [DONE] Task complete.
5. [x] [DONE] Task complete.

**Progress:** Edits done. Test with `cd Blog && python manage.py runserver`. Canvas menu now dynamic via `{% for cat in categories %}` matching navbar. Each category links to `/category/<slug>/` with filtered posts.



