### Set Up

--

## Create a .env file
Replace `EMAIL_USER`  with the actuall email acted as a sender.
Replace `EMAIL_PASSWORD` with your app password.
> Google no longer allows login with your real password via SMTP.

```env
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
EMAIL_USER=your-email@example.com
EMAIL_PASSWORD=super-secret-password
```

## Instance Directory & .gitignore
Make sure the instance/ folder contains a .gitkeep file.
Do not commit files from instance/ or any secrets.
Add this to your .gitignore:
```gitignore
.env
instance/
```
