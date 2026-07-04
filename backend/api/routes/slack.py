from slack_bolt.async_app import AsyncApp 
from core.config import Settings
from services.agent.llm import agent


bot_token = Settings.SLACK_BOT_TOKEN
signing_secret = Settings.SLACK_SIGNING_SECRET


slack_app = AsyncApp(token=bot_token, signing_secret=signing_secret)


@slack_app.event("message")
async def handle_event(body, say, logger):
    #write code for what will happen when you aapp is mentioned
    
    # logger.info(body)
    
    message = body["event"]["text"]

    result = await agent.run(message)
    

    await say(result.output)


# @slack_app.event("message")
# async def handle_message_events(body, say, logger):
#     # Log the incoming body so you can see exactly what Slack is sending
#     logger.info(body)
    
#     event = body.get("event", {})
#     channel_type = event.get("channel_type")
    
#     # Strictly filter for Direct Messages (Instant Messages)
#     if channel_type == "im":
#         # Ignore messages sent by the bot itself to prevent an infinite loop!
#         if event.get("bot_id") is not None:
#             return
            
#         user_id = event.get("user")
#         text_received = event.get("text", "")
        
#         # Respond back to the user
#         await say(f"Hi <@{user_id}>! I received your DM: '{text_received}'")
