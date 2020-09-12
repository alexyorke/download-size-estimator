# download-size-estimator
Estimates the total amount of data to download using a stopping criterion with error bounds.

Ever need to download a set of files but don't know how large the files are, just how many files there are in total? `download-size-estimator` will calculate a file-size sample of the provided files and give a confidence interval as to how accurate the estimate is so that resources can be provisioned correctly.
