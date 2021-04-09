# terraform-cdk-example

## Prerequisite

Install cdktf:

```
~$ npm install --global cdktf-cli
```

Verify the installation:

```
~$ cdktf

Commands:
  cdktf deploy [OPTIONS]   Deploy the given stack
  cdktf destroy [OPTIONS]  Destroy the given stack
  cdktf diff [OPTIONS]     Perform a diff (terraform plan) for the given stack
  cdktf get [OPTIONS]      Generate CDK Constructs for Terraform providers and modules.
  cdktf init [OPTIONS]     Create a new cdktf project from a template.
  cdktf login              Retrieves an API token to connect to Terraform Cloud.
  cdktf synth [OPTIONS]    Synthesizes Terraform code for the given app in a directory.
```

Install Pipenv

```
~$ brew install pipenv
```

Install Dependency Library

```
~$ pipenv install
```

## Get Started

Export AWS credentials.

Available tasks:

```
~$ inv -l
>>
  cdk.eks.deploy       >> Deploy EKS stack.
  cdk.eks.destroy      >> Destroy EKS stack.
  cdk.eks.diff         >> Show terrafrom diff for the EKS stack.
  local.autopep8       >> Run autocorrection on python files.
  local.prepare-repo   >> Prepare the repo for given project.
```

Prepare dependencies and deploy stack:

```
~$ inv local.prepare-repo
~$ inv cdk.deploy
```

Remove stack:

```
~$ inv cdktf.destroy
```
