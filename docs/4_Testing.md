We have an empty `tests` directory! We should introduce some basic tests just to get an idea for how testing works.

## Basic tests
In the `cancer_model.py` file, there is a class method called `diagnosis_to_target()`, and another class method called `target_to_diagnosis()`. We will write a test for these using [Unittest](https://docs.python.org/3/library/unittest.html). This is not the only testing framework - another popular one is Pytest.

Add a new file in the `test` directory called `test_CancerModel.py`. Import `unittest` and the relevant modules. We typically have a single test class for each actual class, and then test each method within the test class. This maintains cohesion on a class level. You can then have different test files for different actual files.

A test case is created by subclassing unittest.TestCase. The individual tests are defined with methods whose names start with the letters `test`. This naming convention informs the test runner about which methods represent tests:
```python
class TestCancerModel(unittest.TestCase):

    def test_whatever_method():
        pass
```

We then write methods for each corresponding method in our class that we want to test. Think about how you would run the `diagnosis_to_target()` method in a Jupyter Notebook:
```python
from cancer_prediction.cancer_model import CancerModel

model = CancerModel()
model.diagnosis_to_target("Benign")

1
```

The crux of each test is a call to an assert, for example
- `assertEqual()` to check for an expected result;
- `assertTrue()` or `assertFalse()` to verify a condition;
- `assertRaises()` to verify that a specific exception gets raised.

These methods are used instead of the assert statement so the test runner can accumulate all test results and produce a report.

Now trying writing test cases for these two models.

<details>
<summary>Click to reveal the answer</summary>

```python
import unittest

from cancer_prediction.cancer_model import CancerModel


class TestCancerModel(unittest.TestCase):

    def test_diagnosis_to_target(self):
        model = CancerModel()
        diagnosis = 'Malignant'
        target = model.diagnosis_to_target(diagnosis)
        self.assertEqual(target, 0)

        diagnosis = 'Benign'
        target = model.diagnosis_to_target(diagnosis)
        self.assertEqual(target, 1)

    def test_target_to_diagnosis(self):
        model = CancerModel()
        target = 0
        diagnosis = model.target_to_diagnosis(target)
        self.assertEqual(diagnosis, 'Malignant')

        target = 1
        diagnosis = model.target_to_diagnosis(target)
        self.assertEqual(diagnosis, 'Benign')

if __name__ == '__main__':
    unittest.main()

```
</details> 

## Running tests
### In the VSCode UI
To run the tests, we click on the "Testing" tab on the sidebar, and then "Configure Python Tests". The order of clicks is as follows:

`unittest` -> `tests` -> `test_*.py`

This selects what type of testing framework to use, where the tests are located and what naming convention we have used for the files.

### In the terminal
We can also run these tests in the command line. We will need to know this for later, when we automate the testing process:
```bash
uv run python -m unittest discover tests/
```

You should see something like:
```
$ uv run python -m unittest discover tests/
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

You can try changing part of the test code to force them to fail, and check the output. Now that the tests have run succesfully, it's time to commit and push the changes.

<br>
![Dark Souls Bonfire](../imgs/dark-souls-bonfire.gif "Commit your changes and rest, weary traveller"){ width="50" .center }
<br>

!!! note

    For some reason Codespaces is not discovering the tests. Just run them in the terminal for now. But VSCode run locally should work fine.

## Further reading
<div class="grid cards" markdown>

-   :fontawesome-solid-book-open:{ .lg .middle } [__Testing resources__](resources/references.md#testing)

    ---
    Information on `unittest`, Pytest, and testing in VSCode

</div>
