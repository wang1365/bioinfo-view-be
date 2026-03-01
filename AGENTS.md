# BACKEND ROOT KNOWLEDGE BASE

## OVERVIEW
Backend umbrella directory for deployment/runtime assets and Django service source.
Primary application logic lives in `bioinformatics-analysis/`.

## STRUCTURE
```text
bioinfo-view-be/
├── bioinformatics-analysis/   # Django project root (main code)
├── docker-compose.yml         # runtime orchestration
├── docker-compose-offline.yml # offline deployment variant
├── init/                      # initialization artifacts
├── frontend/                  # backend-side static serving container assets
├── static/                    # docs/screenshots/static resources
└── spec/                      # additional specs/scripts
```

## WHERE TO LOOK
| Task | Location | Notes |
|---|---|---|
| Django app code | `bioinformatics-analysis/` | See nested AGENTS.md |
| Container orchestration | `docker-compose*.yml` | Service wiring + env |
| Backend image build | `bioinformatics-analysis/Dockerfile` | Python service image |
| Frontend static container | `frontend/` | Nginx/static packaging |

## COMMAND ENTRY POINTS
```bash
cd bioinformatics-analysis
python manage.py runserver
python manage.py test
python manage.py migrate
```

## CONVENTIONS
- Treat this folder as orchestration boundary; business/domain changes belong in Django project subtree.
- Keep compose/runtime docs here; keep API/domain rules in nested AGENTS.

## ANTI-PATTERNS
- Do not edit `bioinformatics-analysis/venv/` contents.
- Do not mix deployment concerns into app-layer modules.

## NOTES
- Child instructions in `bioinformatics-analysis/AGENTS.md` override this file for Django source edits.
