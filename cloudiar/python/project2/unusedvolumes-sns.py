import boto3

def lambda_handler(event, context):

    print(event)

    ec2 = boto3.client('ec2')
    sns = boto3.client('sns')
    sns_arn = event.get('detail').get('requestParameters').get('topicArn')

    print(sns_arn)


    unused = []
    volumes = ec2.describe_volumes()

    for v in volumes['Volumes']:
        if len(v['Attachments']) == 0:
            unused.append(v['VolumeId'])
            print(v)
            print("--------------------")
    
    email = "Unused EBS Volume: "

    for u in unused:
        email = email + "VolumeId = {} \n".format(u)
    
    sns.publish(
        TopicArn = sns_arn ,
        Subject = "****Unused EBS Volume Detected****",
        Message = email
        )