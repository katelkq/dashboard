# Documentation
From within the parent directory, navigate to `./docs/build/html/`, and double click `index.html`. This should be able to open the documentation in your browser.

# Getting Started
## Installing dependencies
Run the following command within the main folder:

```
$ pip install -r ./requirements.txt
```

## Updating the pickles
Run the following command within the main folder:

```
$ python ./Dashboard/params_update.py
```

This will refresh all the pickles under `./Dashboard/lib/` using data freshly fetched from Refinitiv. I don't think this needs to be done very often, though.

## Serving the dashboard on a local machine
Run the following command within the main folder:

```
$ bokeh serve --show Dashboard
```
