# ShopSphere - Production Deployment Guide

This guide will help you deploy the ShopSphere e-commerce application to production platforms like Vercel, Heroku, or other cloud providers.

## Prerequisites

- Python 3.9+
- Git
- A Vercel account (for Vercel deployment)
- PostgreSQL database (for production)

## Quick Deployment to Vercel

### 1. Prepare Your Repository

1. Ensure all files are committed to your Git repository
2. Push your code to GitHub, GitLab, or Bitbucket

### 2. Environment Variables

Set the following environment variables in your Vercel dashboard:

```bash
SECRET_KEY=your-super-secret-key-here
DEBUG=False
DJANGO_SETTINGS_MODULE=ecommerce_store.settings_production
DATABASE_URL=postgresql://username:password@host:port/database_name
```

Optional variables:
```bash
CUSTOM_DOMAIN=yourdomain.com
DJANGO_LOG_LEVEL=INFO
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@yourdomain.com
DJANGO_SUPERUSER_PASSWORD=secure-password
```

### 3. Deploy to Vercel

1. Connect your repository to Vercel
2. Vercel will automatically detect the Django application
3. The build process will run automatically using `build_files.sh`
4. Your application will be deployed and accessible via the provided URL

### 4. Post-Deployment Setup

After deployment, run the production setup command:

```bash
# This will run migrations and collect static files
python manage.py setup_production --create-superuser
```

## Alternative Deployment Options

### Heroku Deployment

1. Install Heroku CLI
2. Create a `Procfile`:
   ```
   web: gunicorn ecommerce_store.wsgi:application
   release: python manage.py setup_production
   ```
3. Set environment variables in Heroku dashboard
4. Deploy using Git

### Railway Deployment

1. Connect your repository to Railway
2. Set environment variables
3. Railway will automatically deploy your Django application

## Database Setup

### PostgreSQL (Recommended for Production)

1. Create a PostgreSQL database
2. Set the `DATABASE_URL` environment variable
3. Run migrations: `python manage.py migrate`

### SQLite (Development Only)

The application will use SQLite if no `DATABASE_URL` is provided.

## Static Files

Static files are handled by WhiteNoise middleware and are automatically collected during deployment.

## Media Files

For production, consider using cloud storage services like:
- AWS S3
- Cloudinary
- Google Cloud Storage

## Security Considerations

The production settings include:
- ✅ Debug mode disabled
- ✅ Secure headers enabled
- ✅ CSRF protection
- ✅ XSS protection
- ✅ Clickjacking protection
- ✅ HSTS headers
- ✅ Session security

## Monitoring and Logging

Logs are configured to output to the console and can be viewed in your deployment platform's dashboard.

## Troubleshooting

### Common Issues

1. **Static files not loading**: Ensure `STATIC_ROOT` is set and `collectstatic` has been run
2. **Database connection errors**: Verify `DATABASE_URL` is correctly set
3. **Secret key errors**: Ensure `SECRET_KEY` environment variable is set

### Debug Mode

Never enable debug mode in production. If you need to debug issues:
1. Check the application logs
2. Use the Django admin interface
3. Set up proper logging

## Performance Optimization

For better performance:
1. Use a CDN for static files
2. Enable database connection pooling
3. Use Redis for caching
4. Optimize database queries

## Backup Strategy

1. Regular database backups
2. Media files backup
3. Environment variables backup

## Support

For issues related to deployment, check:
1. Platform-specific documentation
2. Django deployment documentation
3. Application logs
