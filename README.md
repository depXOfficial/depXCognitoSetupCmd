# Setup-AWS-Cognito-depX
This repo will help depx users with their first time setup of AWS Cognito. This software is still in alpha. 

### Pre-requisites

1. AWS account
2. IAM User with admin access
3. Permanent Security credentials

You can create an IAM user and generate permanent security credentials by checking out the following links:-

1. https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html
2. https://k21academy.com/amazon-web-services/create-access-and-secret-keys-in-aws/
3. https://youtu.be/HuE-QhrmE1c?si=59YCh7dZb-HhjtsQ

## Run
You can download the binary from the releases or install it using the instructions in the next section

## Installation

### Linux x64
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


### Windows

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
