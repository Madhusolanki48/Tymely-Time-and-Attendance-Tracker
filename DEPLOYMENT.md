# Deployment Guide

## Prerequisites

1. **Render Account** - For PostgreSQL database
2. **Vercel Account** - For application deployment
3. **GitHub Repository** - Your code should be pushed to GitHub

## Step 1: Set up Database on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "PostgreSQL"
3. Fill in the details:
   - Name: `tymely-database` (or any name you prefer)
   - Database: `tymely_db`
   - User: `tymely_user`
   - Region: Choose closest to your users
   - PostgreSQL Version: 15 (recommended)
   - Plan: Free (for testing) or paid for production
4. Click "Create Database"
5. Once created, note down the connection details:
   - **External Database URL** (this is what you'll use for DATABASE_URL)

## Step 2: Set up Environment Variables

Create a `.env` file in your project root with these variables:

```env
# Django Settings
SECRET_KEY=your-very-long-secret-key-here-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=your-app-name.vercel.app,localhost,127.0.0.1

# Database Settings (from Render)
DATABASE_URL=postgresql://tymely_user:password@hostname:port/tymely_db

# Vercel Settings
VERCEL_URL=your-app-name.vercel.app
```

### Generate a Secret Key

Run this command to generate a new secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Step 3: Deploy to Vercel

1. Push your code to GitHub
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "New Project"
4. Import your GitHub repository
5. Configure the project:

   - **Framework Preset**: Other
   - **Root Directory**: ./
   - **Build Command**: `./build_files.sh`
   - **Output Directory**: Leave empty
   - **Install Command**: `pip install -r requirements.txt`

6. Add Environment Variables in Vercel:

   - Go to Project Settings → Environment Variables
   - Add all the variables from your `.env` file:
     - `SECRET_KEY`
     - `DEBUG` = `False`
     - `ALLOWED_HOSTS` = `your-app-name.vercel.app,localhost,127.0.0.1`
     - `DATABASE_URL` = (your Render PostgreSQL URL)
     - `VERCEL_URL` = `your-app-name.vercel.app`

7. Deploy the project

## Step 4: Run Database Migrations

After deployment, you need to run migrations. You have two options:

### Option A: Local Migration (Recommended)

1. Set the DATABASE_URL in your local `.env` file to point to Render
2. Run: `python manage.py migrate`
3. Create a superuser: `python manage.py createsuperuser`

### Option B: Using Vercel CLI

1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Run: `vercel exec -- python manage.py migrate`
4. Create superuser: `vercel exec -- python manage.py createsuperuser`

## Step 5: Test Your Deployment

1. Visit your Vercel URL: `https://your-app-name.vercel.app`
2. Test the health check: `https://your-app-name.vercel.app/health/`
3. Access admin panel: `https://your-app-name.vercel.app/admin/`

## Important Notes

1. **Static Files**: Handled by WhiteNoise, no additional configuration needed
2. **Media Files**: For production, consider using AWS S3 or Cloudinary
3. **Database**: The free Render PostgreSQL has limitations, upgrade for production
4. **Domain**: You can add a custom domain in Vercel settings
5. **Monitoring**: Set up error tracking (Sentry) for production

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check your requirements.txt and Python version
2. **Database Connection**: Verify DATABASE_URL format and credentials
3. **Static Files Not Loading**: Ensure STATIC_ROOT and collectstatic work
4. **500 Error**: Check environment variables, especially SECRET_KEY

### Debug Commands:

```bash
# Test locally with production settings
python manage.py check --deploy

# Test database connection
python manage.py dbshell

# Collect static files
python manage.py collectstatic

# Run the deploy command
python manage.py deploy
```

## Security Checklist

- ✅ SECRET_KEY is set from environment variable
- ✅ DEBUG=False in production
- ✅ ALLOWED_HOSTS is properly configured
- ✅ Database credentials are in environment variables
- ✅ CSRF_TRUSTED_ORIGINS includes your domain
- ✅ Security middleware is enabled
- ✅ HTTPS redirect is enabled for production

Your Django application is now deployment-ready! 🚀
