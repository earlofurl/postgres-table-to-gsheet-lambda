<!-- @format -->

This is a simple AWS Lambda function to copy the entire contents of a PostgreSQL database table to a specified worksheet in Google Drive.

Simply add the environment variables to the Lambda config, upload main.py as the deployment package, and run whenever you need to copy the database table to a sheet.

See the Lambda docs page on creating deployment packages to see your options for deploying the code.
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

You may find that the dependencies exceed the 250mb unzipped limit for lambda.

Luckily, AWS now has EFS, which can be pretty handy for creating a shared filesystem for python dependencies.

See this AWS blog post for a detailed guide on how it works:
https://aws.amazon.com/blogs/aws/new-a-shared-file-system-for-your-lambda-functions/
