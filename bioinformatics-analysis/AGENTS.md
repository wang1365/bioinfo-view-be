# DJANGO PROJECT KNOWLEDGE BASE

## OVERVIEW
Django backend for bioinformatics analysis, project/task management, reporting, and reference-genome workflows.
Apps are organized by domain (`account`, `project`, `sample`, `task`, etc.).

## WHERE TO LOOK
| Task | Location | Notes |
|---|---|---|
| Framework entry | `manage.py` | Management/test/run entrypoint |
| Project settings | `bioinformatics/settings/{dev,uat,prod}.py` | Env-specific behavior |
| URL routing | `bioinformatics/urls.py` | API route registration |
| WSGI app | `bioinformatics/wsgi.py` | Server gateway |
| Domain APIs/models | `<app>/views.py`, `<app>/models.py`, `<app>/serializers.py` | Per-app layering |
| App tests | `<app>/tests.py` | Django test baseline |

## HIGH-SIGNAL APPS
- `account/`: authentication/user ops
- `rbac/`: role/permission model
- `project/`, `sample/`, `patient/`: core domain entities
- `task/`, `flow/`, `report/`, `verdict/`: analysis orchestration and result interpretation
- `reference_genome/`: reference genome management

## COMMANDS
```bash
python manage.py runserver
python manage.py test
python manage.py test <app_name>
python manage.py migrate

# environment-specific run
DJANGO_SETTINGS_MODULE=bioinformatics.settings.dev python manage.py runserver
```

## CONVENTIONS
- Use per-app boundaries; avoid cross-app coupling unless shared in `common/` or explicit service layers.
- Keep request/response schemas in serializers; keep persistence in models/managers.
- Settings are split by environment; verify `DJANGO_SETTINGS_MODULE` before debugging behavior differences.

## TESTING PATTERN
- Primary test location: `<app>/tests.py` (Django test framework).
- Standalone script exists: `test_flow_filter.py` (project-root-level special case).

## ANTI-PATTERNS
- Do not edit `venv/` or generated caches (`__pycache__/`).
- Do not hardcode environment secrets in code or AGENTS docs.
- Do not assume pytest-first layout; default test flow is Django `manage.py test`.

## NOTES
- Keep AGENTS updates aligned with structural changes (new apps/settings layout changes).
