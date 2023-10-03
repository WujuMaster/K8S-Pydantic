from typing import List

import yaml

import schemas as k8s


def create_ingress(
    applications_conf: k8s.ApplicationConfList,
    shared_conf: k8s.SharedConf,
    ingress_conf: k8s.IngressConf,
    output_path: str,
):
    rules: List[k8s.IngressRule] = []
    for app in applications_conf.applications:
        for app_ingress in app.ingress:
            path = k8s.HttpPath(
                path=app_ingress.path,
                backend=k8s.HttpBackend(
                    service=k8s.HttpBackendService(
                        name=app.name,
                        port=k8s.HttpBackendServicePort(number=app.service.port),
                    )
                ),
            )
            found = [d for d in rules if d.host == app_ingress.host]
            if found:
                found[0].http.paths.append(path)
            else:
                rule = k8s.IngressRule(
                    host=app_ingress.host,
                    http=k8s.HttpRule(paths=[path]),
                )
                rules.append(rule)

    ingress = k8s.Ingress(
        metadata=k8s.IngressMetaData(
            name=ingress_conf.name,
            namespace=shared_conf.namespace,
            labels={"ingress": ingress_conf.name},
            annotations=ingress_conf.metadata.annotations,
        ),
        spec=k8s.IngressSpec(
            ingressClassName=ingress_conf.className,
            tls=k8s.IngressTLS(
                hosts=ingress_conf.tls.hosts,
                secretName=ingress_conf.tls.secretName,
            )
            if ingress_conf.tls
            else None,
            rules=rules,
        ),
    )
    with open(output_path, "w") as outfile:
        yaml.dump(
            ingress.model_dump(exclude_none=True), outfile, default_flow_style=False
        )
