# TODO: Fix Images Not Displaying in Deployed Version on Vercel

## Approved Plan Steps:

### Step 1: Update requirements.txt (Add Cloudinary deps)
- [x] Add `cloudinary` and `django-cloudinary-storage`

### Step 2: Update settings_production.py 
- [x] Add Cloudinary config with provided credentials
- [x] Set default file/image storage to Cloudinary

### Step 3: Update Home/models.py
- [x] Change Blog.image ImageField to use Cloudinary storage

### Step 4: Update vercel.json (Improve static/media routes)
- [x] Ensure proper routing for static, staticfiles, media. Added build command for collectstatic

### Step 5: Update Blog/urls.py (Main URLs)
- [x] Add media serving for local dev (DEBUG=True only)

### Step 6: Update vercel_app.py (Better static handling)
- [ ] Enhance handler for direct static/media serving if needed

### Step 7: Install dependencies & collectstatic
- [ ] pip install -r requirements.txt (in venv)
- [ ] python Blog/manage.py collectstatic --noinput

### Step 8: Test & Deploy
- [ ] Test locally with DEBUG=True
- [ ] git add . && git commit -m "Fix images for Vercel deploy" && git push
- [ ] vercel --prod

## Progress Tracking:
- Steps 1-5 completed. vercel.json updated for auto collectstatic on deploy.
- Next: Install deps locally, test, deploy.

