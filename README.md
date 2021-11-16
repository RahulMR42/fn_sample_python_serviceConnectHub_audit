# fn_sample_python_serviceConnectHub_audit
a sample function code with Oracle Cloud function and service connector hub
------------------------

- Objective 

  - The code build here to explain the usage of oracle function with a service connector hub (ie an image upload letting a Oracle cloud deployment pipeline (over OKE) to invoke automatically).
  - Here the flow uses a service connector hub based on audit logs ,that will invoke while uploading an image to oracle cloud registry.
  - Reference - https://docs.oracle.com/en-us/iaas/Content/service-connector-hub/home.htm 
  
 


- Edit the auth values.

```
$ Update invoke.py with necessary values or parse it as a variable via fn config or docker image config.

 config = {
                "user": 'ocid1.user.oc1..<userid>,
                "key_file": "user.pem",
                "fingerprint": 'fingerprint',
                "tenancy": 'ocid1.tenancy.oc1..<tenacity id>',
                "region": 'region'
                }

```
- Reference - https://docs.oracle.com/en-us/iaas/Content/Functions/Concepts/functionshowitworks.htm 
- Create a OKE deployment with Oracle cloud pipeline. - https://docs.oracle.com/en-us/iaas/Content/devops/using/deploy_oke.htm
- Create the application - https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionscreatingapps.htm


- Deploy the  functions 

```
 $ git clone https://github.com/RahulMR42/fn_sample_function_with_python
 $ cd fn_sample_function_with_python
 $ fn deploy -v --app <app name>
```
- Invoke the function (Manually)
- Here we have to provide a sample payload (a format like a docker repo image upload event) 
- Here we are using a precreated docker image (reference - https://github.com/RahulMR42/python_fastapi_app/blob/main/Dockerfile ) which is the target application's image.

```
- cat sample.json|DEBUG=1 fn invoke <app name> mr-devops-deploy-pipeline
```

Once the deployment completed / based on the application docker image and ingress URL (of OKE) we can see the new version as deployed.

