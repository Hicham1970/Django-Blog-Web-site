# TODO Steps to Fix Media/Images on Vercel

## Plan Breakdown:
1. ✅ **Update vercel.json**: Added headers/routes for /media/* and updated build to copy media/
2. ✅ **Update build command**: Copies media to staticfiles/media during collectstatic
3. ⬜ **Redeploy**: Run `vercel --prod` (production deploy) or `git push` if linked to repo
4. ⬜ **Test**: 
   - Visit deployed site
   - Check blog posts images load
   - Direct: https://your-site.vercel.app/media/[filename].jpg (replace with actual image)
5. ⬜ **Verify**: If works, mark complete. If not, share Vercel build/deploy logs.

**Next step:** Execute `vercel --prod` in terminal and test the deployed site.
