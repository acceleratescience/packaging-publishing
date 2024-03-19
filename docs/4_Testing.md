## 4. Testing
Now that the file structure is setup, try running the software with
```bash
streamlit run cancer_prediction/streamlit_app.py
```

When you reach a point that everything seems to be working, it's probably a good idea to commit your changes...

We'll now introduce some basic tests just to get an idea for how testing works. In the `cancer_model.py` file, there is a class method called `diagnosis_to_target()`, and another class method called `target_to_diagnosis()`. We will write a test for these.

Add a new file in the `test` directory called `test_CancerModel.py`. Import `unittest` and the relevant modules. We typically have a single test class for each actual class, and then test each method within the test class. This maintains cohesion on a class level. You can then have different test files for different actual files. So we start these tests like so:

```python
class TestCancerModel(unittest.TestCase):
```

Try writing test cases for these two methods. Think about how you would run this method in a Jupyter Notebook.

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

To run the tests, we click on the "Testing" tab on the sidebar, and then "Configure Python Tests". The order of clicks is as follows:

`unittest` -> `tests` -> `test_*.py`

This selects what type of testing framework to use, where the tests are located and what naming convention we have used for the files.

Now that the tests have run succesfully, it's time to commit and push the changes.

But it's annoying to have to run these tests everytime...surely we can automate it...