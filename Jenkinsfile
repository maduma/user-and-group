pipeline {
    agent none
    stages {
        stage('Build Test Image') {
            agent any
            steps {
                sh 'docker build -f Dockerfile.test -t user-and-group:test .'
            }
        }
        stage('Unit Test') {
            agent { docker 'user-and-group:test' }
            steps {
                sh 'python test.py'
            }
        }
        stage('Smoke Test') {
            agent { docker 'user-and-group:test' }
            steps {
                sh 'ls -l'
            }
        }
        stage('Build Prod Image') {
            agent any
            steps {
                sh 'docker build -f Dockerfile.prod -t user-and-group:prod .'
            }
        }
    }
}
