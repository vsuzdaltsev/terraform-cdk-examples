from invoke import Collection, task


@task
def prepare(context):
    """>> Prepare the repo."""

    context.run("cdktf get")


@task
def deploy(context):
    """>> Deploy stack."""
    context.run("cdktf deploy --auto-approve --disable-logging")


@task
def destroy(context):
    """>> Deploy stack."""
    context.run("cdktf destroy --auto-approve --disable-logging")


@task
def autopep8(context):
    """
    >> Run autocorrection on python files
    """
    print(">> Autocorrect python files according to styleguide")
    context.run("autopep8 --in-place --max-line-length 200 --aggressive *.py --verbose")


ns = Collection()
local = Collection('local')
cdk = Collection('cdk')

local.add_task(prepare, 'prepare_repo')
local.add_task(autopep8, 'autopep8')

cdk.add_task(deploy, 'deploy')
cdk.add_task(destroy, 'destroy')

ns.add_collection(cdk)
ns.add_collection(local)
