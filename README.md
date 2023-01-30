# corise-mlops
co:rise mlops course

Step 5 can be found in the file `week3/project/step5.py` you should be able to run it just executing this command while in the same directory:

```bash
python step5.py
```

I commited the logs.out from step5, so you should be able to see that in the file `week3/project/data/logs.out`

The test execution was a little bit weird to setup but you should be able to run it from the same directory with the following command:
```bash
python -m pytest test_app.py
```
In order to make the tests work I had to add a pytest.ini file so it could set the right python path for things to be loaded.