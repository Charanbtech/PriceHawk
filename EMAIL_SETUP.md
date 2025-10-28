# 📧 Email Setup Guide for PriceHawk

To enable email notifications and test emails, you need to configure Gmail credentials.

## Quick Setup Steps:

### 1. Enable Gmail 2-Factor Authentication
- Go to your Google Account settings
- Enable 2-Factor Authentication (2FA)

### 2. Generate Gmail App Password
- Go to Google Account > Security > App passwords
- Generate a new app password for "Mail"
- Copy the 16-character password (e.g., `abcd efgh ijkl mnop`)

### 3. Configure Environment Variables
Create a `.env` file in the `backend` folder:

```env
# Email Configuration
SENDER_EMAIL=your-email@gmail.com
SENDER_EMAIL_PASSWORD=your-16-character-app-password

# Other required variables
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/pricehawk
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret
```

### 4. Restart the Application
```bash
docker-compose down
docker-compose up -d --build
```

## Test Email Functionality

1. Go to **Notifications** page in PriceHawk
2. Click **📧 Send Test Email**
3. Enter your email address
4. Check your inbox for the test email

## Troubleshooting

- **"Username and Password not accepted"**: Use App Password, not regular Gmail password
- **"Email not configured"**: Check your `.env` file has correct SENDER_EMAIL and SENDER_EMAIL_PASSWORD
- **No email received**: Check spam folder, verify email address is correct

## Security Notes

- Never commit your `.env` file to version control
- Use App Passwords, not your main Gmail password
- Keep your credentials secure