
# Getting started with Python dev

Go to the container dir and then run the install sequence

    make venv
    source venv/bin/activate

Once installed run with the following:

    k8s-python start --config tests/test_data/config.yaml

Optionally run with debug shell

    k8s-python --debug start tests/test_data/config.yaml

Testing is provided by pytest. Typicallly invoked by `pytest` but also available via `ptw` to provide watching for automatic retest of file change.

    pytest
    ptw

# Parse your configs

    k8s-python --debug parse --config tests/test_data/config.yaml --secrets tests/test_data/secrets

# Add some test data

    k8s-python --debug embed --config tests/test_data/config.yaml --secrets tests/test_data/secrets tests/test_data/sampletext/*

# Query some data

    k8s-python --debug query --config tests/test_data/config.yaml --secrets tests/test_data/secrets "Where is the best road to drive on"

# Add some chunks to the chunk parser

There is an example chunk parser in the system that will parse some data and keep a count of how much is left to process.

    curl -X POST http://k8s-python/pie/v0/chunks -H "Content-Type: application/json" -d '{"name": "example", "num_chunks": 25}'

# Development Mode

When developing you can take advantage of adev to manage restarts, etc
This maps to a hardcoded config in the tests/test_data/config.yaml file
This can be run using the make wrapper:

    make adev

# Issues

Capture issues here to look at:

* [x] CLI parsing
* [x] config loading via yaml
* [x] secret loading [https://github.com/pydantic/pydantic/discussions/2928#discussioncomment-4744841]
* [x] async http
* [x] liveness
* [x] prestart and shutdown actions
* [x] Signals support for shutdown https://docs.aiohttp.org/en/stable/web_advanced.html#signals
  * [x] After shutdown is triggered ready should reply negative (automatic based on shutdown hook)
  * [z] System should pause a certain amount of time before final shutdown to ensure traffic is rebalanced off the pod (ie 2xliveness time)
* [x] Metrics (Prometheus)
