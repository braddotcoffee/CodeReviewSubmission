# CodeReviewSubmission
> Discord Bot for accepting code submissions for review

## Prerequisites
- Python 3.x
- MySQL Server
- Discord account and a server with administrative privileges
- Discord Bot

## Installation

### Clone the Repository
```bash
git clone https://github.com/braddotcoffee/CodeReviewSubmission
cd CodeReviewSubmission
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Setup

### Setting up the Discord Bot
1. Visit the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application and bot.
3. Copy the bot token.
4. Add the bot to your server by creating an OAuth2 URL with appropriate permissions.

### Create a Moderator Role and Community Channel on Discord
1. Create a moderator role in your Discord server.
2. Add a community channel and create a forum channel within it.
3. Create a tag in the forum channel for code review submissions.

### Database Setup
1. Install and run MySQL Server on your device.
2. Create a new database named `codereview`.
3. Create a user `codereviewuser` with a password.

### Configuration
Replace the placeholders in `example.config.yaml` and `example.secrets.yaml` with your actual data:
- `example.secrets.yaml`:
   ```yaml
   Discord:
     Token: YOUR_DISCORD_BOT_TOKEN
   Database:
     Password: YOUR_DATABASE_PASSWORD
   ```

- `example.config.yaml`:
   ```yaml
   Database:
     Username: codereviewuser
     Host: localhost # prod-db for production
     Name: codereview
   Discord:
     ModeratorRole: YOUR_MODERATOR_ROLE_ID
     CodeReview:
       Channel: YOUR_CODE_REVIEW_CHANNEL_ID
       NeedsReviewTag: YOUR_REVIEW_TAG_ID
   ```

Rename these files to `config.yaml` and `secrets.yaml`.

### Sync Commands
Uncomment below code in `bot.py` under `on_ready` function, run the bot once, then comment it back. This will sync the commands to your server.

### Dump Tags
Create a post inside the forum channel and run `/sync dumb_tags` to retrieve the `NewdReviewTag` and replace it respectively.

### Running the Bot Locally
```bash
python3 bot.py
```

### Using Docker (Production)
Brad, I didn't try this, so I'll leave it up to you to fill this up.
