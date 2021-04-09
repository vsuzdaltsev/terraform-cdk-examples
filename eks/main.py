#!/usr/bin/env python

# CDK
from constructs import Construct
from cdktf import App, TerraformOutput, TerraformStack, Token

# terraform provider
from imports.aws import AwsProvider, DataAwsCallerIdentity

# terraform module
from imports.vpc import Vpc
from imports.eks import Eks


AWS_REGION = 'us-west-2'
TAGS = {"Environment": "test", "Delete me": "true"}


class BasicStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, 'Aws', region=AWS_REGION)

        eks_vpc = Vpc(
            self, 'TestEksClusterVpc',
            name='my-vpc',
            cidr='10.0.0.0/16',
            azs=[
                f"{AWS_REGION}a",
                f"{AWS_REGION}b",
                f"{AWS_REGION}a"],
            private_subnets=[
                '10.0.1.0/24',
                '10.0.2.0/24',
                '10.0.3.0/24'],
            public_subnets=[
                '10.0.101.0/24',
                '10.0.102.0/24',
                '10.0.103.0/24'],
            enable_nat_gateway=True,
            tags=TAGS
        )

        my_eks = Eks(
            self, 'TestEks',
            cluster_name='my-eks',
            subnets=Token().as_list(eks_vpc.private_subnets_output),
            vpc_id=Token().as_string(eks_vpc.vpc_id_output),
            manage_aws_auth=False,
            cluster_version='1.17',
            node_groups=[
                {
                    "instance_types": ["m5.large"],
                    "capacity_type":"SPOT"
                }
            ],
            tags=TAGS
        )

        TerraformOutput(
            self, 'cluster_endpoint',
            value=my_eks.cluster_endpoint_output
        )

        TerraformOutput(
            self, 'create_user_arn',
            value=DataAwsCallerIdentity(self, 'current').arn
        )


app = App()
BasicStack(scope=app, ns="test-eks-stack")
app.synth()
