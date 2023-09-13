from models.newsletter import Newsletter
from models.newsletter import NewsLetterBot
from app  import db

class NewsletterService:
    def get_newsletters(self):
        newsletters = Newsletter.query.all()
        return [self._convert_to_dict(newsletter) for newsletter in newsletters]

    def get_newsletter(self, newsletter_id):
        newsletter = Newsletter.query.get(newsletter_id)
        return self._convert_to_dict(newsletter) if newsletter else None

    def create_newsletter(self, data):
        newsletter = Newsletter(**data)
        db.session.add(newsletter)
        db.session.commit()
        return self._convert_to_dict(newsletter)

    def update_newsletter(self, newsletter_id, data):
        newsletter = Newsletter.query.get(newsletter_id)
        if newsletter:
            for key, value in data.items():
                setattr(newsletter, key, value)
            db.session.commit()
            return self._convert_to_dict(newsletter)
        return None

    def delete_newsletter(self, newsletter_id):
        newsletter = Newsletter.query.get(newsletter_id)
        if newsletter:
            db.session.delete(newsletter)
            db.session.commit()
            return True
        return False

    def _convert_to_dict(self, newsletter):
        if newsletter:
            return {key: getattr(newsletter, key) for key in newsletter.__dict__.keys() if not key.startswith('_')}
        return None

#newsletterbot
    def get_bot_credentials(self):
        return NewsLetterBot.query.first()

    def create_or_update_bot_credentials(self,bot_token, channel_id):
        credentials = NewsLetterBot.query.first()
        if not credentials:
            credentials = NewsLetterBot(bot_token=bot_token, channel_id=channel_id)
        else:
            credentials.bot_token = bot_token
            credentials.channel_id = channel_id

        db.session.add(credentials)
        db.session.commit()

    def get_bot_credentials(self):
        # Fetch bot credentials from the database
        bot = NewsLetterBot.query.first()
        if bot:
            return bot.bot_token, bot.channel_id
        return None, None