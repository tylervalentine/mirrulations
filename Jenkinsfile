pipeline {
  agent {
    docker {
      image 'python:3.8'
    }
  }
  stages {
    stage('Hello World') {
      steps {
        sh '''
          echo Hello World
        '''
      }
    }
  }
}
