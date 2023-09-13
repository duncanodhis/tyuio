from app import db  # Import your database instance
from models.user import (
    ShopBot,
    CourierBot,
    DisputesReviewsBot,
    NewsletterChannel
)

class BotManagementService:
   
    def create_shop_telegram_bot(self,token):
        shop_bot = ShopBot(token=token)
        db.session.add(shop_bot)
        db.session.commit()
        return shop_bot

  
    def create_courier_telegram_bot(self,token):
        courier_bot = CourierBot(token=token)
        db.session.add(courier_bot)
        db.session.commit()
        return courier_bot

  
    def create_disputes_reviews_bot(self,token):
        disputes_reviews_bot = DisputesReviewsBot(token=token)
        db.session.add(disputes_reviews_bot)
        db.session.commit()
        return disputes_reviews_bot

 
    def create_newsletter_channel(self,channel_id, token):
        newsletter_channel = NewsletterChannel(channel_id=channel_id, token=token)
        db.session.add(newsletter_channel)
        db.session.commit()
        return newsletter_channel

   
    def get_shop_telegram_bot(self,bot_id):
        return ShopBot.query.get(bot_id)

    def get_courier_telegram_bot(self,bot_id):
        return CourierBot.query.get(bot_id)


    def get_disputes_reviews_bot(self,bot_id):
        return DisputesReviewsBot.query.get(bot_id)


    def get_newsletter_channel(self,channel_id):
        return NewsletterChannel.query.get(channel_id)


    def update_shop_telegram_bot(self,bot_id, new_token):
        shop_bot = ShopBot.query.get(bot_id)
        if shop_bot:
            shop_bot.token = new_token
            db.session.commit()
        return shop_bot


    def update_courier_telegram_bot(self,bot_id, new_token):
        courier_bot = CourierBot.query.get(bot_id)
        if courier_bot:
            courier_bot.token = new_token
            db.session.commit()
        return courier_bot


    def update_disputes_reviews_bot(self,bot_id, new_token):
        disputes_reviews_bot = DisputesReviewsBot.query.get(bot_id)
        if disputes_reviews_bot:
            disputes_reviews_bot.token = new_token
            db.session.commit()
        return disputes_reviews_bot

 
    def update_newsletter_channel(self,channel_id, new_token):
        newsletter_channel = NewsletterChannel.query.get(channel_id)
        if newsletter_channel:
            newsletter_channel.token = new_token
            db.session.commit()
        return newsletter_channel


    def delete_shop_telegram_bot(self,bot_id):
        shop_bot = ShopBot.query.get(bot_id)
        if shop_bot:
            db.session.delete(shop_bot)
            db.session.commit()
        return shop_bot


    def delete_courier_telegram_bot(self,bot_id):
        courier_bot = CourierBot.query.get(bot_id)
        if courier_bot:
            db.session.delete(courier_bot)
            db.session.commit()
        return courier_bot


    def delete_disputes_reviews_bot(self,bot_id):
        disputes_reviews_bot = DisputesReviewsBot.query.get(bot_id)
        if disputes_reviews_bot:
            db.session.delete(disputes_reviews_bot)
            db.session.commit()
        return disputes_reviews_bot


    def delete_newsletter_channel(self,channel_id):
        newsletter_channel = NewsletterChannel.query.get(channel_id)
        if newsletter_channel:
            db.session.delete(newsletter_channel)
            db.session.commit()
        return newsletter_channel


    def get_latest_shop_telegram_bot(self):
        # Retrieve the latest ShopTelegramBot entry from the database
        return ShopBot.query.order_by(ShopBot.id.desc()).first()

    def get_latest_courier_telegram_bot(self):
        # Retrieve the latest CourierTelegramBot entry from the database
        return CourierBot.query.order_by(CourierBot.id.desc()).first()

    def get_latest_disputes_reviews_bot(self):
        # Retrieve the latest DisputesReviewsBot entry from the database
        return DisputesReviewsBot.query.order_by(DisputesReviewsBot.id.desc()).first()

    def get_latest_newsletter_channel(self):
        # Retrieve the latest NewsletterChannel entry from the database
        return NewsletterChannel.query.order_by(NewsletterChannel.id.desc()).first()
