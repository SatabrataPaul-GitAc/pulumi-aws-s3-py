[![Deploy](https://get.pulumi.com/new/button.svg)](https://app.pulumi.com/new?template=https://github.com/pulumi/examples/blob/master/aws-py-s3-folder/README.md)

# Host a Static Website on AWS s3 with appropriate bucket policies and reduced latency configuration using AWS CloudFront CDN (Content Delivery Network)

## Deploying and running the program

Note: some values in this example will be different from run to run.  These values are indicated
with `***`.

1. Create a new stack:

    ```bash
    $ pulumi stack init dev
    ```

2. Set Config parameters in Pulumi:
    a) Set the AWS Region to be used for deploying the cloud resources 
    ```bash
    $ pulumi config set aws:region us-west-2
    ```
    b) Set the accesskey for the AWS account to be used
    ```bash
    $ pulumi config set aws:accessKey <access_key>
    ```
    c) Set the secretkey for the AWS account to be used
    ```bash
    $ pulumi config set --secure aws:secretKey <secret_key>
    ```
    
3. Run `pulumi up` to preview and deploy changes.  After the preview is shown you will be
    prompted if you want to continue or not.

    ```bash
    $ pulumi up
    Previewing update (dev):

        Type                              Name                                Plan       
    +   pulumi:pulumi:Stack               pulumi-aws-s3-py-dev                create     
    +   ├─ aws:s3:Bucket                  website-bucket                      create     
    +   ├─ aws:s3:BucketObject            index.html                          create     
    +   ├─ aws:s3:BucketObject            python.png                          create     
    +   ├─ aws:s3:BucketObject            favicon.png                         create     
    +   └─ aws:s3:BucketPolicy            static-hosting-bucket-policy        create
    +   └─ aws:cloudfront:Distribution    static-hosting-s3Distribution       create

    Resources:
        + 6 to create

    Do you want to perform this update?
    > yes
      no
      details
    ```

4. To see the resources that were created, run `pulumi stack output`:

    ```bash
    $ pulumi stack output
    Current stack outputs (2):
        OUTPUT                                           VALUE
        bucket_name                                      static-hosting-bucket-****
        cdn                                              ****.cloudfront.net
    ```

5. To see that the S3 objects exist, you can either use the AWS Console or the AWS CLI:

    ```bash
    $ aws s3 ls `pulumi stack output bucket_name`
    2022-08-17 15:40:47      13731 favicon.png
    2022-08-17 15:40:48        249 index.html
    ```

6. Open the CDN URL in a browser to see both the rendered HTML and Python splash image:

    ```bash
    $ pulumi stack output cdn
    ***.cloudfront.net
    ```

7. To clean up resources, run `pulumi destroy` and answer the confirmation question at the prompt.
