pipeline {
    agent any
    stages {
        stage('Build Test Image') {
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
            steps {
                sh 'docker build -f Dockerfile.prod -t user-and-group:prod .'
            }
        }
        stage('Run Prod Image') {
            steps {
                sh 'docker inspect user_and_group >/dev/null 2>&1 && docker rm -f user_and_group'
                sh 'docker run -d -p 5000:5000 --name user_and_group user-and-group:prod'
            }
        }
    }
}
