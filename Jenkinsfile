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
                git 'https://github.com/aayush5593/testMulti.git'
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
            stage('SonarQube Analysis') {
                steps {
                    withSonarQubeEnv('SonarQube') {
                        sh '/opt/sonar-scanner/bin/sonar-scanner'
                    }
                }
            }
        stage('Update Deployment YAML') {
            steps {
                script {
                    sh """
                    sed -i 's|image: aayushhhsharma/flaskapp:.*|image: ${FLASK_IMAGE}:${IMAGE_TAG}|' deployment.yaml
                    sed -i 's|image: aayushhhsharma/logger:.*|image: ${LOGGER_IMAGE}:${IMAGE_TAG}|' deployment.yaml
                    """
                }
            }
        }

        stage('Apply to Kubernetes') {
             steps {
                withCredentials([file(credentialsId: 'KubeCtlServer', variable: 'KUBECONFIG')]) {
                 sh 'kubectl apply -f deployment.yaml'
                }
            }
        }

    post {
    success {
        emailext(
            subject: "✅ Build Success: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
            body: "Good news! The build succeeded.\n\nJob: ${env.JOB_NAME}\nBuild Number: ${env.BUILD_NUMBER}\nCheck console output at: ${env.BUILD_URL}"
        )
        }
        failure {
            emailext(
                subject: "❌ Build Failure: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: "Oh no! The build failed.\n\nJob: ${env.JOB_NAME}\nBuild Number: ${env.BUILD_NUMBER}\nCheck console output at: ${env.BUILD_URL}"
            )
        }
    }
}
}
