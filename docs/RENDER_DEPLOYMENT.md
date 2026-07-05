# 🚀 Deploy ShopSphere to Render

This guide will walk you through deploying your Django e-commerce application to Render.

## Prerequisites

- GitHub account with your code pushed
- Render account (free tier available)
- Basic understanding of environment variables

## Step-by-Step Deployment

### 1. Prepare Your Repository

Ensure your code is pushed to GitHub with all the production files:
- ✅ `render.yaml`
- ✅ `build.sh`
- ✅ `requirements.txt`
- ✅ Production settings

### 2. Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

### 3. Deploy Database First

1. In Render dashboard, click **"New +"**
2. Select **"PostgreSQL"**
3. Configure:
   - **Name**: `shopsphere-db`
   - **Database**: `shopsphere`
   - **User**: `shopsphere`
   - **Region**: Choose closest to your users
   - **Plan**: Free (for testing) or Starter ($7/month)
4. Click **"Create Database"**
5. **Save the Internal Database URL** (you'll need this)

### 4. Deploy Web Service

1. In Render dashboard, click **"New +"**
2. Select **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `shopsphere-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn ecommerce_store.wsgi:application`
   - **Plan**: Free (for testing) or Starter ($7/month)

### 5. Set Environment Variables

In your web service settings, add these environment variables:

#### Required Variables:
```bash
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DEBUG=False
DJANGO_SETTINGS_MODULE=ecommerce_store.settings_production
DATABASE_URL=postgresql://user:password@host:port/database
```

#### Optional Variables:
```bash
CUSTOM_DOMAIN=yourdomain.com
DJANGO_LOG_LEVEL=INFO
CREATE_SUPERUSER=true
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=secure-password-here
```

**Important**: 
- Get the `DATABASE_URL` from your PostgreSQL service in Render
- Generate a strong `SECRET_KEY` (50+ random characters)

### 6. Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start your application

### 7. Access Your Application

1. Once deployed, you'll get a URL like: `https://shopsphere-backend.onrender.com`
2. Visit the URL to see your live application
3. Access admin at: `https://your-app.onrender.com/admin/`

## Post-Deployment

### Create Superuser (if not done automatically)

If you didn't set the superuser environment variables:

1. Go to your web service in Render
2. Open the **"Shell"** tab
3. Run: `python manage.py createsuperuser`

### Add Sample Data

1. Access Django admin
2. Add categories and products
3. Upload product images

### Custom Domain (Optional)

1. In your web service settings
2. Go to **"Settings"** → **"Custom Domains"**
3. Add your domain
4. Update DNS records as instructed
5. Set `CUSTOM_DOMAIN` environment variable

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check build logs for missing dependencies
2. **Database Connection**: Verify `DATABASE_URL` is correct
3. **Static Files**: Ensure `collectstatic` runs in build script
4. **Secret Key**: Make sure it's set and long enough

### Checking Logs:

1. Go to your web service in Render
2. Click **"Logs"** tab
3. Monitor for errors

### Environment Variables:

Make sure all required variables are set in Render dashboard under **"Environment"**.

## Scaling and Performance

### Free Tier Limitations:
- Service sleeps after 15 minutes of inactivity
- 750 hours/month limit
- Slower cold starts

### Paid Tier Benefits:
- Always-on service
- Faster performance
- More resources
- Better support

## Security Notes

- Never commit `.env` files
- Use strong passwords
- Enable HTTPS (automatic on Render)
- Regular security updates

## Cost Estimation

### Free Tier:
- Web Service: Free (with limitations)
- PostgreSQL: Free (1GB storage)

### Paid Tier:
- Web Service: $7/month (Starter)
- PostgreSQL: $7/month (Starter)
- **Total**: ~$14/month

## Next Steps

1. Set up monitoring
2. Configure backups
3. Add custom domain
4. Optimize performance
5. Set up CI/CD pipeline

Your ShopSphere e-commerce application is now live on Render! 🎉
