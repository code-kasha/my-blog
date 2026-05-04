# Anime Blog

A Django blog project with custom user accounts, post publishing, comments, and like/dislike reactions.

## Features

- Custom user model with unique email, bio, and avatar fields
- User registration, login, logout, profile, and profile editing views
- Blog post create, read, update, and delete flows
- Slug-based post detail URLs
- Comment creation, editing, and deletion
- Like/dislike reactions for posts and comments
- SQLite-backed development setup
- Django templates with a shared base layout

## Tech Stack

- Python
- Django 6.0.4
- SQLite
- Django class-based views
- Django authentication

## Project Structure

```text
anime/
├── accounts/          # Custom user model, auth views, forms, middleware
├── base/              # Project settings, root URLs, ASGI/WSGI config
├── blog/              # Blog models, forms, views, URLs, migrations
├── media/             # Uploaded media files in development
├── staticfiles/       # Static files in development
├── templates/         # Shared project templates
├── db.sqlite3         # Local development database
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Getting Started

Clone the repository and move into the project directory:

```bash
git clone https://github.com/code-kasha/my-blog
cd my-blog
```

Create and activate a virtual environment:

```bash
python -m venv .env
```

On Windows:

```bash
.env\Scripts\activate
```

On macOS or Linux:

```bash
source .env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Run the development server:

```bash
python manage.py runserver
```

Open the app at:

```text
localhost:8000/
```

## Main Routes

These routes are mounted from `base/urls.py` and `blog/urls.py`:

| Route                          | Description       |
| ------------------------------ | ----------------- |
| `/`                            | Blog post list    |
| `/admin/`                      | Django admin      |
| `/post/create/`                | Create a post     |
| `/post/<slug>/`                | View a post       |
| `/post/<slug>/edit/`           | Edit a post       |
| `/post/<slug>/delete/`         | Delete a post     |
| `/post/<slug>/comment/create/` | Add a comment     |
| `/comment/<id>/edit/`          | Edit a comment    |
| `/comment/<id>/delete/`        | Delete a comment  |
| `/post/<slug>/react/like/`     | Like a post       |
| `/post/<slug>/react/dislike/`  | Dislike a post    |
| `/comment/<id>/react/like/`    | Like a comment    |
| `/comment/<id>/react/dislike/` | Dislike a comment |

Account routes are defined in `accounts/urls.py`. Include `accounts.urls` in `base/urls.py` when you want to enable registration, login, logout, and profile routes.

## Development Notes

- The default Django settings module is `base.settings`.
- Development uses SQLite through `db.sqlite3`.
- Uploaded files are stored in `media/`.
- Static files are served from `staticfiles/` during development.
- The project uses a custom user model: `accounts.User`.

## Useful Commands

Run checks:

```bash
python manage.py check
```

Make migrations after model changes:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

Format Python files:

```bash
black .
```

## License

Add a license before publishing if you want others to use or contribute to the project.
