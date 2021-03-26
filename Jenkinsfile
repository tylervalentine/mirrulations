pipeline {
  agent {
    docker {
      image 'python:3.8'
    }
  }
  stages {
    stage('Create Virtual Environment') {
      steps {
        sh '''
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -e .
        '''
      }
    }

    stage('Unit Tests') {
      steps {
        sh '''
          . .venv/bin/activate
          make test
        '''
      }
    }
    stage('Static Analysis') {
      steps {
        sh '''
          . .venv/bin/activate
          make static
        '''
      }
    }
  }
}
