pipeline {
    agent none
    stages {
        stage('Preparation') {
            agent any
            steps {
                sh 'ls -l'
                // git 'https://github.com/maduma/user-and-group.git'
                sh 'docker build -f Dockerfile.test -t user-and-group:test .'
                sh 'ls -l'
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
