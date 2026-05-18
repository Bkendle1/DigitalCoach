# Digital Coach

Senior Design Project for Fall 2025 - Spring 2026

Digital Coach is an AI-powered interview prep web application that allows job seekers to practice interviewing and receive personalized, actionable feedback. Key features of Digital Coach include creating interview sets from our database of questions and then recording corresponding video responses and realtime mock interviews with an AI avatar. Our app uses machine learning models to analyze audio and video against common interview metrics such as the STAR framework. At the end, users are provided with scores for each metric along with feedback focused on that metric and an overall performance score accompanied with actionable feedback.

For more detailed documentation on the different parts of the app ([frontend](/digital-coach-app/README.md) and [mlapi](/mlapi/README.md)) refer to the README.md file in the root directory of the folders.

# Setup Instructions

## Frontend
1. Create a Firebase project [here](https://console.firebase.google.com)
1. Within your Firebase project, create a Web app by going to **Project Overview** -> **Add app**.
1. Within your Firebase project, enable Authentication and Firestore services. Within the Authentication service, go to **Sign-in method** -> **Add new provider** and enable "Email/Password" sign-in method.
1. Get your Firebase configurations by going to **Settings** -> **General** and scrolling down to where you should see your web app selected.
1. Duplicate the `.env.example` file in `/digital-coach-app` directory and rename it as `.env`. Populate the `.env` file with the Firebase configurations from the previous step.
1. Install Node LTS [here](https://nodejs.org/en/)
1. `cd` into the `/digital-coach-app` directory and run `npm install` to install all npm packages needed by the frontend.

## Backend
1. Install Python 3.10 [here](https://www.python.org/downloads/)
1. Create an account with AssemblyAI [here](https://www.assemblyai.com/dashboard/signup) and get an API key.
1. Copy the `env.example` file in the `/mlapi` directory and rename it `.env`. Populate the `AAPI_KEY` key in the `.env` file with the API key from AssemblyAI.
1. Create a HeyGen LiveAvatar account [here](https://app.liveavatar.com/signin) and get an API key.
1. Populate the `HEYGEN_LIVEAVATAR_API` key in the `.env` file with the API key from HeyGen LiveAvatar.
1. Install uv for install Python packages [here](https://docs.astral.sh/uv/getting-started/installation/).
1. Run `uv sync` to create a Python virtual environment with all the dependencies installed. 
From now on, when you’re working on the backend, its recommended that you use the virtual environment by running `mlapi/.venv/Scripts/activate` in your project's terminal.

## Docker Compose
To manage all the technologies used for this application, we chose Docker for containerization. This has the benefit of portability across various systems and also has Docker Model Runner which makes hosting local LLMs easier.
1. Download Docker Desktop [here](https://www.docker.com/products/docker-desktop/)
1. Run `docker compose build` to create the images defined in the `docker-compose.yml` file. This may take a few minutes. 
    - **NOTE**: Whenever you add/remove dependencies from this project you MUST rebuild the images with the same command.
1. To start the application, run `docker compose up -d` the `-d` flag is optional but it runs your containers in the background which frees up your terminal. 

When the application's containers are spun up, you have access to the following:
- The FastAPI server listens on `localhost:8000`.
- The Next.js website is served at `localhost:3000`.
- The Firebase emulation console is served at `localhost:4000`.


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

Next, we need to make your website HTTPS accessible and we can do so using a free SSL certificate provided by Let’s Encrypt (this doesn’t require you to be eligible for GSDP). Since we’re using multiple Docker containers, we also must configure Nginx as a reverse proxy and tell it how to route incoming traffic to our internal ports, e.g. 8000 for the backend and 3000 for the frontend. This is better explained by following a YouTube tutorial like [this](https://github.com/user-attachments/assets/02bd9c26-7834-40a3-8d49-42d5ad6b3ce0
) (you can start at 3:00 timestamp within the video as that’s relevant for our setup).

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

- Next.js
- React
- TypeScript
- Firebase
  - Storage (emulator only)
  - Firestore
  - Authentication
- Sass
- Cloudinary

## Backend
- FastAPI 
- Pydantic
- Firebase
    - Firestore
- Redis' RQ (workers for ML tasks)
- OpenAI (manage OpenAI-compliant ML models)

## Machine Learning Model

- AssemblyAI (transcription)
- Docker Model Runner (local LLM)
- HeyGen LiveAvatar (mock interview avatar)

# Members

- Britt Li Kendle
- Ivana Lu
- Hans Iselborn
- Mikkail Allen
- Thomas Kain
- Isabella Baratta
