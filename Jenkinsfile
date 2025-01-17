pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/ji-ki/web-service-docker'
            }
        }

        stage('Build Docker Images') {
            agent { label 'build-agent' } // Используем build-agent для сборки
            steps {
                script {
                    sh 'docker-compose build'
                    sh 'docker save note-app:latest -o note-app.tar' // Сохранить образ в файл
                }
            }
        }

        stage('Deploy Application') {
            agent { label 'deploy-agent' } // Используем deploy-agent для деплоя
            steps {
                script {
                    sh 'docker load -i note-app.tar' // Загрузить образ
                    sh 'docker-compose up -d'       // Запустить приложение
                }
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }
    }
}
