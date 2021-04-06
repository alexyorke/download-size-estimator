# download-size-estimator
Estimates the total amount of data to download using a stopping criterion with error bounds.

Ever need to download a set of files but don't know how large the files are, just how many files there are in total? `download-size-estimator` will calculate a file-size sample of the provided files and give a confidence interval as to how accurate the estimate is so that resources can be provisioned correctly.

## How to use

- Install requirements from `requirements.txt`

```bash
alex@DESKTOP-2BT8H8S:~$ echo -e https://dummyimage.com/400x{400..450}/999/fff.jpg\\n | python3 download-size-estimator.py
4.8KiB±121.7B (95% conf., 5% error)
```
