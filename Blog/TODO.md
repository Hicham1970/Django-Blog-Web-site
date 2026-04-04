# PostgreSQL Migration TODO

## Previous: Images Fixed ✅

## Postgres Migration Plan:
1. ✅ **Requirements**: Added psycopg[binary]==3.2.1
2. ✅ **Settings**: Updated settings_production.py with Neon: postgresql://neondb_owner:npg_i6Xor2cYEhLJ@ep-cool-king-anypd2cp.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require
3. ✅ **Local setup**: `cd Blog && python manage.py makemigrations && python manage.py migrate`
4. ✅ **Vercel env**: Add DATABASE_URL = `postgresql://neondb_owner:npg_i6Xor2cYEhLJ@ep-cool-king-anypd2cp.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require` (all envs)
5. ✅ **Update settings**: Parse DATABASE_URL if set
6. ✅ **Deploy & test**: `vercel --prod`, test new comments

**Next:** Run local migrations, add DATABASE_URL to Vercel, redeploy.

**Next:** Run migrations locally, then add `DATABASE_URL` to Vercel env vars.
