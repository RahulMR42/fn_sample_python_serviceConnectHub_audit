import io
import json
import logging
import os
import oci
from datetime import datetime
from fdk import response


class deploy:
    def __init__(self,image_url):
        self.image_url = image_url


    def deploy_version(self):
        try:
            
            logging.getLogger().info("Inside deploy handler")
         
            config = {
                "user": 'ocid1.user.oc1..<user id>',
                "key_file": "user.pem",
                "fingerprint": '<user fingerprint>',
                "tenancy": 'ocid1.tenancy.oc1..<tenacity id>',
                "region": '<region>'
                }
            deployment_timestamp = datetime.today().isoformat()
            # Initialize service client with default config file
            logging.getLogger().info("Attempting to initialize the devops client")
            devops_client = oci.devops.DevopsClient(config)
            logging.getLogger().info('Initialized devops client')
            # Send the request to service, some parameters are not required, see API
            # doc for more info
            logging.getLogger().info('Attempting deployment')
            create_deployment_response = devops_client.create_deployment(
                create_deployment_details=oci.devops.models.CreateDeployPipelineDeploymentDetails(
                    deployment_type="PIPELINE_DEPLOYMENT",
                    deploy_pipeline_id="ocid1.devopsdeploypipeline.oc1.iad.amaaaaaak56z2vqadrpumpjwlngyngxjojm5na25h4fxr6jrejvtmofy3i4a",
                    display_name=f"deployment_{deployment_timestamp}",
                    deployment_arguments=oci.devops.models.DeploymentArgumentCollection(
                        items=[
                            oci.devops.models.DeploymentArgument(
                                name="image_url",
                                value=self.image_url)]))
                                )
            # Get the data from response
            logging.getLogger().info('Response ' + str(create_deployment_response.data))
            return create_deployment_response
        except Exception as error:
            logging.getLogger().error('Exception' + str (error))


def handler(ctx, data: io.BytesIO = None):
    image_url = "us-ashburn-1.ocir.io/fahdabidiroottenancy/rahul/mr-devops/fastapp:0.0.4"
    logging.getLogger().info("Function invokation begins")
    try:
        input = json.loads(data.getvalue())
        logging.getLogger().info("Function inputs are  " + str(input))
        body = input[0]
        oci_region = 'us-ashburn-1.ocir.io' 
        image_repo = body['data']['additionalDetails']['path']
        image_digest = body['data']['additionalDetails']['digest']
        image_url = f'{oci_region}/{image_repo}@sha256:{image_digest}' 
        logging.getLogger().info("Using the image url" + str(image_url))
        sdk_handler = deploy(image_url)
        sdk_handler.deploy_version()
    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))
    logging.getLogger().info("Inside sdk handler message block")
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": f"Deployment attempted  with URL {image_url}"}),
        headers={"Content-Type": "application/json"}
    )

