# DigitalCoach

Senior Design Project for Fall 2022-Spring 2023

DigitalCoach is an AI-powered interview prep web application that allows job seekers to practice interviewing and receive immediate feedback. Some key features of DigitalCoach include creating interview sets from our database of questions and then recording corresponding video responses. Our AI uses machine learning models to analyze audio and video through a sentiment analysis. At the end, users are left with an overall score and actionable feedback.

For more detailed documentation on the different parts of the app ([frontend](/digital-coach-app/README.md), [ml-api](/ml-api/README.md), [ml model](/ml/README.md)) refer to the README.md file in the root directory of the folders.

# Setup Instructions

## Setup

1. Create a firebase app [here](https://console.firebase.google.com)
1. Create a service account for the firebase app you've created using the Google Cloud console with [instructions here](https://cloud.google.com/iam/docs/creating-managing-service-accounts#creating)
1. Populate the `.env` files in `digital-coach-app/` and `digital-coach-app/functions/` directory with the service account credentials. The files in the repository are just sample env files. Make sure that the files are named .env without the example part!
1. Install the latest stable version of Node [here](https://nodejs.org/en/)
1. Install yarn [here](https://classic.yarnpkg.com/en/docs/install)
1. Install Python 3.10 [here](https://www.python.org/downloads/)
1. Install redis [here](https://redis.io/docs/getting-started/)
1. Install pipenv [here](https://pipenv.pypa.io/en/latest/)
   - Make sure you run this in administrator mode if you're on Windows!
1. Install nltk with `pip install nltk`
1. Open python with `python` in the command line
   - Ensure you are running python 3.10!
1. Type into the python console:
   ```
   import nltk
   nltk.download()
   ```
   and download all packages in the UI prompt (sorry we didn't figure out which ones you really need)
1. Create an account with Assembly AI and get an API key
1. Populate the .env file in `ml-api/` with the API key from AssemblyAI. The files in the repository are just sample env files. Make sure that the files are named .env without the example part!
1. Ensure that firebase is connected: run `firebase login` and click the link to login and authenticate
1. Run `firebase projects:list` to see the projectId
1. Set the current project using the projectId from the previous step: `firebase use <projectId>`

## Frontend

- Prerequisites
  - Ensure you are running Windows or Ubuntu to avoid complier issues
  - Use Node v20.19.2

1. cd to the `digital-coach-app` directory
1. run `yarn install` to install dependencies for Next.JS
1. run `npm install -g firebase-tools` to install firebase
1. cd to the `functions` directory
1. run `yarn install` to install dependencies for the firebase functions
1. run `yarn add typescript@latest` to upgrade typescript
1. run `yarn build --skipLibCheck` to build the firebase functions modules
1. cd back to the `digital-coach-app` directory
1. run `yarn run emulate` to run the firebase emulator
1. in another terminal in the `digital-coach-app` directory, run `yarn run dev` to run the Next.JS dev server
1. Navigate to `localhost:3000/api/seed` to seed the database.

- The Next.JS dev server is served at `localhost:3000`
- The Firebase emulation console is served at `localhost:4000`

## Backend

1. start your redis server with the instructions from the installation page [here](https://redis.io/docs/getting-started/)
1. cd to the `ml-api` directory
1. run `pipenv install` to install the dependencies for the flask API
1. run `pipenv run serve` to start the Flask API server

## Local LLM Setup
The AI model(s) used for this application are implemented via the Docker Model Runner (DMR). This provides the following advantages:

1. Portability between systems. (AI models should work with NVIDIA, AMD, and Intel GPUs).
2. Switching between models requires minimal code changes (see below for steps).
3. Docker model runner can use both the CPU and/or GPU for AI inference with little configuration.

To set up the AI model(s) on your host machine, do the following steps:

1. Open Docker Desktop, then go to settings which should be a gear icon on the top right, and then select the “AI” section.
2. Enable the following options:
    - “Enable Docker Model Runner”
    - “Enable host-side TCP support” (use the default port number)
    - “Enable GPU-backed inference” (if you don’t see this option then ignore this)
3. Download the AI model’s file. In `mlapi/.env.example` there should be a `MODEL` environment variable that’s populated with the name of the current AI model being used (in the later section we’ve provided steps for how to change the AI model). In your host machine’s terminal, run the following command: `docker model pull <model-name>`.

Congratulations, you have a local LLM on your machine that the web application can use for ML tasks! You can also use it personally within Docker Desktop by selecting the “Models” tab in the left-hand side of the Docker Desktop navigation bar, and then selecting the AI model that you downloaded.

If you want to switch to a different model, Docker Hub has plenty of AI models to choose from. However, be mindful of the AI model’s size because if its too large and can’t fit in your GPU’s VRAM then AI inference will take much longer or fail. After you find a model, you must perform the following: 

1. In `mlapi/.env`, change the environment variable `MODEL` to be `MODEL="ai/<model-name>"` where `<model-name>` can be found when you visit that specific AI model’s Docker Hub page under the “Variant” category and make sure to copy the entire name listed.
2. In `/docker-compose.yml` in the top-level `models` section, change the `model` field to also be `model: ai/<model-name>`

Notes: 
- We don’t recommend using a system that doesn’t have a GPU because CPU inference is very slow (e.g. GPU-bound inference ETC 30s, CPU-bound inference ETC 10mins).
- As far as we know, if you have a GPU then there isn’t a way to set up DMR so that it only uses your CPU for inference. This shouldn’t be a problem and makes sense because GPU-bound inference is much faster than CPU-bound inference.
- The model itself will be hosted on your host machine and NOT a container.
- If you make changes to the configuration of the model within `docker-compose.yml`, you may have to unload and then load the model back again for the configurations to take effect because DMR is separate from Docker Compose. Specifically, after closing the application with `docker-compose down`, unload the model with `docker model rm <model-name>` and then redownload it with `docker model pull <model-name>`.
- It's possible that DMR ignores the context_size field defined in the LLM section of the `docker-compose.yml` file. If that's the case then run `docker model configure --context-size <size_value> <model_name>` where `<size_value>` if your desired context window size and `<model_name>` is the name of your LLM.

## (Optional) Hosting Guide
You may want to host this website on the internet for beta testing purposes. The easiest way we found was basically to get a cloud virtual machine, set up the application like on our host machine, and then get a domain so other people can use the application. Thankfully, being a student allows this process to be free (for approximately a year). Specifically, Github Student Developer Pack (GSDP) gives students access to a variety of perks, two of which this guide will utilize. Before continuing, register for the Github Student Developer Pack.

First, we have to get a cloud virtual machine. GSDP offers a perk with DigitalOcean (cloud hosting platform) giving you $200 in credits for 1 year which should be plenty for our use case. Accept the offer with your Github account and then create a Droplet which is a LINUX-BASED virtual machine. You can set up the Droplet from scratch or use their 1-click Docker Droplet which has Docker Engine and Docker Compose pre-installed [here](https://marketplace.digitalocean.com/apps/docker).

After you have Docker set up, you can follow the same guide used to set up the DigitalCoach application.  An important step is to make sure in your `docker-compose.yml` file, all services that will be using your local LLM will have the the following in their section:

```
extra_hosts:
      - "host.docker.internal:host-gateway"
```

This is because the Docker Engine doesn’t automatically have `host.docker.internal` set up unlike with Docker Desktop.

Additionally, you must configure your Droplet’s firewall settings so that it can be accessed from the internet. Specifically, go to your Droplet’s “Networking” tab and then “Manage Firewalls”. You want to create a firewall that has inbound rules for port 80 (HTTP), port 443 (HTTPS) and port 8000 (your FastAPI server) for all IPv4 and IPv6 sources. Now we can set up HTTPS access for our Droplet.

Technically, our Droplet can be accessed by going to `http://your_droplets_public_ipv4` but the application won’t work. Since our application requires access to the user’s camera and microphone, the app must be hosted over HTTPS. To set that up we first need a domain name which brings us to the next GSDP perk from Namecheap. GSDP gives us ownership of a `.me` domain for 1 year free. Make an account with Namecheap using your Github account and then get your free domain.

After registering for your domain, we must set up DNS so your Droplet’s IPv4 is mapped to your domain name. Go to your Namecheap dashboard and then select the “Domain List” tab and select the “Manage” button next to your newly registered domain. Next, select “Advanced DNS” where there should be some entries already but feel free to delete them. Then, under the “Host Records” section, click on “Add new record”, select “A Record” and then put `@` for the host to refer to your domain name and then type in your Droplet’s IPv4 address for the value and then have TTL be “Automatic”. Optionally, if you want people to access your website with `www` you can do the following.  Click “Add a new record” again and select “CNAME Record”, then have the Host be `www`, and then enter your domain name for the value, and have TTL be “Automatic”. It may take a while for these changes to propagate to all the DNS servers that make up the internet but you can check if it’s done with DNS lookup websites like [this](https://www.whatsmydns.net/) where you can enter your domain name and if it worked, you should see the IPv4 address of your Droplet.

Next, we need to make your website HTTPS accessible and we can do so using a free SSL certificate provided by Let’s Encrypt (this doesn’t require you to be eligible for GSDP). Since we’re using multiple Docker containers, we also must configure Nginx as a reverse proxy and tell it how to route incoming traffic to our internal ports, e.g. 8000 for the backend and 3000 for the frontend. This is better explained by following a YouTube tutorial like [this](https://youtu.be/spbkCihFpQ8?t=182) (this link starts the video at the timestamp that’s relevant for our setup).

If you’re following the video that we linked then you’ll notice that you must create a Nginx configuration file at `/etc/nginx/sites-available/your_domain_name` within your Droplet. You can ignore the video’s configuration files and use the following:

```
server {
    server_name your_domain_name www.your_domain_name;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Notice that any requests with `/api/` will be routed to our FastAPI server, therefore, whenever you create new FastAPI routes, ensure they start with `/api/` so Nginx knows to reroute the request to `localhost:8000` where the server lives within the Droplet.

At this point, your application should now be accessible on the internet by typing `https://domain_name`. You can still view the RQ Dashboard and our other backend endpoints manually using `http://domain_name:8000/`. One final thing is to make sure your application knows where your backend is when it makes its requests using the Fetch API. To do so, in your `digital-coach-app/.env` file, change the value in `NEXT_PUBLIC_HOST` to be `https://domain_name`. Nginx will handle requests on ports 80 and 443 with the configuration that you set it up with and it knows when to route requests either to our FastAPI server or our Next.js frontend.

That’s it, enjoy your newly hosted web application! An important note is that once the frontend is on `https://` it can’t make requests to `http://` domains as that will trigger a Mixed Content security error and block that request.

# Technologies Used

## Frontend

- Next.JS
- React
- Firebase
  - Storage
  - Firestore
  - Functions
- Sass

## Build Tools

- Yarn
- Pipenv

## Machine Learning API

- Flask
- Redis

## Machine Learning Model

- RQ
- AssemblyAI
- FER
- Numpy
- Scipy
- Matplotlib
- Jupyter Notebook
- Keras
- OpenCV
- Tensorflow
- NLTK

# Members

- Ming Lin (Fullstack)
- Max Shi (Fullstack)
- Hamzah Nizami (Machine Learning)
- Suzy Shailesh (UX/UI Design)
- Michael McCreesh (QA)
- Aparajita Rana (Product Management)
