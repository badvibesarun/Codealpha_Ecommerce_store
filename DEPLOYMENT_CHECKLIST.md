# 🚀 Render Deployment Checklist

Follow this checklist to deploy your ShopSphere e-commerce app to Render.

## ✅ Pre-Deployment Checklist

- [ ] Code is committed and pushed to GitHub
- [ ] All production files are present:
  - [ ] `render.yaml`
  - [ ] `build.sh`
  - [ ] `requirements.txt`
  - [ ] `ecommerce_store/settings_production.py`
  - [ ] `.env.example`

## 🗄️ Database Setup

1. **Create PostgreSQL Database on Render**
   - [ ] Go to [render.com](https://render.com)
   - [ ] Click "New +" → "PostgreSQL"
   - [ ] Name: `shopsphere-db`
   - [ ] Database: `shopsphere`
   - [ ] User: `shopsphere`
   - [ ] Plan: Free (for testing)
   - [ ] Click "Create Database"
   - [ ] **Copy the Internal Database URL**

## 🌐 Web Service Setup

2. **Create Web Service on Render**
   - [ ] Click "New +" → "Web Service"
   - [ ] Connect your GitHub repository
   - [ ] Name: `shopsphere-app`
   - [ ] Environment: `Python 3`
   - [ ] Build Command: `./build.sh`
   - [ ] Start Command: `gunicorn ecommerce_store.wsgi:application`
   - [ ] Plan: Free (for testing)

## 🔧 Environment Variables

3. **Set Environment Variables** (in Render web service settings):

### Required Variables:
```
SECRET_KEY=your-50-character-random-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=ecommerce_store.settings_production
DATABASE_URL=postgresql://user:password@host:port/database
```

### Optional Variables (for auto superuser creation):
```
CREATE_SUPERUSER=true
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=YourSecurePassword123!
```

## 🚀 Deploy

4. **Deploy Your Application**
   - [ ] Click "Create Web Service"
   - [ ] Wait for build to complete (5-10 minutes)
   - [ ] Check build logs for any errors
   - [ ] Visit your app URL when build succeeds

## ✅ Post-Deployment

5. **Verify Deployment**
   - [ ] App loads successfully
   - [ ] Admin panel accessible at `/admin/`
   - [ ] Can log in with superuser credentials
   - [ ] Static files loading correctly
   - [ ] Database connection working

6. **Add Sample Data**
   - [ ] Log into Django admin
   - [ ] Create product categories
   - [ ] Add sample products
   - [ ] Upload product images

## 🔍 Troubleshooting

### If Build Fails:
- Check build logs in Render dashboard
- Verify all files are in repository
- Check `requirements.txt` for correct dependencies

### If App Won't Start:
- Check environment variables are set correctly
- Verify `DATABASE_URL` is correct
- Check application logs

### If Static Files Don't Load:
- Ensure `collectstatic` ran during build
- Check `STATIC_ROOT` setting
- Verify WhiteNoise is installed

## 📱 Your Live App

Once deployed, your app will be available at:
`https://your-app-name.onrender.com`

Admin panel: `https://your-app-name.onrender.com/admin/`

## 💰 Cost

**Free Tier:**
- Web Service: Free (sleeps after 15 min inactivity)
- PostgreSQL: Free (1GB storage)

**Paid Tier:**
- Web Service: $7/month (always-on)
- PostgreSQL: $7/month (better performance)

## 🎉 Success!

Your ShopSphere e-commerce application is now live on the internet!

Share your live URL and start selling! 🛒
