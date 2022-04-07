from constructs import Construct
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    aws_ec2 as ec2
)


class S3(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "myFirstBucket", bucket_name="cdkbucketz345", 
                           encryption=s3.BucketEncryption.KMS,
                           bucket_key_enabled=True
                        )
        permission = bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=['s3:GetObject'],
            resources=[bucket.arn_for_objects('*')],
            principals=[iam.AccountRootPrincipal()]
            )
        )

class EC2Stack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        

        count = 0
        
        vpc = ec2.Vpc(self, "vpc-cf",
            cidr="10.0.0.0/16",
            # dns hostnames and support enabled by default
            max_azs=2,
            subnet_configuration=[ec2.SubnetConfiguration(
                name='Public Subnet',
                subnet_type=ec2.SubnetType.PUBLIC,
                cidr_mask=24
            ),
            ec2.SubnetConfiguration(
                name='Private Subnet',
                subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                cidr_mask=24
            )             
            ],
            nat_gateways=2
        )
        
       
        role = iam.Role(self, "SSM_Agent_CDK", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        
        while count < 2:
            public_instance = ec2.Instance(self, f"Public_EC2 {count}", 
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO), machine_image=ec2.MachineImage.latest_amazon_linux(),
                key_name="virginia_key", 
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
                role = role
                )            
            private_instance = ec2.Instance(self, f"Private_EC2 {count}", 
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO), machine_image=ec2.MachineImage.latest_amazon_linux(),
                key_name="virginia_key", 
                vpc=vpc,
                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
                role = role            
            )
            count += 1

        
