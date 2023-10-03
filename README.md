# K8S-Pydantic
Generate Kubernetes configuration files using Python's Pydantic library. Use Pydantic models and PyYAML to generate template files for Helm Charts installation.

## Prepare templates for Helm
- [__Optional__] Define schema(s) for K8S resource in `schemas` directory.
- [__Optional__] Define function(s) to generate template (yaml file in `templates` directory) for the schema(s).
- [__Optional__] Include the function(s) in `generate_templates.py` file.
- Define values for the template in `values` directory.
- Define environment variables for your applications in the format: `.env.<app-name>`.  
  These variables' names should be referenced in the [applications.yaml](values/applications.yaml) file (env or secret).
- Generate the templates: 
    ```bash
    $ python generate_templates.py
    ```
NOTES: If Ingress host is not defined, default external IP of the Cluster will be the host.

## Apply the Helm charts:
- Install/Upgrade the Helm chart:
  ```bash
  $ helm upgrade --install fss-staging .
  ```

## Others
### Install Kong Plugins using Helm
For more details: https://docs.konghq.com/kubernetes-ingress-controller/latest/guides/setting-up-custom-plugins/
1. Create a ConfigMap or Secret based on the plugin code:
   ```bash
   # using ConfigMap
    $ kubectl create configmap <kong-plugin-config-name> --from-file=<plugin-name> -n kong

    # OR using Secret
    $ kubectl create secret generic -n kong <kong-plugin-config-name> --from-file=<plugin-name>
   ```
2. Update Kong’s Deployment to load custom plugin:
    ```yaml
    # kong-plugin.yaml
    plugins:
    configMaps:                # change this to 'secrets' if you created a secret
    - name: <kong-plugin-config-name>
        pluginName: <plugin-name>
    ```
3. Deploy the Kong Ingress Controller:
    ```bash
    $ helm repo add kong https://charts.konghq.com
    $ helm repo update
    $ helm install kong/kong --generate-name --set ingressController.installCRDs=false --values kong-plugin.yaml
    ```