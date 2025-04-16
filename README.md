# Full-Stack Project

Welcome to our Full-Stack Recipe Application! This project is a comprehensive solution for all your recipe needs, combining the power of **Svelte** on the frontend and **Python** on the backend. The project is designed to showcase a web application with a clean separation between client-side (frontend) and server-side (backend) code.

<img width="1636" alt="VietSpark " src="https://github.com/user-attachments/assets/e88a1d38-a860-469a-a7ca-8aee8798a243" />

## Project Overview

Our application is designed to make your culinary journey easier and more enjoyable. With a sleek and intuitive interface, you can effortlessly generate, save, add, and delete recipes. The application is fully deployed and mobile-friendly, ensuring you can access your recipes anytime, anywhere.

## Table of Contents
- [Full-Stack Project](#full-stack-project)
  - [Project Overview](#project-overview)
  - [Table of Contents](#table-of-contents)
  - [Technologies Used](#technologies-used)
    - [Frontend:](#frontend)
    - [Backend:](#backend)
  - [Project Structure](#project-structure)
  - [Environment Variables](#environment-variables)
  - [Frontend Setup](#frontend-setup)
  - [Backend Setup](#backend-setup)
  - [License](#license)

## Technologies Used

### Frontend:
- **Svelte** - A modern JavaScript framework for building user interfaces.
- **Vite** - A fast development server and build tool for Svelte.
- **Tailwind CSS** - A utility-first CSS framework for styling.

### Backend:
- **Python** - The server-side language for backend logic.
- **FastAPI** (or any Python web framework you choose) - A modern, fast (high-performance) web framework for building APIs with Python.
- **LLM** - A large language model for generating recipes.

## Project Structure

### Backend
```

```
### Frontend
```
frontend/
│── src/
│   ├── lib/                  # Reusable components, utilities, stores
│   │   ├── components/        # Custom components
│   │   ├── stores/            # Svelte stores
│   │   ├── firebase/          # Firebase configuration
│   │   └── images/            # Global images
│   │
│   ├── routes/                # SvelteKit pages & API endpoints
│   │   ├── +layout.svelte      # Root layout (navbar, footer, etc.)
│   │   ├── +page.svelte        # Home page
│   │   └── authentication/     # Register page
│   │   └── login/              # Login page
│   │   └── recipe/             # Recipe page
│   │   └── user/               # User profile page
│   │
│   ├── +layout.svelte          # Layout for all pages
│   ├── +page.svelte            # Home page (landing page)
│
├── static/                    # Static assets (images, fonts, etc.)
│
├── .env                       # Environment variables
├── svelte.config.js           # SvelteKit config
├── tailwind.config.cjs        # TailwindCSS config
├── postcss.config.cjs         # PostCSS config
└── package.json               # Project dependencies & scripts
```


## Environment Variables
### Backend
Before running backend, you need to set up the environment variables. Create a `.env` file in the `Backend/tams_prototype/firebase` directory and add the following variables:
```
APIKEY=
AUTHDOMAIN=
DATABASEURL=
PROJECTID =
STORAGEBUCKET =
MESSAGINGSENDERID =
APPID =
MEASUREMENTID=
SERVICE_ACCOUNT_KEY=
OAI_API_KEY=
CALORIES_NINJAS_API_KEY=
```

### Frontend
Before running frontend, you need to set up the environment variables. Create a `.env` file in the `Frontend` directory and add the following variables:
```
VITE_API_KEY=
VITE_GMAP_API_KEY=
```

## Frontend Setup

To run the frontend, follow these steps:
```
cd Frontend
npm install
npm run dev
```

Access the application in your browser at `http://localhost:5173`.


## Backend Setup
Before setting up the backend, create a virtual environment and activate it:
* On Windows:
```
python -m venv venv
venv\Scripts\activate
```

* On macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate 
```  

To set up the backend, follow these steps:
```
cd Backend/tams-prototype/firebase
pip install -r requirements.txt
uvicorn main:app --reload

```


## License
