# Bonus (Critères de performance § 6) :
#   - Utilisateur non-root (USER non-root après mkdir + chown)
#   - HEALTHCHECK qui interroge /health
#   - Multi-stage build pour réduire la taille finale
#
# Commande type pour build et lancer une fois ce fichier complété :
#   docker build -t fastia-maintenance:dev .
#   docker run --rm -p 8000:8000 fastia-maintenance:dev
#   curl http://localhost:8000/health

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY model/ ./model

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]