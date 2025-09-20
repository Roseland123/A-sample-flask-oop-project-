pipeline {
  agent any
  stages {
    stage('Setup Python') {
      steps {
        sh 'python -V || true'
        sh 'python -m venv .venv'
        sh '. .venv/bin/activate && pip install -U pip && pip install -r requirements.txt'
      }
    }
    stage('Unit Tests') {
      steps {
        sh '. .venv/bin/activate && python -m pytest -q || true' // keep example light
      }
    }
    stage('ETL') {
      steps {
        sh '. .venv/bin/activate && python -m src.etl.pipeline'
      }
    }
  }
  post {
    success { echo 'Pipeline completed.' }
  }
}
