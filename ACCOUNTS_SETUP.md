# Accounts setup: Django account database + working sign-in

The project now has two parts that run side by side:

| Folder | What it is | How it runs |
|---|---|---|
| `backend/` | Django: the account database and the sign-in API | `python manage.py runserver` (port 8000) |
| everything else (`src/` etc.) | The React website from Figma Make | `npm run dev` (port 8443) |

The website sends sign-in and sign-up requests to Django, and Django checks
them against the database.

## One-time setup (Windows, VS Code)

You need Python (you already have it) and **Node.js LTS** from https://nodejs.org.

Open the project folder in VS Code, then open a terminal (`` Ctrl+` ``).

### 1. Set up the Django backend

```
cd backend
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations accounts
python manage.py migrate
```

`makemigrations` writes the instructions for building the accounts table,
and `migrate` creates the database file `backend/db.sqlite3` with that table
in it. (On Windows, if activation says scripts are disabled, run
`Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once.)

Optional but useful: create an admin login so you can look inside the database:

```
python manage.py createsuperuser
```

Check everything works by running the automated tests:

```
python manage.py test
```

You should see `Ran 6 tests ... OK`.

### 2. Set up the website

Open a **second** terminal (the `+` button in the terminal panel), make sure
you're in the main project folder (not `backend`), then:

```
npm install
```

## Every time you work on it

You need **both** running, each in its own terminal:

**Terminal 1: Django**
```
cd backend
.venv\Scripts\activate
python manage.py runserver
```

**Terminal 2: website**
```
npm run dev
```

Then open **http://localhost:8443** in your browser. Click Sign in, then
"Create account", and create an account. You're signed in straight away.
Sign out from the menu at the bottom left, then sign back in.

## Seeing the accounts in the database

Go to **http://127.0.0.1:8000/admin/** and log in with the superuser you
created. Click **Users** to see every account. Passwords appear as long
scrambled strings starting `pbkdf2_sha256$`. That's correct: Django
only ever stores a hash, never the real password.

## Where the code is

| File | What it does |
|---|---|
| `backend/accounts/models.py` | The account table (Django's built-in user, with email required and unique) |
| `backend/accounts/views.py` | Sign up, sign in, sign out and "who's signed in" |
| `backend/accounts/urls.py` | The API addresses: `/api/signup/`, `/api/login/`, `/api/logout/`, `/api/me/`, `/api/csrf/` |
| `backend/accounts/tests.py` | Automated tests (`python manage.py test`) |
| `backend/config/settings.py` | Django settings, including the database (SQLite) |
| `src/api.ts` | The website's side: functions that call the Django API |
| `src/App.tsx` → `Auth` | The sign-in screen, now sending what's typed to Django and showing errors |
| `vite.config.ts` → `proxy` | Forwards `/api/...` requests from the website to Django |

## Rules the sign-up form enforces

- Email, password and username are all required.
- Email must be valid and not already used (case doesn't matter).
- Username must not already be taken.
- Password: at least 8 characters, not a common password, not all numbers,
  not too similar to the username/email (Django's standard rules, set in
  `AUTH_PASSWORD_VALIDATORS` in settings.py).

## Not done yet

- **Forgot password** shows a "not set up yet" notice. Real reset emails need
  an email service configured in Django. Until then, reset passwords from the
  admin site.
- The **Settings** page and other library pages still show demo data
  ("Alex Morgan", the four sample games). Saving games per account is the
  next database step.
- `SECRET_KEY` and `DEBUG = True` in settings.py are for development only.
  Change them before putting the site online.

## Troubleshooting

- **"Can't reach the server. Is Django running?"** Terminal 1 isn't running
  `python manage.py runserver`, or it stopped with an error.
- **"no such table: accounts_user"** Run `python manage.py makemigrations accounts`
  and then `python manage.py migrate` inside `backend`.
- **"Security check failed"** Refresh the page and try again.
- **Port 8443 already in use** Close the other terminal running `npm run dev`.
