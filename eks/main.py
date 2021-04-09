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
AVAILABILITY_ZONES = [
    f"{AWS_REGION}a",
    f"{AWS_REGION}b",
    f"{AWS_REGION}a"]
TAGS = {"Environment": "test", "Delete me": "true"}
VPC_CIDR = '10.0.0.0/16'
PRIVATE_SUBNETS = [
    '10.0.1.0/24',
    '10.0.2.0/24',
    '10.0.3.0/24']
PUBLIC_SUBNETS = [
    '10.0.101.0/24',
    '10.0.102.0/24',
    '10.0.103.0/24']
CLUSTER_VERSION = '1.17'
NODE_GROUP_INSTANCE_TYPE = "m5.large"


class BasicStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, 'Aws', region=AWS_REGION)

        eks_vpc = Vpc(
            self, 'TestEksClusterVpc',
            name='test-eks-cluster-vpc',
            cidr=VPC_CIDR,
            azs=AVAILABILITY_ZONES,
            private_subnets=PRIVATE_SUBNETS,
            public_subnets=PUBLIC_SUBNETS,
            enable_nat_gateway=True,
            tags=TAGS
        )

        eks_cluster = Eks(
            self, 'TestEksCluster',
            cluster_name='test-eks-cluster',
            subnets=Token().as_list(eks_vpc.private_subnets_output),
            vpc_id=Token().as_string(eks_vpc.vpc_id_output),
            manage_aws_auth=False,
            cluster_version=CLUSTER_VERSION,
            node_groups=[
                {
                    "instance_types": [NODE_GROUP_INSTANCE_TYPE],
                    "capacity_type":"SPOT"
                }
            ],
            tags=TAGS
        )

        TerraformOutput(
            self, 'cluster_endpoint',
            value=eks_cluster.cluster_endpoint_output
        )

        TerraformOutput(
            self, 'create_user_arn',
            value=DataAwsCallerIdentity(self, 'current').arn
        )


app = App()
BasicStack(scope=app, ns="test-eks-stack")
app.synth()
