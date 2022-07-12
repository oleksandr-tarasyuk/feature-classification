# CE Repository Template Test

Template with our basic structure

## Description

The repository should follow the next structure:
```
|_ package_name/
|    |_ model/
          |_ your_model_script.py
     |_ other_code
|_ docs/
|_ fluid/
|_ tests/
|_ Dockerfile
|_ gpu.Dockerfile
|_ Pipfile
|_ Pipefile.lock
|_ setup.py
|_ setup.cfg
```

### AI Model
In case of implementing an AI model using the framework, be sure to follow the same structure in both the repository 
and the `apiCall` so the model is loaded correctly.

As an example:
`package-name.model.your_model_script.py`

## Installation

The repository works using pipenv to separate development from production packages.
To install then:
```
pipenv install

or

pipenv install --dev
```
Pipenv will create an environment, uses `pip shell` to activate it.


To install individual packages use: `pipenv install xxx` so it will be directly
added to the Pipfile.

## Test
To run test use: `pytest -vv tests`

## Deploy

Run the following command to deploy to the desired environment `{env}` 
*(which can be ces, integration, staging or production)*

```bash
fluid-deploy -c fluid/config.json -c fluid/config.{env}.json
```

If still in development and testing, use `-d` so it doesn't require committing changes. 
The docker image will be tagged with: `dev-yourGithubUser`.

## Package wheel

To create a python package, execute the following commands:
``` bash
python setup.py ${version} sdist bdist_wheel
twine upload --repository-url http://209.133.199.50:8090 dist/* --verbose -u "$USER" -p "$PASS"
```
