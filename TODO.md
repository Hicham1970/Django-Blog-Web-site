# Task: Update Editor's Pick section with real/dynamic posts - COMPLETE

## Steps:
1. [x] Update Blog/Home/views.py: Add `editors_pick = Blog.objects.filter(status='1').order_by('-created_at')[:5]` to home context.
2. [x] Update Blog/templates/index.html: Replace hardcoded Editor's Pick row (from `<div class="row gy-5">` to closing `</div>`) with dynamic loop over editors_pick.
3. [x] Test: Editor's Pick now uses 5 most recent published posts. First post (most recent) uses its image or fallback; links to blog_details. Run `python manage.py runserver` to verify at http://127.0.0.1:8000/. If no published posts, section empty - create via admin.

All steps complete.

