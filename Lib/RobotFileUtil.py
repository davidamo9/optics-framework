import pandas as pd
import csv
import re

def generate_robot_test_case_file_from_csv(test_case_csv_file, output_test_case_robot_file):
        """
        Generates a Robot Framework test case file from a given CSV file.

        Args:
            csv_file_path (str): Path to the input CSV file containing test cases and steps.
            output_file_path (str): Path to the output Robot Framework file to be generated.
        """
        # Read the CSV file and organize the test cases
        test_cases = {}

        with open(test_case_csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                test_case_name = row['test_case']
                test_step = row['test_step']
                if test_case_name not in test_cases:
                    test_cases[test_case_name] = []
                test_cases[test_case_name].append(test_step)

        # Generate the Robot Framework file
        with open(output_test_case_robot_file, 'w') as robotfile:
            # Write the Settings section
            robotfile.write("*** Settings ***\n")
            robotfile.write("Resource   ${{EXECDIR}}/Resource/keyboard.robot\n\n")  # Example of an external keyword file
 
            
            # Write the Variables section
            robotfile.write("*** Variables ***\n")
 

            # Write the Keywords section (if needed)
            robotfile.write("*** Keywords ***\n")


            # Write the Test Cases section
            robotfile.write("*** Test Cases ***\n\n")

            for test_case_name, steps in test_cases.items():
                # Convert test case name to a tag-friendly format (replace spaces with underscores)
                tag_name = test_case_name.replace(" ", "_")
                
                # Write the test case name and tag
                robotfile.write(f"{test_case_name}\n")
                robotfile.write(f"    [Tags]    {tag_name}\n")
                
                # Write each step of the test case
                for step in steps:
                    robotfile.write(f"    {step}\n")
                
                robotfile.write("\n")
def generate_module_keywords_from_csv(module_csv_file, module_output_robot_file):
        # Load the CSV file into a DataFrame
        df = pd.read_csv(module_csv_file)

        # Open the output file for writing the keywords
        with open(module_output_robot_file, 'w') as f:
            f.write(f"*** Settings ***\n\n")

            f.write(f"Resource    ${{EXECDIR}}/VariableFiles/variables.robot\n\n")

            f.write(f"*** Keywords ***\n\n")

            # Get distinct module names
            module_names = df['module_name'].unique()

            for module in module_names:
                f.write(f"{module}\n")
                module_steps = df[df['module_name'] == module]

                for _, row in module_steps.iterrows():
                    # Prepare the step string based on non-empty parameters
                    step = f"    {row['module_step']}"
                    if pd.notna(row['param_1']):
                        step += f"    {row['param_1']}"
                    if pd.notna(row['param_2']):
                        step += f"    {row['param_2']}"
                    step += "\n"
                    f.write(step)

                f.write("\n")

def extract_variables(df):
        """Extract all variables from the DataFrame."""
        variables = set()
        variable_pattern = re.compile(r'\$\{[^}]+\}')

        for column in ['param_1', 'param_2']:
            for item in df[column].dropna():
                found_vars = variable_pattern.findall(item)
                variables.update(found_vars)
        
        return variables

def generate_robot_variables(variables, output_file):
    # Open the output file for writing the variables
    with open(output_file, 'w') as f:
        f.write(f"*** Variables ***\n\n")
        for variable in variables:
            f.write(f"{variable}    ${{EMPTY}}\n")

def generate_variables_file(csv_module_file=None, robot_variables_file=None):
    df = pd.read_csv(csv_module_file)
    variables = extract_variables(df)
    generate_robot_variables(variables=variables, output_file=robot_variables_file)

def generate_robot_file_from_csv(csv_file_path, output_file_path):
    """
    Generates a Robot Framework test case file from a given CSV file.

    Args:
        csv_file_path (str): Path to the input CSV file containing test cases and steps.
        output_file_path (str): Path to the output Robot Framework file to be generated.
    """
    # Read the CSV file and organize the test cases
    test_cases = {}

    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        # Print the fieldnames to debug the issue
        print("CSV Headers:", reader.fieldnames)

        for row in reader:
            test_case_name = row['test_case'].strip()  # Use strip() to remove any leading/trailing spaces
            test_step = row['test_step'].strip()  # Use strip() to remove any leading/trailing spaces
            if test_case_name not in test_cases:
                test_cases[test_case_name] = []
            test_cases[test_case_name].append(test_step)

    # Generate the Robot Framework file
    with open(output_file_path, 'w') as robotfile:
        # Write the Settings section
        robotfile.write("*** Settings ***\n")
        robotfile.write("Resource   ${EXECDIR}/Resources/modules.robot\n\n")  # Example of an external keyword file

        # Write the Variables section
        robotfile.write("*** Variables ***\n\n")

        # Write the Keywords section (if needed)
        robotfile.write("*** Keywords ***\n\n")


        # Write the Test Cases section
        robotfile.write("*** Test Cases ***\n\n")

        for test_case_name, steps in test_cases.items():
            # Convert test case name to a tag-friendly format (replace spaces with underscores)
            tag_name = test_case_name.replace(" ", "_")
            
            # Write the test case name and tag
            robotfile.write(f"{test_case_name}\n")
            robotfile.write(f"    [Tags]    {tag_name}\n")
            
            # Write each step of the test case
            for step in steps:
                robotfile.write(f"    {step}\n")
            
            robotfile.write("\n")


# def generate_test_cases_file(csv_journey_file=None, robot_journey_file=None):
#     q = CsvLibrary()
#     q.generate_robot_test_case_file_from_csv(test_case_csv_file=csv_journey_file, output_test_case_robot_file=robot_journey_file)

# def generate_keyword_file(csv_keyword_file=None, robot_keywords_file=None):
#     q = CsvLibrary()
#     q.generate_robot_keywords_from_csv(csv_file=csv_keyword_file, output_file=robot_keywords_file)
    

# def generate_variables_file(csv_keyword_file=None, robot_variables_file=None):
#     r = CsvLibrary()
#     df = pd.read_csv(csv_keyword_file)
#     variables = r.extract_variables(df)
#     r.generate_robot_variables(variables=variables, output_file=robot_variables_file)
    

# Input
script_base_dir = "/Users/lalitanand/Desktop/ICICI/share/icici-scripts-optics-framework/"
modules_csv_file = script_base_dir + "/input/modules.csv"
test_cases_csv_file = script_base_dir + "/input/ft_test_cases.csv"

# # Output
module_output_robot_file = script_base_dir + "/Resources/modules.robot"
variables_output_file =  script_base_dir + "/VariableFiles/variables.robot"
test_case_output_file =  script_base_dir + "/TestSuite/ft_test_cases.robot"
# fake_framework_output_file = script_base_dir + "/Lib/fake_framework.py"

# generate_keyword_file(csv_keyword_file=modules_csv_file, robot_keywords_file=keywords_output_file)
generate_variables_file(csv_module_file=modules_csv_file, robot_variables_file=variables_output_file)
generate_robot_test_case_file_from_csv(test_case_csv_file=test_cases_csv_file, output_test_case_robot_file=test_case_output_file)
generate_module_keywords_from_csv(module_csv_file=modules_csv_file, module_output_robot_file=module_output_robot_file)

# generate_robot_file_from_csv(csv_file_path=test_cases_csv_file, output_file_path=test_case_output_file)


