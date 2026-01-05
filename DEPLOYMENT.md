# Deployment Guide

## 🚀 Deploy to Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy this app for free!

### Step 1: Prerequisites
- GitHub account (already done ✅)
- Repository created (already done ✅ - https://github.com/snehitvaddi/h1b-wage-finder)

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**: https://streamlit.io/cloud

2. **Sign in with GitHub**
   - Click "Sign in with GitHub"
   - Authorize Streamlit Cloud

3. **Deploy App**
   - Click "New app"
   - Select repository: `snehitvaddi/h1b-wage-finder`
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy!"

4. **Wait for Deployment** (takes 2-3 minutes)
   - Streamlit Cloud will install dependencies from `requirements.txt`
   - Build the app
   - Deploy it live

5. **Get Your URL**
   - You'll get a URL like: `https://your-app-name.streamlit.app`
   - Share this URL publicly!

### Step 3: Configure App (Optional)

In Streamlit Cloud dashboard:
- **App settings** → Advanced settings
  - Python version: 3.11 (recommended)
  - Memory: Default (should be fine)

### Step 4: Custom Domain (Optional)

If you want a custom domain like `h1bwages.com`:
1. Buy domain from Namecheap/GoDaddy
2. In Streamlit Cloud: Settings → General → Custom subdomain
3. Add CNAME record in your DNS settings

---

## Alternative: Deploy to Vercel (Not Recommended for Streamlit)

Vercel is optimized for Next.js/React apps, not Streamlit. Stick with Streamlit Cloud for best results.

---

## Post-Deployment Checklist

- [ ] Update README.md with live app URL
- [ ] Test all features (Salary Recommendations, Wage Level Summary, Quick Search)
- [ ] Test location search (ZIP, County, City name)
- [ ] Share link on:
  - LinkedIn
  - Reddit (r/h1b, r/immigration)
  - Twitter/X
  - Your network

---

## Monitoring

Streamlit Cloud provides:
- **Analytics**: View count, user engagement
- **Logs**: Debug errors
- **Metrics**: Performance monitoring

Access via: Streamlit Cloud Dashboard → Your App → Analytics/Logs

---

## Updating the App

To push updates:

```bash
git add .
git commit -m "Your update message"
git push
```

Streamlit Cloud will automatically redeploy! ⚡

---

## Troubleshooting

### App won't start
- Check Streamlit Cloud logs
- Verify `requirements.txt` has all dependencies
- Ensure data files are in `OFLC_Wages_2025-26_Updated/` folder

### Slow performance
- Streamlit Cloud free tier has limits
- Consider upgrading to paid tier for better performance

### Data not loading
- Make sure CSV files are pushed to GitHub
- Check file paths in code match repository structure

---

## Cost

**Streamlit Cloud**: FREE for public repos! 🎉
- Unlimited apps
- Unlimited views
- Community support

**Paid tier** ($20/month) if you need:
- Private repos
- More resources
- Priority support

---

## Your App is Live! 🎊

Repository: https://github.com/snehitvaddi/h1b-wage-finder

Next: Deploy on Streamlit Cloud following steps above!
