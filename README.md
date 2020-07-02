## Creek Water Height Check and Notification
Checks a USGS gage on McAlpine Creek in Charlotte NC. When water height breaches set thresholds it notifies that our backyards are flooding, it has reached standard flood stage, and finally if it reaches record highs. Notifications are sent via SNS (subscribe to topic outside script).

If you don't care about the water height at this location, then lookup the site and paramter code for the location near you.  Update the URL query string paramters located at the top of the lambda function.

Things it does: 
1. Cloudwatch sends event trigger to Lambda every 10 minutes
2. Lambda checks water gage height from USGS
3. Lambda sends SNS msg if water height meets thresholds in Dynamo table

## Deployment
This application uses AWS SAM for build and deployment, making it much faster to create the infrastructure plumbing that we don't care about for the purpose of this app. For information on AWS SAM, visit the [GitHub page](https://github.com/awslabs/serverless-application-model).

0. You will need the SAM CLI & AWS CLI installed and configured. Then you will need to clone this repo.

1. Navigate to the root of the repo folder. We are going to build the SAM package, which means it will review our template and populate additional fields, pull in dependencies located in our requirements file, and pull together our source code. All this is uploaded to S3.

$ sam build

The first time you execute the build, it will ask you a few questions to create a .toml configuration file. Going forward it will pickup config from this file.

3. We are ready to deploy the package using CloudFormation (via SAM). Execute the following command.
 
$ sam deploy 

It will first do a change analysis to confirm you intended to change the resources. After you confirm, it will deploy the resources via CloudFormation.

4. Locate the new SNS topic and subscribe with your email address.

## Execution
If the deployment is successful and you add your SNS subscription, the lambda function runs every 10 minutes... forever.

