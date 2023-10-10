# Setup-AWS-Cognito-depX
This repo will first time setup AWS Cognito for depX users. This software is still in alpha. Make sure you have an active AWS account and have generated security credentials for your IAM user. If not, you can checkout the following links:-

1. https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html
2. https://k21academy.com/amazon-web-services/create-access-and-secret-keys-in-aws/
3. https://youtu.be/HuE-QhrmE1c?si=59YCh7dZb-HhjtsQ

Installation steps are mentioned below

## Linux x64
1. Download the repo
  ```
  git clone https://github.com/depXOfficial/Setup-AWS-Cognito-depX.git
  ```
2. Make the installer script executable
  ```
  chmod +x linux_x64_install.sh
  ./linux_x64_install.sh
  ```
3. Run the executable
```
./dist/DepXCogntioSetup
```
![image](https://github.com/depXOfficial/Setup-AWS-Cognito-depX/assets/47640633/eb92e966-d363-499c-a21d-9b08e4faa15c)


## Windows

NOTE: You'll need python >= 3.10 installed in order to run this script. You can visit https://www.python.org/downloads/

Open up command prompt. Navigate to the directory of this repo and run the following commands.

1. Run the windows installer script
  ```
  .\windows_x64_install.bat
  ```
2. Run the executable
  ```
  .\dist\DepXCogntioSetup
  ```
