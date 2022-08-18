"""IaaC to host a static website on AWS s3 with CDN"""
import os
import mimetypes
import json
from uuid import uuid4
from pulumi import FileAsset, export
from pulumi_aws import s3, cloudfront

# Create an s3 bucket for static file hosting
bucket = s3.Bucket('website-bucket', bucket="static-hosting-bucket-satabratapaul",
                   website=s3.BucketWebsiteArgs(index_document='index.html'))

static_dir = 'static'

for file in os.listdir(static_dir):
    file_path = os.path.join(static_dir, file)
    mime_type, _ = mimetypes.guess_type(file_path)
    obj = s3.BucketObject(file, bucket=bucket.id, source=FileAsset(
        file_path), content_type=mime_type)


def public_read_bucket_policy(bucket_name):
    return json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:GetObject"
            ],
            "Resource": [
                f"arn:aws:s3:::{bucket_name}/*",
            ]
        }]
    })


bucket_name = bucket.id
bucket_policy = s3.BucketPolicy("static-hosting-bucket-policy",
                                bucket=bucket_name, policy=bucket_name.apply(public_read_bucket_policy))
originid = 'static-hosting-s3-{}'.format(uuid4())

cdn = cloudfront.Distribution('static-hosting-s3Distribution', origins=[
    cloudfront.DistributionOriginArgs(
        domain_name=bucket.bucket_regional_domain_name, origin_id=originid)], enabled=True, default_cache_behavior=cloudfront.DistributionDefaultCacheBehaviorArgs(
    allowed_methods=["HEAD", "GET", "OPTIONS"], cached_methods=["GET", "HEAD"], target_origin_id=originid, viewer_protocol_policy='https-only', min_ttl=0, default_ttl=3600, max_ttl=86400, forwarded_values=cloudfront.DistributionOrderedCacheBehaviorForwardedValuesArgs(
                query_string=False,
                cookies=cloudfront.DistributionOrderedCacheBehaviorForwardedValuesCookiesArgs(
                    forward="none",
                ),
            )), default_root_object='index.html',
    restrictions=cloudfront.DistributionRestrictionsArgs(geo_restriction=cloudfront.DistributionRestrictionsGeoRestrictionArgs(restriction_type="whitelist", locations=['US', 'CA', 'IN'])), viewer_certificate=cloudfront.DistributionViewerCertificateArgs(
    cloudfront_default_certificate=True))


export('bucket_name', bucket_name)
export('cdn', cdn.domain_name)
