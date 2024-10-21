# k8s-python

This project provides a sample for k8s with python executing a web api

# Getting started

Pull down the docker image to test it

    docker pull ghcr.io/polecatworks/k8s-python:main
    docker run -it ghcr.io/polecatworks/k8s-python:main

Now that you have confirmed a good working image lets prep the k8s env to run the image.
You must setup a secret to provide credentials to your repository where you wil pull the image from eg the secrets: `dockerconfigjson-ghcr` as referenced in the `k8s-python-values.yaml` file. Then use the following to run your chart on k8s


    helm upgrade -i k8s-python chart/k8s-python -f chart/k8s-python-values.yaml
