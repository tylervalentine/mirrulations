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
          pip install -r requirements.txt
          pip install .
        '''
      }
    }
    stage('Hello World')[
      steps{
        sh '''
          echo Hello World
        '''
      }
    ]

//    stage('Unit Tests') {
//      steps {
//        sh '''
//          . .venv/bin/activate
//          pytest
//        '''
//      }
//    }
//    stage('Static Analysis') {
//      steps {
//        sh '''
//          . .venv/bin/activate
//          pylint src/c21server/*.py tests/c21server/*.py
//        '''
//      }
//    }
  }
}
