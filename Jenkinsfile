pipeline {
    agent any

    environment {
        IMAGE_TAG = ''
        FLASK_IMAGE = "aayushhhsharma/flaskapp"
        LOGGER_IMAGE = "aayushhhsharma/logger"
        DB_IMAGE = "aayushhhsharma/db"
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/aayushhhsharma/testMulti.git'
            }
        }

        stage('Set Image Tag') {
            steps {
                script {
                    IMAGE_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    echo "Using IMAGE_TAG: ${IMAGE_TAG}"
                }
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'DockerHub', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                }
            }
        }

        stage('Build and Push Flask Image') {
            steps {
                sh "docker build -t ${FLASK_IMAGE}:${IMAGE_TAG} ./Simple-Flask-Calculator"
                sh "docker push ${FLASK_IMAGE}:${IMAGE_TAG}"
            }
        }

        stage('Build and Push Logger Image') {
            steps {
                sh "docker build -t ${LOGGER_IMAGE}:${IMAGE_TAG} ./loggerService"
                sh "docker push ${LOGGER_IMAGE}:${IMAGE_TAG}"
            }
        }

        // stage('Build and Push DB Image') {
        //     steps {
        //         sh "docker build -t ${DB_IMAGE}:${IMAGE_TAG} ./db"
        //         sh "docker push ${DB_IMAGE}:${IMAGE_TAG}"
        //     }
        // }

        stage('Deploy') {
            steps {
                withEnv(["IMAGE_TAG=${IMAGE_TAG}"]) {
                    sh 'docker-compose up -d'
                }
            }
        }
    }
}
