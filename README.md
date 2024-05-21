# Celestial Alert

![Logo](https://raw.githubusercontent.com/astroclubiitt/CelestialAlert/main/assets/logo.png)

This is a discord bot developed for Gagan Vedhi Club server, the Astronomy club of Indian Institute of Technology, Tirupati. The bot checks the current location of the `International Space Station` periodically every 5 seconds and ping the server memebers when the ISS is in close promixity of the city.

## Installation and Running:

1. Clone the repository using the following command:

```bash
git clone https://github.com/astroclubiitt/CelestialAlert.git
```

2. Install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

3. Either you can run locally or deploy it in a virtual private server, or you can configure an Arduino zero to do it, since the bot is not heavy.

4. Create a `.env` file in the root directory and add the following variables:

```bash
TOKEN=YOUT_DISCORD_BOT_TOKEN
CHANNEL_ID=Channel id in which you want the bot to prompt
```

5. In Testing/debugging phase :

```bash
python bot.py
```

## Deployment:

1. You can deploy the bot in a virtual private server or in a cloud platform like Heroku, AWS, etc.
2. This bot is deployed on render and cron-jobs is used to monitor the uptime.
3. To deployt in render:
   - `build command`:
     - ```bash
       ./build.sh
       ```
   - `run command`:
     - ```bash
       python main.py
       ```

## Features:

1. The bot checks the current location of the `International Space Station` periodically every 5 seconds.
2. The bot pings the server memebers when the ISS is in close promixity of the city.

## Contributors:

1. [Ikshitha](https://github.com/Ikshitha1004) - Mentee
2. [Manas](https://github.com/scienmanas) - Mentor

## API Used:

1. [Open Notify API](http://open-notify.org/Open-Notify-API/)

## Citties Available:
 
-  Tirupati, Gorakhpur, Delhi, Kanpur, Kaharjpur, Mumbai, Bengaluru, Chennai, Kolkata, Hyderabad, Tokyo, London, Sydney, Paris, Singapore.

## Note: 

- The bot is not optimized and configures, so we advise you to create your own bot and configure it according to your needs by utilizing the code. use **`$help`** to get bot commands.

- Enable the intents so that it can read message events.

![Permissions](https://raw.githubusercontent.com/astroclubiitt/CelestialAlert/main/assets/permissions.png)

## Folder Structure:

```bash
.
├── assets
│   └── logo.png
│   └── permissions.png
│── .env
│    ├── TOKEN=Your Discord Bot Token
├── .gitignore
├── main.py
├── app.py 
├── bot.py
├── Procfile
├── LICENSE
├── README.md
└── requirements.txt
```

## License:

This project is licensed under the MIT License
