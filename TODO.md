# Fix Image 404s on Main Page (Vercel Deployment)

## Steps from Approved Plan:

### 1. Update settings_production.py
- Ensure MEDIA_URL = '/static/media/'
- MEDIA_ROOT = BASE_DIR / 'staticfiles/media'
- Confirm WhiteNoise middleware and STATICFILES_STORAGE.

### 2. Update vercel.json buildCommand
- After collectstatic: Copy Blog/media/* to Blog/staticfiles/media/
  Command: `python manage.py collectstatic --noinput --clear &amp;&amp; python -c "import shutil, os; [shutil.copy2(src, &#39;Blog/staticfiles/media/&#39;) for src in os.listdir(&#39;Blog/media&#39;) if os.path.isfile(os.path.join(&#39;Blog/media&#39;, src))] + [shutil.copytree(os.path.join(&#39;Blog/media&#39;, d), os.path.join(&#39;Blog/staticfiles/media&#39;, d), dirs_exist_ok=True) for d in os.listdir(&#39;Blog/media&#39;) if os.path.isdir(os.path.join(&#39;Blog/media&#39;, d))]"`

### 3. Fix relative image paths in templates
- Search for src="images/..." or data-bg-image="images/..." without {% static %}
- Replace with {% static 'images/...' %} (load static already in base).

### 4. Test
- python Blog/manage.py collectstatic --noinput --clear
- Check Blog/staticfiles/media/images/ has airship-8854797_640.jpg etc.
- python Blog/manage.py runserver &amp;&amp; browse /media/images/airship-8854797_640.jpg

### 5. Deploy
- git add . &amp;&amp; git commit -m "fix: media 404s" &amp;&amp; git push
- Vercel auto-deploys.

**Progress: TODO.md created. Next: Edit files.**

Current: Step 1 - settings_production.py

