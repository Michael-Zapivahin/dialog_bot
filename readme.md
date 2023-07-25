# The dialog bot  
  
This learning project for Telegram and VK's bots, interaction with  [DialogFlow](https://cloud.google.com/dialogflow/docs/) от Google.  

The service include the questions and answers from file `dictionaries/qustions.json`.  
  
For example my bot [zmg_dialog_bot](https://t.me/zmg_dialog_bot) and also group to VK [VKontakte](https://vk.com/club221731378)
  
## How to install

Python3 should already be installed. 
Use pip or pip3, if there is a conflict with Python2) to install dependencies:

```
pip install -r requirements.txt
```

## Program uses an environment variable

#### Variables:

```  
GOOGLE_APPLICATION_CREDENTIALS: link to Google Cloud service account
PROJECT_ID: ID project on Google Cloud 
BOT_TOKEN: telegram bot token
VK_TOKEN: VK goup token
TG_CHAT_ID: Chat ID for logs.
```  

# Start

```python
python bot.py # Telegram-bot
python vk_dialogflow.py # VK - bot
```

# Teaching bot 

```python
python upload_questions.py
```
  
Script `upload_questions.py` upload new answers and questions to service DialogFlow.   

## The aim of the project 
The code is written for educational purposes on the online course for web developers [Devman практика Python](https://dvmn.org/)