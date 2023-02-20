# EC2-Mongo Database
*Last Dump 02-03-2023*

Our Mongo Database Dump is now on an AWS EC2 instance dedicated for querying and exploring the data away from our production system.

# Table of Contents
* [Connect To EC2 Instance](#Connect-To-EC2)
* [Loading Mongo Data](#Loading-Mongo-Data)


# Connect-To-EC2

To access our EC2 Compute Service you will need to complete the following steps.

1. Create your key-pair pem file for ssh access to the EC2 instance
    ```
    nano ~/.ssh/Mongo-EC2.pem
    ```
2. Go to 1Password and copy the contents from `Mongo-EC2.txt` into the .pem file in your terminal

3. Change permissions on your `.pem` file for secure key practice and access to EC2 instance via `ssh`
    ```
    chmod 400 ~/.ssh/Mongo-EC2.pem 
    ```

4. Navigate to the `AWS Management Console > EC2 > Instances `

5. Select instance **mirrulations-MongoDB** and copy the Public IPV4 IP-Address

    - Make sure the Instance is running before getting the IPV4 address



6. Connect via ssh/key-pair indentity to EC2 instance

    ```
    ssh -i ~/.ssh/Mongo-EC2.pem ec2-user@<Public-IP-Address-For-EC2>
    ```

7.  Once connected, you should be able to access Mongo in the EC2 by entering the `mongo` command

8. When your Queries are completed make sure to stop the instance,  **DO NOT TERMINATE**
    - Currently working on creating an image of the Instance so we can replicate this instance easily.


# Loading-Mongo-Data

To Load new mongo dumps onto this EC2 instance you will need to first be connected to the EC2 instance
    - See [Connect To EC2 Instance](#Connect-To-EC2)

1. Assuming the dump is already in an s3 bucket we will use the aws cli to download the mongo data.bson to the instance.

2. You will need to enter your aws credentials in order to use the aws cli

```
nano ~/.aws/credentials
```
Fill in the corresponding fields:
```
[default]
aws_access_key_id=<ACCESS_KEY_ID>
aws_secret_access_key=<SECRET_ACCESS_KEY>
```

- If you don't have a key created see an AWS admin for setting up the proper permissions for key creation


3. Next, get the `mongo-dump.bson` **s3 uri link** for whichever db you wish to have on the EC2 instance  
    - This file will have the form of 
    ```
    s3://mirrulations-mongodump-2023-02-03/mirrulations/comments_2023_02_03.bson
    ```

4. Then we will copy that file from the s3 bucket to our EC2 instance 

```
    aws s3 cp s3://mirrulations-mongodump-2023-02-03/mirrulations/comments_2023_02_03.bson .
```
- This command copies the data to our current working directory

5. Then with mongo downloaded we can issue the command
```
mongorestore --uri="mongodb://localhost:27017" --db=mirrulations comments_2023_02_03.bson
```

This may take a while but after that the new database will be in mongo and ready to query.
