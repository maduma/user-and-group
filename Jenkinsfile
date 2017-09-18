pipeline {
    agent none
    stages {
        stage('Preparation') {
            agent any
            steps {
                git 'https://github.com/maduma/user-and-group.git'
                sh 'docker build -f Dockerfile.test -t user-and-group:test .'
            }
        }
        stage('test') {
            agent { docker 'user-and-group:test' }
            steps {
                sh 'python test.py'
            }
        }
    }
}
