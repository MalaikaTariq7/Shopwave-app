pipeline {
    agent any
    stages {
        stage('Clone') {
            steps {
                git url: 'https://github.com/MalaikaTariq7/Shopwave-app.git', branch: 'main'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t shopwave-test .'
            }
        }
        stage('Test') {
            steps {
                sh '''
                    mkdir -p test-results
                    docker run --rm \
                        --shm-size=2g \
                        -v $(pwd)/test-results:/app/test-results \
                        shopwave-test \
                        bash -c "
                            python app.py &
                            sleep 3
                            pytest test_shopwave.py \
                                --html=test-results/report.html \
                                --self-contained-html \
                                -v
                        "
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                    docker stop shopwave-app || true
                    docker rm shopwave-app || true
                    docker run -d \
                        --name shopwave-app \
                        -p 5000:5000 \
                        shopwave-test \
                        flask run --host=0.0.0.0 --port=5000
                '''
            }
        }
    }
    post {
        always {
            emailext(
                to: 'malaikatariq2400@gmail.com',
                subject: "ShopWave Test Results: ${currentBuild.currentResult} - Build #${env.BUILD_NUMBER}",
                body: """
                    <h2>Test Results: ${currentBuild.currentResult}</h2>
                    <p><b>Job:</b> ${env.JOB_NAME}</p>
                    <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
                    <p><b>App URL:</b> <a href="http://16.16.233.7:5000">http://16.16.233.7:5000</a></p>
                    <p><b>Console:</b> <a href="${env.BUILD_URL}console">View Console Output</a></p>
                """,
                mimeType: 'text/html',
                recipientProviders: [
                    [$class: 'DevelopersRecipientProvider'],
                    [$class: 'RequesterRecipientProvider']
                ],
                attachLog: true
            )
        }
    }
}
