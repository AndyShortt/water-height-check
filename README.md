## Creek Water Height Check and Notification
This basic service...

Things it does: 
1. ...
2. ...
3. ...


## License Summary


## Deployment
This application uses AWS SAM for build and deployment, making it much faster to create the infrastructure plumbing that we don't care about for the purpose of this app. For information on AWS SAM, visit the [GitHub page](https://github.com/awslabs/serverless-application-model).

0. You will need the SAM CLI & AWS CLI installed and configured. Then you will need to clone this repo.

1. Navigate to the root of the repo folder. We are going to build the SAM package, which means it will review our template and populate additional fields, pull in dependencies located in our requirements file, and pull together our source code. All this is uploaded to S3.

$ sam build

The first time you execute the build, it will ask you a few questions to create a .toml configuration file. Going forward it will pickup defaults from this file. You can name the stack anything you want and I recommend you use your normal default aws region.

3. We are ready to deploy the package using CloudFormation (via SAM). Execute the following command.
 
$ sam deploy 

It will first do a change analysis to confirm you intended to change the resources. After you confirm, it will deploy the resources via CloudFormation.

## Execution



## TODO

