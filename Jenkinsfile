pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and push Docker image') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker buildx build --platform linux/amd64 \
                          -t tawa123/blog-k8s:latest \
                          --push .
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to EKS staging') {
            steps {
                sh '''
                    set -e

                    aws eks describe-cluster \
                      --name round2-eks \
                      --region us-east-1 \
                      --query cluster.certificateAuthority.data \
                      --output text | base64 --decode > /tmp/eks-ca.crt

                    TOKEN=$(aws eks get-token \
                      --cluster-name round2-eks \
                      --region us-east-1 \
                      --query status.token \
                      --output text)

                    ENDPOINT=$(aws eks describe-cluster \
                      --name round2-eks \
                      --region us-east-1 \
                      --query cluster.endpoint \
                      --output text)

                    helm upgrade --install staging ./helm/blog-chart \
                      --values ./helm/staging-values.yaml \
                      --namespace staging \
                      --kube-token "$TOKEN" \
                      --kube-apiserver "$ENDPOINT" \
                      --kube-ca-file /tmp/eks-ca.crt
                '''
            }
        }

        stage('Deploy to EKS production') {
            steps {
                sh '''
                    set -e

                    aws eks describe-cluster \
                      --name round2-eks \
                      --region us-east-1 \
                      --query cluster.certificateAuthority.data \
                      --output text | base64 --decode > /tmp/eks-ca.crt

                    TOKEN=$(aws eks get-token \
                      --cluster-name round2-eks \
                      --region us-east-1 \
                      --query status.token \
                      --output text)

                    ENDPOINT=$(aws eks describe-cluster \
                      --name round2-eks \
                      --region us-east-1 \
                      --query cluster.endpoint \
                      --output text)

                    helm upgrade --install production ./helm/blog-chart \
                      --values ./helm/production-values.yaml \
                      --namespace production \
                      --kube-token "$TOKEN" \
                      --kube-apiserver "$ENDPOINT" \
                      --kube-ca-file /tmp/eks-ca.crt
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline succeeded - blog platform deployed to EKS staging and production"
        }
        failure {
            echo "Pipeline failed - check logs above"
        }
    }
}
