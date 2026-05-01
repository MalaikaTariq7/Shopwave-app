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
    }

    post {
        always {
            emailext(
                subject: "ShopWave Test Results: ${currentBuild.currentResult} - Build #${env.BUILD_NUMBER}",
                body: """
                    <h2>Test Results: ${currentBuild.currentResult}</h2>
                    <p><b>Job:</b> ${env.JOB_NAME}</p>
                    <p><b>Build:</b> #${env.BUILD_NUMBER}</p>
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
