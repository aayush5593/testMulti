pipeline {
    agent any

    environment {
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
                    def tag = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    env.IMAGE_TAG = tag
                    echo "Using IMAGE_TAG: ${env.IMAGE_TAG}"
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

        stage('Update Deployment YAML') {
            steps {
                script {
                    sh """
                    sed -i 's|image: aayushhhsharma/flaskapp:.*|image: ${FLASK_IMAGE}:${IMAGE_TAG}|' k8s/deployment.yaml
                    sed -i 's|image: aayushhhsharma/logger:.*|image: ${LOGGER_IMAGE}:${IMAGE_TAG}|' k8s/deployment.yaml
                    """
                }
            }
        }

        stage('Apply to Kubernetes') {
            steps {
                withCredentials([file(credentialsId: 'KubeCtlServer', variable: 'KUBECONFIG')]) {
                    sh 'echo "✅ Using kubeconfig from: $KUBECONFIG"'
                    sh 'kubectl config get-contexts --kubeconfig=$KUBECONFIG || echo "⚠️ Could not get contexts"'
                    sh 'kubectl get nodes --kubeconfig=$KUBECONFIG || echo "⚠️ Could not reach Kubernetes cluster"'
                     sh 'kubectl delete deployment prometheus --ignore-not-found=true --kubeconfig=$KUBECONFIG'
                    sh 'kubectl apply -f k8s/ --kubeconfig=$KUBECONFIG --validate=false'
                }
            }
        }
    }

    post {
        success {
            emailext(
                subject: "✅ Build Success: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """Good news! The build succeeded.

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Check console output at: ${env.BUILD_URL}
"""
            )
        }
        failure {
            emailext(
                subject: "❌ Build Failure: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
                body: """Oh no! The build failed.

Job: ${env.JOB_NAME}
Build Number: ${env.BUILD_NUMBER}
Check console output at: ${env.BUILD_URL}
"""
            )
        }
    }
}
