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