# 🚀 Deployment Checklist for Tymely Time and Attendance Tracker

## ✅ Pre-Deployment Setup

### 1. Database Setup (Render)

- [ ] Create PostgreSQL database on Render
- [ ] Note down the External Database URL
- [ ] Test connection from local machine

### 2. Environment Variables Setup

- [ ] Copy `.env.template` to `.env` (for local use)
- [ ] Generate new SECRET_KEY (use `python generate_secret_key.py`)
- [ ] Set DEBUG=False for production
- [ ] Set proper ALLOWED_HOSTS with your Vercel domain
- [ ] Set DATABASE_URL from Render
- [ ] Set VERCEL_URL with your app domain

### 3. Code Repository

- [ ] Push all code to GitHub
- [ ] Ensure `.env` is in `.gitignore` (already done)
- [ ] Verify all deployment files are committed:
  - [ ] `vercel.json`
  - [ ] `build_files.sh`
  - [ ] `runtime.txt`
  - [ ] `requirements.txt`

## 🎯 Deployment Steps

### 1. Vercel Setup

- [ ] Create new project on Vercel
- [ ] Connect to your GitHub repository
- [ ] Set Framework Preset to "Other"
- [ ] Build Command: `./build_files.sh`
- [ ] Install Command: `pip install -r requirements.txt`

### 2. Environment Variables (Vercel)

Add these in Vercel Project Settings → Environment Variables:

- [ ] `SECRET_KEY` = (your generated secret key)
- [ ] `DEBUG` = `False`
- [ ] `ALLOWED_HOSTS` = `your-app.vercel.app,localhost,127.0.0.1`
- [ ] `DATABASE_URL` = (your Render PostgreSQL URL)
- [ ] `VERCEL_URL` = `your-app.vercel.app`

### 3. Deploy

- [ ] Deploy the project
- [ ] Wait for build to complete
- [ ] Check for any build errors

### 4. Database Migration

Choose one method:

**Method A - Local Migration (Recommended):**

- [ ] Set local `.env` DATABASE_URL to Render
- [ ] Run: `python manage.py migrate`
- [ ] Run: `python manage.py createsuperuser`

**Method B - Vercel CLI:**

- [ ] Install Vercel CLI: `npm i -g vercel`
- [ ] Run: `vercel exec -- python manage.py migrate`
- [ ] Run: `vercel exec -- python manage.py createsuperuser`

## 🔍 Testing

### URLs to Test:

- [ ] Home page: `https://your-app.vercel.app/`
- [ ] Health check: `https://your-app.vercel.app/health/`
- [ ] Admin panel: `https://your-app.vercel.app/admin/`
- [ ] Static files loading correctly
- [ ] Login/logout functionality
- [ ] Database operations working

### Performance Checks:

- [ ] Page load times acceptable
- [ ] Static files loading from CDN
- [ ] Database queries working
- [ ] Forms submitting properly

## 🔒 Security Verification

- [ ] SECRET_KEY is different from example
- [ ] DEBUG=False in production
- [ ] HTTPS working (Vercel provides this automatically)
- [ ] Admin panel accessible only to superusers
- [ ] Database credentials not exposed in logs

## 📊 Post-Deployment

### Monitoring Setup:

- [ ] Set up error tracking (optional)
- [ ] Monitor application logs
- [ ] Set up uptime monitoring
- [ ] Regular database backups

### Domain Setup (Optional):

- [ ] Purchase custom domain
- [ ] Configure domain in Vercel
- [ ] Update ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS

## 🆘 Troubleshooting

If deployment fails, check:

1. **Build Logs** - Look for Python/pip errors
2. **Environment Variables** - Ensure all are set correctly
3. **Database Connection** - Test DATABASE_URL format
4. **Static Files** - Check if collectstatic works locally
5. **Secret Key** - Must be set and valid

### Common Error Solutions:

- **500 Error**: Check SECRET_KEY and DEBUG settings
- **Static files 404**: Verify STATIC_ROOT and collectstatic
- **Database errors**: Check DATABASE_URL format and credentials
- **Import errors**: Verify all packages in requirements.txt

## 📞 Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/stable/howto/deployment/

---

✅ **Your application is now production-ready!**

Remember to:

- Keep your environment variables secure
- Regularly update dependencies
- Monitor application performance
- Backup your database regularly
