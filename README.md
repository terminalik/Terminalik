<div style="text-align: center;">
  <h1>
    Terminalik
  </h1>
</div>

<sub><sup>README written by AI)</sub></sup>

Terminalik is a Textual-based CLI/TUI that lets you spin up a project structure quickly and maintain your project with ease.

Why Would I Use This?
---------------------
Too lazy to write this

## Table of Contents

- [Install](#install)
- [Dev Install](#dev-install)
- [Frontend Frameworks Supported](#frontend-frameworks-supported)
- [Backend Frameworks Supported](#backend-frameworks-supported)
- [Database Support](#database-support)
- [Other Features](#other-features)
- [Demo](#demo)
- [Documentation](#documentation)
- [GitHub Stats](#github-stats)
- [License](#license)

<a id="install"></a>

<h2>
  <picture>
    <img src="./public/install.gif?raw=true" width="60px" style="margin-right: 1px;">
  </picture>
  Install
</h2>

Install via package managers is not yet available. Planned targets:

### Python (pipx)
```
pipx install terminalik   # not yet available
```

### UV
```
uv install terminalik   # not yet available
```

### Homebrew
```
brew install terminalik   # not yet available
```

<a id="dev-install"></a>

## Dev Install

```bash
git clone https://github.com/terminalik/TerminalikSSH.git
cd TerminalikSSH

python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# install dependencies from pyproject
pip install -e .

# run the TUI
python main.py
```

Frontend Frameworks Supported
-----------------------------
- [HTMX](https://htmx.org/)
- [Vue](https://vuejs.org/)
- [React](https://react.dev/)
- [Svelte](https://svelte.dev/)
- [SolidJS](https://www.solidjs.com/)
- [Alpine.js](https://alpinejs.dev/)
- [Angular](https://angular.io/)

Backend Frameworks Supported
----------------------------
Python
- [Django](https://www.djangoproject.com/)
- [Flask](https://flask.palletsprojects.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Starlette](https://www.starlette.io/)
- [Falcon](https://falcon.readthedocs.io/)

Go
- [Gin](https://github.com/gin-gonic/gin)
- [Chi](https://github.com/go-chi/chi)
- [Echo](https://github.com/labstack/echo)
- [Fiber](https://github.com/gofiber/fiber)

Node / JS Runtimes
- [Express](https://expressjs.com/)
- [Fastify](https://www.fastify.io/)
- [NestJS](https://nestjs.com/)
- [Koa](https://koajs.com/)
- [Hono](https://hono.dev/)
- [Bun](https://bun.sh/) + frameworks like [Elysia](https://elysiajs.com/)

Database Support
----------------
- [MySQL](https://www.mysql.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLite](https://www.sqlite.org/)
- [MongoDB](https://www.mongodb.com/)

Note: Docker files can be generated to help you wire a DB. Turnkey DB scaffolding is on the roadmap.

Other Features
--------------
- Dockerfiles for frontend and backend + docker-compose
- In-app README viewer (loads local README.md or fetches from GitHub)
- Optional GitHub Device Flow demo (`authFlow.py`)
- Runs well over SSH; recommended with `tmux` for persistent sessions

Demo
----
Not yet available.


Documentation
-------------
Not yet available.

<a id="github-stats"></a>

## GitHub Stats

<p align="center">
  <img alt="Alt" src="https://repobeats.axiom.co/api/embed/cef299e9c904903819554a7de3e8051a56698af0.svg" title="Repobeats analytics image"/>
</p>

<a id="license"></a>

## License

Licensed under the [MIT License](./LICENSE).
