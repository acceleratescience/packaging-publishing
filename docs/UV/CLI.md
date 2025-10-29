# Implement the CLI entry point
Notice that the CLI will still not work in the way that we want it to. In order for the CLI to work, we have to make some alterations.

!!! tip

    There are a few different libraries that will help you handle CLI. In this project, we use `click`, but `typer` and `argparse` are also a very popular.

## Additions to the code
At this point it is worth quickly going through the code for the `app.py` script.

``` python
import click
import pandas as pd
import numpy as np
from pathlib import Path
from cancer_prediction.cancer_model import CancerModel

@click.group()
def cli():
    """Cancer prediction model CLI tool."""
    pass

@cli.command()
@click.option(
    '--data-file',
    '-d',
    type=click.Path(exists=True),
    required=True,
    help='Path to the CSV file containing training data'
)
@click.option(
    '--output-model',
    '-o',
    type=click.Path(),
    default='cancer_model.pkl',
    help='Path to save the trained model (default: cancer_model.pkl)'
)

def train(data_file, output_model):
    """Train a cancer diagnosis prediction model from a CSV file.
    
    Example usage:
        python train.py -d data.csv -o my_model.pkl
    """
    click.echo(f"Loading data from {data_file}...")
    
    # Load the data
    try:
        df = pd.read_csv(data_file)
        click.echo(f"Loaded {len(df)} samples")
    except Exception as e:
        click.echo(f"Error loading data: {e}", err=True)
        raise click.Abort()
    
    # Split features and target
    X = df.drop(columns=['target'])
    y = df['target']
    
    click.echo(f"Features: {X.shape[1]} columns")
    

    X_train, y_train = X, y
    
    # Train the model
    click.echo("\nTraining model...")
    model = CancerModel()
    
    try:
        model.fit(X_train, y_train)
        click.echo("Model trained successfully")
    except Exception as e:
        click.echo(f"Error training model: {e}", err=True)
        raise click.Abort()
    
    # Show train accuracy
    train_accuracy = model.accuracy(X_train, y_train)
    click.echo(f"Training accuracy: {train_accuracy:.4f}")
    
    # Save the model
    click.echo(f"\nSaving model to {output_model}...")
    try:
        model.save(output_model)
        click.echo(f"Model saved successfully")
    except Exception as e:
        click.echo(f"Error saving model: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option(
    '--model-file',
    '-m',
    type=click.Path(exists=True),
    required=True,
    help='Path to the trained model file'
)
@click.option(
    '--test-file',
    '-t',
    type=click.Path(exists=True),
    required=True,
    help='Path to the CSV file containing test data'
)
@click.option(
    '--show-predictions',
    '-p',
    is_flag=True,
    help='Show individual predictions for each sample'
)
def test(model_file, test_file, show_predictions):
    """Test a trained model on new data.
    
    Example usage:
        cancer-predict test -m cancer_model.pkl -t test_data.csv
        cancer-predict test -m cancer_model.pkl -t test_data.csv --show-predictions
    """
    click.echo(f"Loading model from {model_file}...")
    
    # Load the model
    model = CancerModel()
    try:
        model.load(model_file)
        click.echo("Model loaded successfully")
    except Exception as e:
        click.echo(f"Error loading model: {e}", err=True)
        raise click.Abort()
    
    click.echo(f"\nLoading test data from {test_file}...")
    
    # Load test data
    try:
        df = pd.read_csv(test_file)
        click.echo(f"Loaded {len(df)} test samples")
    except Exception as e:
        click.echo(f"Error loading test data: {e}", err=True)
        raise click.Abort()
    
    # Split features and target
    X_test = df.drop(columns=['target'])
    y_test = df['target']
    
    # Calculate accuracy
    click.echo("\nEvaluating model...")
    try:
        accuracy = model.accuracy(X_test, y_test)
        click.echo(f"Test accuracy: {accuracy:.4f}")
    except Exception as e:
        click.echo(f"Error evaluating model: {e}", err=True)
        raise click.Abort()
    
    # Show predictions if requested
    if show_predictions:
        click.echo("\nPredictions:")
        click.echo("-" * 50)
        predictions = model.predict(X_test)
        
        for i, (diagnosis, confidence) in enumerate(predictions):
            actual = model.target_to_diagnosis(y_test.iloc[i])
            correct = "✓" if diagnosis == actual else "✗"
            click.echo(
                f"Sample {i+1}: {diagnosis} ({confidence:.2f}) | "
                f"Actual: {actual} {correct}"
            )
        
        # Summary statistics
        correct_count = sum(
            1 for i, (diagnosis, _) in enumerate(predictions)
            if diagnosis == model.target_to_diagnosis(y_test.iloc[i])
        )
        click.echo("-" * 50)
        click.echo(f"Correct predictions: {correct_count}/{len(predictions)}")


if __name__ == '__main__':
    cli()
```

We create a new folder inside `cancer_prediction` called `scripts`.

We also need to add the `click` library. Since this is a main dependancy, we can add it using the regular `uv add` command.

## Additions to the `.toml` file
The first thing we need to do is add an entry point to our `toml` file:
```bash
[project.scripts]
train = "cancer_prediction.scripts.app:train"
```

We can check that it works, but running in the command line:
```bash
uv run train -d 'data/breast_cancer_train.csv' -o 'models/cancer_model_2.pkl'
```

This likely won't work, because our environment is not really aware that we can do this, so let's try installing our package locally
```bash
pip install -e .
```

Now try the command again. Hopefull you should get some training stats reported, and a new model saved in your folder. Great!

Now try running `uv sync`...you should get a message that says something like
```bash
warning: Skipping installation of entry points (`project.scripts`) because this project is not packaged; to install entry points, set `tool.uv.package = true` or define a `build-system`
Resolved 86 packages in 0.80ms
Audited 81 packages in 1ms
```

Interesting...

Ultimately we want someone to be able to do:
```bash
pip install cancer-prediction
```

and then
```
cancer-prediction train
cancer-prediction test
```

We have defined our `train` command, but your bash terminal will not recognize the command `cancer-prediction`! To do this, we first need to make some other changes. We add the following lines to the bottom of `pyproject.toml`:
```toml
[project.scripts]
cancer-prediction = "cancer_prediction.scripts.app:cli"

[build-system]
requires = ["uv_build>=0.9.5,<0.10.0"]
build-backend = "uv_build"

[tool.uv]
package = true
```

This tells Python: "When I type the command `cancer-prediction` in my terminal, run the function `cli` from `cancer_prediction/scripts/app.py`"
Next, install the project locally with
```bash
pip install -e .
```

We can now try it out by running
```bash
cancer-prediction test -t 'data/breast_cancer_train.csv' -m 'models/cancer_model_2.pkl'
```

and you should get some stuff printed to the terminal:
```bash
Loading model from models/cancer_model_2.pkl...
Model loaded successfully

Loading test data from data/breast_cancer_train.csv...
Loaded 455 test samples

Evaluating model...
Test accuracy: 0.9473
```

<br>
![Dark Souls Bonfire](../imgs/dark-souls-bonfire.gif "Commit your changes and rest, weary traveller"){ width="50" .center }
<br>

## Further reading
<div class="grid cards" markdown>

-   :fontawesome-solid-book-open:{ .lg .middle } [__uv resources__](../../resources/references.md#uv)

    ---
    Information on uv, toml files, and licensing

</div>