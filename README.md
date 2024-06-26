# Setup AWS Cognito for depX
This repository will help depx users with their first time setup of AWS Cognito.
WARNING: This software is beta. Donot run this code in a production environment. 

Checkout our latest documentation to get started: https://depxdocs.notion.site/Documentation-for-depX-2b4ae6f3ceda48c08926e6acd07d63b7?pvs=4

### Pre-requisites

1. AWS account
2. IAM User with admin access
3. Permanent Security credentials

You can create an IAM user and generate permanent security credentials by checking out the following links:-

1. https://docs.aws.amazon.com/IAM/latest/UserGuide/security-creds.html
2. https://k21academy.com/amazon-web-services/create-access-and-secret-keys-in-aws/
3. https://youtu.be/HuE-QhrmE1c?si=59YCh7dZb-HhjtsQ

## Run
You can download the binary from the releases section or install it using the instructions in the next section

## Installation

### Linux x64
1. Download the repo
  ```
  git clone https://github.com/depXOfficial/depXCognitoSetupCmd.git
  ```
2. Make the installer script executable
  ```
  cd depXCognitoSetupCmd/
  chmod +x linux_x64_install.sh
  ./linux_x64_install.sh
  ```
3. Run the executable
```
./dist/DepXCognitoSetup/DepXCognitoSetup
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
  .\dist\DepXCognitoSetup\DepXCognitoSetup
  ```
