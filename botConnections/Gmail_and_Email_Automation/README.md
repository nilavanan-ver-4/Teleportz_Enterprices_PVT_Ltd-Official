# Gmail and Email Automation Resources

This directory contains resources for the Marketing Team to configure and manage automated email outreach.

## 📁 Contents
- `/templates`: Custom HTML email templates for outreach.
- `automation_logic.py`: (Optional) Python scripts for SMTP/Gmail API handling.

## 🔐 Configuration Guidelines
1. **Gmail API**: Recommended for high reliability. Use Google Cloud Console to create a Service Account.
2. **App Passwords**: If using standard SMTP, ensure 2FA is enabled and use an App Password.
3. **n8n Nodes**: Use the `Gmail` or `Send Email` nodes in n8n to connect these resources to your social workflows.

## 🚀 Future Integrations
- AI-driven subject line testing.
- Automatic lead scoring based on email opens/clicks.
