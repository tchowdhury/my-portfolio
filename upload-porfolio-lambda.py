import boto3
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):

    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:294911564117:codeDeployTopic')

    try:
        s3 = boto3.resource('s3')

        portfolio_bucket = s3.Bucket('portfolio.gogo-gadget.com.au')
        build_bucket = s3.Bucket('portfoliobuild.gogo-gadget.com.au')

        portfolio_zip = StringIO.StringIO()
        build_bucket.download_fileobj('Portfoliobuild.zip',portfolio_zip)


        with zipfile.ZipFile(portfolio_zip) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj,nm,
                ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')


        print 'Job dobe!'
        topic.publish(Subject="Code Deployed",Message="Code Deployed Successfully")
    except:
        print 'Job failed!'
        topic.publish(Subject="Code Deploy Failed",Message="Code Deploy Failed")

    # TODO implement
    return 'Hello from Lambda'
