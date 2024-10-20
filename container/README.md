
# Getting started with Python dev

Go to the container dir and then run the install sequence

    make venv
    source venv/bin/activate

Once installed run with the following:

    k8s-python start tests/test_data/config.yaml

Optionally run with debug shell

    k8s-python --debug start tests/test_data/config.yaml

# Development Mode

When developing you can take advantage of adev to manage restarts, etc
This maps to a hardcoded config in the tests/test_data/config.yaml file
This can be run using the make wrapper:

    make adev

# Issues

Capture issues here to look at:

* [x] CLI parsing
* [x] config loading via yaml
* [ ] secret loading [https://github.com/pydantic/pydantic/discussions/2928#discussioncomment-4744841]
* [x] async http
* [ ] liveness
