pipeline {
    agent any
    environment {
        // CI set to true to allow it to run in "non-watch" (i.e. non-interactive) mode
        CI = 'true'
    }
    stages {
        stage('Build') { 
            steps {
                script {
                    try {
                        // clean all unused images
                        sh 'yes | docker image prune -a'
                    }
                    catch (Exception e) {
                        echo "no unused images deleted"
                    }
                    try {
                        // clean all unused containers
                        sh 'yes | docker container prune'
                    }
                    catch (Exception e) {
                        echo "no unused containers deleted"
                    }
                }
                // ensure latest image is being build
                sh 'docker build -t yanxun-image:latest .'
            }
        }
    
        stage('Test') {
            parallel {
                stage('Integration UI Testing') {
                    agent {
                        docker {
                            image 'yanxun-image:latest'
                        }
                    }
                    steps {
                        sh 'nohup python3 app.py & pytest -s -rA --junitxml=logs/report.xml'
                        sh 'pkill -f app.py'
                    }
                    post {
                        always {
                            junit testResults: 'logs/report.xml'
                        }
                    }
                }

                stage('Code Quality Check via SonarQube') { 
                    steps { 
                        script { 
                            def scannerHome = tool 'SonarQube'; 
                            withSonarQubeEnv('SonarQube') { 
                                sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=OWASP -Dsonar.sources=." 
                            } 
                        } 
                    }
                }
            }
        }
    }
    post { 
        always { 
            recordIssues enabledForFailure: true, tool: sonarQube() 
        } 
    }
}
