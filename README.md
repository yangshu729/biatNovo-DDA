### Prerequisites for developing
We recommend using docker base image: nvcr.io/nvidia/pytorch:23.10-py3
1. Install Git LFS.

    Install Git LFS and its related packages by running the following commands.
    ```bash
    sudo apt-get update -y
    sudo apt-get install git-lfs
    ```
    After installation, navigate to the repository directory and execute `git lfs install` to enable Git LFS.

2. Install depedencies.

    ```bash
    pip install -r requirements.txt
    ```

### The steps to run the predict code
#### Install the python-C library

Navigate to the `Bianovo/DataProcess` directory and execute the following command: `python deepnovo_cpython_setup.py build && python deepnovo_cpython_setup.py install`. This command will compile the native I/O related code and install the `DataProcess` library into the global Python path.

To ensure that the package has been installed correctly, you can verify it by running a simple test using the following command: `python Biatnovo/DataProcessing/deepnovo_worker_test.py`

### Knapsack data preparing
Unzip the `knapsack.npy.zip`, and put the uncompressed data into the root folder of the repository.

#### Start inference

The `DENOVO_INPUT_DIR` should contain the mgf file and feature file. The name must be `features.csv` and `spectrum.mgf`
User can donwload the checkpoint from our release page
Run command:
```bash
export DENOVO_INPUT_DIR=input_data
export DENOVO_OUTPUT_DIR=outputs
export DENOVO_OUTPUT_FILE=outputs.tab
python main.py  --search_denovo --train_dir /checkpoint_folder/
```
to start inference.
