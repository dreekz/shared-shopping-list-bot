# Serverless Telegram Shopping List Bot

A serverless Telegram bot built on AWS that helps manage shared shopping lists. This project serves as a practical exploration of serverless architecture and AWS services.

## 🎯 Project Overview

This bot allows users to manage shopping lists through Telegram with features like:
- Creating and managing shopping lists
- Adding/Removing items
- Sharing lists with other Telegram users
- Managing user permissions
- Real-time updates and synchronization

## 🏗️ Architecture

The project uses a serverless architecture leveraging several AWS services:
- **AWS Lambda** - Handles bot commands and business logic
- **Amazon DynamoDB** - Stores shopping lists and user data
- **Amazon API Gateway** - Manages webhook endpoints for Telegram
- **Telegram Bot API** - User interface and interaction

![Telegram Shopping List Bot Architecture](./documents/telegram-shared-shopping-list.png)

## 🛠️ Prerequisites

- Python 3.9+
- AWS Account with appropriate permissions
- Terraform installed (v1.0.0+)
- Telegram Bot Token (obtained from [@BotFather](https://t.me/botfather))
- AWS CLI configured with appropriate credentials

## 🚀 Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/shared-shopping-list-bot.git
   cd shared-shopping-list-bot
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```
   BOT_TOKEN=your_telegram_bot_token
   API_URL=your_api_gateway_url
   ADMIN_ID=your_telegram_user_id
   ```

5. Deploy infrastructure:
   ```bash
   cd terraform
   terraform init
   terraform apply
   ```

## 🤖 Bot Commands

- `/list` - Show current shopping list
- `/add [item]` - Add item to the list
- `/remove [item]` - Remove item from the list
- `/add_user [user_id]` - (Admin only) Add new authorized user
- `/myid` - Get your Telegram user ID

## 🔧 Local Development

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run tests:
   ```bash
   pytest
   ```

3. Format code:
   ```bash
   black .
   ```

4. Run type checking:
   ```bash
   mypy .
   ```

## 📦 Deployment

The project uses GitHub Actions for CI/CD. Every push to main will:
1. Run tests
2. Run linting and type checking
3. Deploy to AWS using Terraform

Manual deployment:
```bash
cd terraform
terraform apply
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please make sure to update tests and documentation as appropriate.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔍 Troubleshooting

Common issues and solutions:

1. Bot not responding:
   - Check if the Lambda function is properly deployed
   - Verify API Gateway endpoint is correct in `.env`
   - Check CloudWatch logs for errors

2. Permission issues:
   - Ensure your Telegram ID is added to the users table
   - Verify IAM roles and policies are correctly set up

3. DynamoDB errors:
   - Check if tables are created correctly
   - Verify Lambda has