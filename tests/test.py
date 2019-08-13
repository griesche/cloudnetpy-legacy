import os
import sys
sys.path.append(os.path.split(os.getcwd())[0])
import warnings
import glob
from zipfile import ZipFile
import pytest
import requests
import netCDF4
from tests import run_testcase_processing as process

warnings.filterwarnings("ignore")


def _get_default_path():
    return f"{os.getcwd()}/source_data/"


def main():

    def _load_test_data():
        def _extract_zip():
            sys.stdout.write("\nLoading input files...")
            r = requests.get(url)
            open(full_zip_name, 'wb').write(r.content)
            fl = ZipFile(full_zip_name, 'r')
            fl.extractall(input_path)
            fl.close()
            sys.stdout.write("    Done.\n")

        url = 'http://devcloudnet.fmi.fi/files/cloudnetpy_test_input_files.zip'
        zip_name = os.path.split(url)[-1]
        full_zip_name = f"{input_path}{zip_name}"
        is_dir = os.path.isdir(input_path)
        if not is_dir:
            os.mkdir(input_path)
            _extract_zip()
        else:
            is_file = os.path.isfile(full_zip_name)
            if not is_file:
                _extract_zip()

    print(f"\n{22*'#'} Running all CloudnetPy tests {22*'#'}")

    c_path = f"{os.path.split(os.getcwd())[0]}/cloudnetpy/"
    input_path = _get_default_path()
    _load_test_data()

    options = "--tb=line"
    site = 'mace-head'

    print("\nTesting raw files:\n")
    test = pytest.main([options, f"{c_path}instruments/tests/raw_files_test.py"])
    _check_failures(test, "raw")

    print("\nProcessing CloudnetPy calibrated files from raw files:\n")
    process.process_cloudnetpy_raw_files(site, input_path)

    print("\nTesting calibrated files:\n")
    test = pytest.main([options, f"{c_path}instruments/tests/calibrated_files_test.py"])
    _check_failures(test, "calibrated")

    print("\nProcessing CloudnetPy categorize file:\n")
    process.process_cloudnetpy_categorize(site, input_path)

    print("\nTesting categorize file:\n")
    test = pytest.main([options, f"{c_path}categorize/tests/categorize_file_test.py"])
    _check_failures(test, "category")

    print("\nProcessing CloudnetPy product files:\n")
    process.process_cloudnetpy_products(input_path)

    print("\nTesting product files:\n")
    test = pytest.main([options, f"{c_path}products/tests/product_files_test.py"])
    _check_failures(test, "product")

    print(f"\n{10*'#'} All tests passed and processing works correctly! {10*'#'}")


def initialize_test_data(instrument, source_path=None):
    """
    Finds all file paths and parses wanted files to list
    """
    if not source_path:
        source_path = _get_default_path()
    test_data = glob.glob(f"{source_path}*.nc")
    paths = []
    for inst in instrument:
        for file in test_data:
            if inst in file:
                paths.append(file)
    return paths


def _check_failures(tests, var):
    if tests in (1, 3):
        print(f"\n{20*'#'} Error in {var} file testing! {20*'#'}")
        sys.exit()


def missing_var_msg(missing_keys, name):
    return f"Variable(s) {missing_keys} missing in {name} file!"


def collect_variables(instrument_list):
    test_data_path = initialize_test_data(instrument_list)
    key_dict = {}
    for path, instrument in zip(test_data_path, instrument_list):
        key_dict[instrument] = set(netCDF4.Dataset(path).variables.keys())
    return key_dict


if __name__ == "__main__":
    main()
