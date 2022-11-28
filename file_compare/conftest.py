import pytest


@pytest.fixture(scope="session", autouse=True)
def initialize_test_run(request):
    try:
        global is_output_needed
        output_excel_need = request.config.getoption("--output_excel")

        if str(output_excel_need).lower() == "yes":
            is_output_needed = "yes"
        else:
            is_output_needed = "no"

    except Exception as exception:
        print("Error in Session Method : " + str(exception))


# command line arguments
def pytest_addoption(parser):
    parser.addoption("--output_excel", action="store", default="no")


# Gett the input
@pytest.fixture(scope='function')
def is_excel_ouput_needed(request):
    try:
        return  is_output_needed
    except Exception as exception:
        print(str(exception))
