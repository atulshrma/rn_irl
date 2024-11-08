FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install streamlit && \
    pip install bcrypt && \
    pip install numpy && \
    pip install scipy && \
    pip install matplotlib && \
    pip install sqlalchemy

COPY . .

RUN mkdir -p /var/lib/rn_irl && mv /app/irl.sdb /var/lib/rn_irl

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "Introduction.py", "--server.port=8501", "--server.address=0.0.0.0"]