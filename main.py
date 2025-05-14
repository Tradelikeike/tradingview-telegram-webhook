from flask import Flask, request
from telegram import Bot
import json
import os

app = Flask(__name__)

# Telegram bot settings
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7821525599:AAHaVtzLI6hLoRaEce3gKPkYby5Vk7ujXz0")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "-1002545667267")

# Initialize the Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get the incoming webhook data from TradingView
        data = request.get_json()
        print(f"Received webhook data: {data}")  # Log the incoming data

        # Extract ticker, close price, and signal type from the webhook
        ticker = data.get('ticker', 'Unknown')
        close_price = float(data.get('close', 0))  # Convert close price to float
        signal_type = data.get('signal', 'buy').lower()  # Default to 'buy' if signal is not provided
        print(f"Parsed data - ticker: {ticker}, close_price: {close_price}, signal_type: {signal_type}")

        # Format the message based on signal type
        if signal_type == "buy":
            entry = close_price
            message = (
                f"📈 *Buy Signal for {ticker}*\n\n"
                f"📍 *Entry*: {entry} - {entry - 2}\n"
                f"🎯 *TP1*: {entry + 2}\n"
                f"🎯 *TP2*: {entry + 4}\n"
                f"🎯 *TP3*: {entry + 6}\n"
                f"🎯 *TP4*: {entry + 8}\n"
                f"🛑 *SL*: {entry - 6}\n\n"
                f"⚠️ Use proper risk management!\n"
                f"🚨Account For & Subtract Spread from TP1\n"
                f"📊 Layer your entries.\n"
                f"💰 Send me all your profits to @tradelikeike"
            )
        elif signal_type == "sell":
            entry = close_price
            message = (
                f"📉 *Sell Signal for {ticker}*\n\n"
                f"📍 *Entry*: {entry} - {entry + 2}\n"
                f"🎯 *TP1*: {entry - 2}\n"
                f"🎯 *TP2*: {entry - 4}\n"
                f"🎯 *TP3*: {entry - 6}\n"
                f"🎯 *TP4*: {entry - 8}\n"
                f"🛑 *SL*: {entry + 6}\n\n"
                f"⚠️ Use proper risk management!\n"
                f"🚨Account For & Subtract Spread from TP1\n"
                f"📊 Layer your entries.\n"
                f"💰 Send me all your profits to @tradelikeike"
            )
        else:
            message = f"⚠️ Invalid signal type '{signal_type}' for {ticker}. Must be 'buy' or 'sell'."
            print(f"Error: Invalid signal type '{signal_type}'")
            return {"status": "error", "message": f"Invalid signal type: {signal_type}"}, 400

        # Send the message to Telegram with error handling
        try:
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode='Markdown', disable_web_page_preview=True)
        except Exception as e:
            print(f"Error sending Telegram message: {str(e)}")
            return {"status": "error", "message": f"Failed to send Telegram message: {str(e)}"}, 500

        # Respond to TradingView to confirm receipt
        return {"status": "success"}, 200

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return {"status": "error", "message": f"Webhook processing failed: {str(e)}"}, 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
