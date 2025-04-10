import os
import sys
import json
import re

def extract_xpath(test_name):
    """
    Extracts the xpath portion from a test name string.
    For example, if test_name is:
      "Sets and Get <- /system/aaa/accounting/events/event[event-type=AAA_ACCOUNTING_EVENT_COMMAND]/config/event-type -> AAA_AUTHORIZATION_EVENT_COMMAND"
    This function returns:
      "/system/aaa/accounting/events/event[event-type=AAA_ACCOUNTING_EVENT_COMMAND]/config/event-type"
    If the pattern is not found, returns the full test_name.
    """
    return re.sub(r'\[.*?\]', '', test_name.split("<-")[1].split("->")[0].strip()) if "<-" in test_name and "->" in test_name else test_name

def parse_log_files_from_directory(directory):
    """
    Parse all JSON files in the specified directory and combine the results into a single JSON object.
    """
    combined_data = []  # Initialize as an empty list to hold all the JSON data
    
    for filename in os.listdir(directory):
        if filename.endswith("_result.json"):

            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)  # Load the JSON data from the file
                    
                    # Check if data is a dictionary or list, and handle accordingly
                    if isinstance(data, list):
                        combined_data.extend(data)  # Add all elements of the list to combined_data
                    elif isinstance(data, dict):
                        combined_data.append(data)  # Add the entire dictionary to combined_data
                    else:
                        print(f"Unexpected data format in {filename}")
                        continue  # This continues to the next file if the data format is not list or dict

            except Exception as e:
                print(f"Error reading file {filename}: {e}")
                continue  # This continues to the next file if there is an error reading it
    
    # Write the full combined data to a .json file for debugging
    with open('combined_data.json', 'w', encoding='utf-8') as txt_file:
        json.dump(combined_data, txt_file, indent=4)
    
    return combined_data

def dict_data_handling(files,filename_result):
    tests_total_validations = 0 
    tests_passed_validations = 0
    tests_failed_validations = 0
    tests_ignored_validations = 0
    tests_pass = 0  # Initialize the variable
    tests_total = 0  # Initialize the variable
    tests_fail = 0   # Initialize the variable
    model_info = "N/A"
    model_info_str = set()  # Initialize the variable
    actual_test_release = ""         # Initialize the variable
    test_release = ""                 # Initialize the variable
    actual_test_platform = ""         # Initialize the variable
    test_platform = ""                 # Initialize the variable
    overall_result = "FAIL"  # Initialize the variable
    total_deviations = 0
    total_paths = 0
    set_xpaths = 0
    state_only = 0
    set_get_sub = 0
    deviations_count = 0
    input_xpaths = 0
    input_state_xpaths = 0
    test_set_get_sub = 0
    test_state = 0
    test_xpaths = 0
    test_coverage = 0
    test_coverage_str = "0.00% [0/0]"
    pure_failures = 0
    deviation_failures = 0
    detail_rows = ""

    platform_support_summary = ""
    if isinstance(files, list):
        for data in files:
            # Accessing the "test_target" in each dictionary in the list
            test_target = data.get("test_target", "N/A")
            description = data.get("description", "")
            labels = data.get("labels", [])
            results = data.get("results", [])
            start_time = data.get("start_time_sec", 0)
            end_time = data.get("end_time_sec", 0)
            duration = end_time - start_time
            # Store previous values for comparison
            previous_tests_total_validations = tests_total_validations
            previous_tests_passed_validations = tests_passed_validations
            previous_tests_failed_validations = tests_failed_validations
            previous_tests_ignored_validations = tests_ignored_validations
            previous_tests_pass = tests_pass
            previous_tests_total = tests_total
            previous_tests_fail = tests_fail
            # Get new values from data
            new_tests_total_validations = data.get("tests_total_validations", 0)
            new_tests_passed_validations = data.get("tests_passed_validations", 0)
            new_tests_failed_validations = data.get("tests_failed_validations", 0)
            new_tests_ignored_validations = data.get("tests_ignored_validations", 0)
            new_tests_pass = data.get("tests_pass", 0)
            new_tests_total = data.get("tests_total", 0)
            new_tests_fail = data.get("tests_fail", 0)
            # Add new values only if they are different from the previous values
            if new_tests_total_validations != previous_tests_total_validations:
                tests_total_validations += new_tests_total_validations
            
            if new_tests_passed_validations != previous_tests_passed_validations:
                tests_passed_validations += new_tests_passed_validations
            
            if new_tests_failed_validations != previous_tests_failed_validations:
                tests_failed_validations += new_tests_failed_validations

            if new_tests_ignored_validations != previous_tests_ignored_validations:
                tests_ignored_validations += new_tests_ignored_validations

            if new_tests_pass != previous_tests_pass:
                tests_pass += new_tests_pass

            if new_tests_total != previous_tests_total:
                tests_total += new_tests_total

            if new_tests_fail != previous_tests_fail:
                tests_fail += new_tests_fail
            
            overall_result = "FAIL" if tests_fail > 0 else "PASS"
            


            metadata = data.get("metadata", {})
            model_info_str.update(labels)
            model_info = ", ".join(model_info_str) if model_info_str else "N/A"
            summary = metadata.get("summary_dict", {})
            deviations = metadata.get("deviations", {})
            platform_support = metadata.get("platform_support", {})
            # Store previous values for comparison
            previous_total_deviations = total_deviations
            previous_total_paths = total_paths
            previous_set_xpaths = set_xpaths
            previous_state_only = state_only
            previous_set_get_sub = set_get_sub
            previous_deviations_count = deviations_count
            previous_input_xpaths = input_xpaths
            previous_input_state_xpaths = input_state_xpaths
            previous_test_set_get_sub = test_set_get_sub
            previous_test_state = test_state
            previous_test_xpaths = test_xpaths
            previous_test_coverage = test_coverage

            # Get new values from metadata and summary
            new_total_deviations = metadata.get("total_deviations", 0)
            new_total_paths = summary.get("total_xpaths", 0)
            new_set_xpaths = summary.get("set_xpaths", 0)
            new_state_only = summary.get("state_only", 0)
            new_set_get_sub = summary.get("set_get_sub", 0)
            new_deviations_count = summary.get("deviations", 0)
            new_input_xpaths = summary.get("input_xpaths", 0)
            new_input_state_xpaths = summary.get("input_state_xpaths", 0)
            new_test_set_get_sub = summary.get("test_set_get_sub", 0)
            new_test_state = summary.get("test_state", 0)
            new_test_xpaths = summary.get("test_xpaths", 0)
            new_test_coverage = summary.get("test_coverage", 0)

            # Add new values only if they are different from the previous values
            if new_total_deviations != previous_total_deviations:
                total_deviations += new_total_deviations

            if new_total_paths != previous_total_paths:
                total_paths += new_total_paths

            if new_set_xpaths != previous_set_xpaths:
                set_xpaths += new_set_xpaths

            if new_state_only != previous_state_only:
                state_only += new_state_only

            if new_set_get_sub != previous_set_get_sub:
                set_get_sub += new_set_get_sub

            if new_deviations_count != previous_deviations_count:
                deviations_count += new_deviations_count

            if new_input_xpaths != previous_input_xpaths:
                input_xpaths += new_input_xpaths

            if new_input_state_xpaths != previous_input_state_xpaths:
                input_state_xpaths += new_input_state_xpaths

            if new_test_set_get_sub != previous_test_set_get_sub:
                test_set_get_sub += new_test_set_get_sub

            if new_test_state != previous_test_state:
                test_state += new_test_state

            if new_test_xpaths != previous_test_xpaths:
                test_xpaths += new_test_xpaths

            if new_test_coverage != previous_test_coverage:
                test_coverage += new_test_coverage
            
            actual_test_release_str = summary.get("actual_test_release", [])
            existing_releases = set(actual_test_release.split(", ")) if actual_test_release else set()

            if isinstance(actual_test_release_str, list):
                for release in actual_test_release_str:
                    if str(release) not in existing_releases:  # Add only if not present
                        if actual_test_release:  # Add a comma if content exists
                            actual_test_release += ", "
                        actual_test_release += str(release)
                        existing_releases.add(str(release))
            else:
                if str(actual_test_release_str) not in existing_releases:  # Add only if not present
                    if actual_test_release:  # Add a comma if content exists
                        actual_test_release += ", "
                    actual_test_release += str(actual_test_release_str)
            
            #test_release_str = summary.get("test_release", [])
            #test_release += ", ".join(test_release_str) + ", " if isinstance(test_release_str, list) else str(test_release_str) + ", "

            test_release_str = summary.get("test_release", [])
            existing_releases = set(test_release.split(", ")) if test_release else set()

            if isinstance(test_release_str, list):
                for release in test_release_str:
                    if str(release) not in existing_releases:  # Add only if not present
                        if test_release:  # Add a comma if content exists
                            test_release += ", "
                        test_release += str(release)
                        existing_releases.add(str(release))
            else:
                if str(test_release_str) not in existing_releases:  # Add only if not present
                    if test_release:  # Add a comma if content exists
                        test_release += ", "
                    test_release += str(test_release_str)

            test_platform_str = summary.get("test_platform", [])
            existing_platforms = set(test_platform.split(", ")) if test_platform else set()

            if isinstance(test_platform_str, list):
                for platform in test_platform_str:
                    if str(platform) not in existing_platforms:  # Add only if not present
                        if test_platform:  # Add a comma if content exists
                            test_platform += ", "
                        test_platform += str(platform)
                        existing_platforms.add(str(platform))
            else:
                if str(test_platform_str) not in existing_platforms:  # Add only if not present
                    if test_platform:  # Add a comma if content exists
                        test_platform += ", "
                    test_platform += str(test_platform_str)
                    existing_platforms.add(str(test_platform_str))

            previous_platform_support_summary = platform_support_summary

            platform_support_summary_str = summary.get("platform_support", [])

            existing_platform_supports = set(platform_support_summary.split(", ")) if platform_support_summary else set()

            # Add values only if they are not already present
            if isinstance(platform_support_summary_str, list):
                for platform in platform_support_summary_str:
                    if str(platform) not in existing_platform_supports:  # Add only if not present
                        if platform_support_summary:  # Add a comma if content exists
                            platform_support_summary += ", "
                        platform_support_summary += str(platform)
                        existing_platform_supports.add(str(platform))
            else:
                if str(platform_support_summary_str) not in existing_platform_supports:  # Add only if not present
                    if platform_support_summary:  # Add a comma if content exists
                        platform_support_summary += ", "
                    platform_support_summary += str(platform_support_summary_str)

            if total_paths > 0:
                test_coverage = (test_xpaths / total_paths) * 100
                test_coverage_str = f"{test_coverage:.2f}% [{test_xpaths}/{total_paths}]"
    
            
 
         
    
            detail_rows = ""  # Initialize outside to retain rows
        s_no = 1          # Initialize serial number

        # Check if 'files' is a list or a single dictionary
        if isinstance(files, list):
            file_list = files
        else:
            file_list = [files]  # Wrap single file into a list for uniform processing

        # Loop through the files (single or multiple)
        for data in file_list:
            deviation_platform_count=0
            results = data.get("results", [])
            
            for result in sorted(results, key=lambda r: int(re.findall(r'\d+', r.get("test_id", "0"))[0])):
                testcase = result.get("test_name", "")
          

                # ✅ Handle the bold part if <- and -> are present
                if "<-" in testcase and "->" in testcase:
                    before = testcase.split("<-")[0].strip()
                    bold_part = testcase.split("<-")[1].split("->")[0].strip()
                    after = testcase.split("->")[1].strip()
                    testcase = f'{before} <- <b>{bold_part}</b> -> {after}'

                inner_results = result.get("results", [])
                
                if inner_results:
                    validations = inner_results[0].get("validations", {})
                    #op_dict = validations.get("Set_and_Get", {}).get("type", {})
                    section_name = next(iter(validations), None)
                    op_dict = validations.get(section_name, {}).get("type", {})
                    
                    if op_dict:
                        op_type = list(op_dict.keys())[0]
                     
                        #testcase_operation = "SET - " + op_type + " & GET" if op_type == "UPDATE" else "SET - " + op_type

                        if op_type == "UPDATE":
                            testcase_operation = "SET - " + op_type + " & GET" 
                        elif op_type in ["DELETE", "REPLACE"]:
                            testcase_operation = "SET - " + op_type
                        else:
                            if "SUBSCRIBE" in section_name.upper():
                                testcase_operation = "SUBSCRIBE - " + op_type
                            else:
                                testcase_operation = section_name.upper()
                    else:
                        testcase_operation = testcase.split("<-")[0].strip() if "<-" in testcase else testcase
                else:
                    testcase_operation = testcase.split("<-")[0].strip() if "<-" in testcase else testcase
                
                test_id = result.get("test_id", "")
                xpath = extract_xpath(testcase)
                success = "PASS" if result.get("success", False) else "FAIL"
                testcase_result = next((r.get("result", "N/A") for r in result.get("results", []) if "result" in r), "N/A")
                deviation_field = "No" if xpath not in deviations else "Yes"
                platform_val = platform_support.get(xpath, "NA")
                platform_val1 = platform_val if platform_val != "NA" else "Not Applicable"
                
                result_field = ""
                if success == "FAIL":
                    if deviation_field == "Yes":
                            deviation_failures += 1
                    if deviation_field == "Yes" or platform_val in ['NS', 'NA']:
                        deviation_platform_count = deviation_platform_count + 1 
                        result_field = "PASS" + "(D)" + f"(P-{platform_val1})"
                    elif deviation_field == "No" and platform_val in ['S']:
                        result_field = "FAIL"
                else:
                    if deviation_field == 'Yes':
                        deviation_field +=1
                    if deviation_field == "Yes" or platform_val in ['NS', 'NA']:
                       
                        # deviation_failures += 1
                        deviation_platform_count = deviation_platform_count + 1   
                        result_field = "PASS" + "(D)" + f"(P-{platform_val1})"
                    else:
                        result_field = "PASS" + f"(P-{platform_val1})"

                total_validations = result.get("total_validations", 0)
                passed_validations = result.get("passed_validations", 0)
                failed_validations = result.get("failed_validations", 0)
                ignored_validations = result.get("ignored_validations", 0)
                coverage = result.get("coverage", 0)
                test_log = result.get("test_log", "N/A")
                gnmi_log = result.get("gnmi_log", "N/A")

                subscribe_field = "PASS" if result.get("success", False) else "FAIL"
                inner_logs = ""
                if success == "FAIL":
                    for inner_result in result.get("results", []):
                        log_text = inner_result.get("log", "N/A")
                        inner_logs += log_text + "<br/>"
                else:
                    inner_logs = ""

                # ✅ Append rows correctly for both cases
                detail_rows += f"""
                <tr>
                    <td style="text-align: right;">{s_no}</td>
                    <td>{test_id}</td>
                    <td>{testcase}</td>
                    <td>{testcase_operation}</td>   
                    <td>{success}</td>
                    <td>{deviation_field}</td>
                    <td>{platform_val1}</td>        
                    <td>{result_field}</td>
                    <td>
                   <a href="LOG_REPORT_PLACEHOLDER?test_id={test_id}" onclick="openLogInNewTab(event, '{test_id}', this)">{inner_logs}</a>
  
 </td>
                </tr>
                """
                    # <a href="{filename_result}_log_report.html?test_id={test_id}" onclick="openLogInNewTab(event, '{test_id}', this)">{inner_logs}</a>
                    # <td> <a href="javascript:void(0)" onclick='parent.postMessage({{"action": "navigateToLogReport", "testId": "{test_id}"}}, "*");'>{inner_logs}</a></td>
                    # <td>{inner_logs}</td>
                
                s_no += 1
      
    elif isinstance(files, dict):
        data=files
        #elif isinstance(files, dict):  # Handle single file (data is a dictionary) # If it's a single file, assign it directly
        test_target = data.get("test_target", "N/A") # Handle single file (data is a dictionary)
        data = files  # If it's a single file, assign it directly
        test_target = data.get("test_target", "N/A")
        description = data.get("description", "")
        labels = data.get("labels", [])
        model_info = ", ".join(labels) if labels else "N/A"
        results = data.get("results", [])
        start_time = data.get("start_time_sec", 0)
        end_time = data.get("end_time_sec", 0)
        duration = end_time - start_time

        previous_tests_total_validations = tests_total_validations
        previous_tests_passed_validations = tests_passed_validations
        previous_tests_failed_validations = tests_failed_validations
        previous_tests_ignored_validations = tests_ignored_validations
        previous_tests_pass = tests_pass
        previous_tests_total = tests_total
        previous_tests_fail = tests_fail
        new_tests_total_validations = data.get("tests_total_validations", 0)
        new_tests_passed_validations = data.get("tests_passed_validations", 0)
        new_tests_failed_validations = data.get("tests_failed_validations", 0)
        new_tests_ignored_validations = data.get("tests_ignored_validations", 0)
        new_tests_pass = data.get("tests_pass", 0)
        new_tests_total = data.get("tests_total", 0)
        new_tests_fail = data.get("tests_fail", 0)
        if new_tests_total_validations != previous_tests_total_validations:
            tests_total_validations += new_tests_total_validations
        if new_tests_passed_validations != previous_tests_passed_validations:
            tests_passed_validations += new_tests_passed_validations
        if new_tests_failed_validations != previous_tests_failed_validations:
            tests_failed_validations += new_tests_failed_validations
        if new_tests_ignored_validations != previous_tests_ignored_validations:
            tests_ignored_validations += new_tests_ignored_validations
        if new_tests_pass != previous_tests_pass:
            tests_pass += new_tests_pass
        if new_tests_total != previous_tests_total:
            tests_total += new_tests_total
        if new_tests_fail != previous_tests_fail:
            tests_fail += new_tests_fail
        overall_result = "FAIL" if tests_fail > 0 else "PASS"
        metadata = data.get("metadata", {})
        model_info_str.update(labels)
        model_info = ", ".join(model_info_str) if model_info_str else "N/A"
        summary = metadata.get("summary_dict", {})
        deviations = metadata.get("deviations", {})
        platform_support = metadata.get("platform_support", {})
        previous_total_deviations = total_deviations
        previous_total_paths = total_paths
        previous_set_xpaths = set_xpaths
        previous_state_only = state_only
        previous_set_get_sub = set_get_sub
        previous_deviations_count = deviations_count
        previous_input_xpaths = input_xpaths
        previous_input_state_xpaths = input_state_xpaths
        previous_test_set_get_sub = test_set_get_sub
        previous_test_state = test_state
        previous_test_xpaths = test_xpaths
        previous_test_coverage = test_coverage

        # Get new values from metadata and summary
        new_total_deviations = metadata.get("total_deviations", 0)
        new_total_paths = summary.get("total_xpaths", 0)
        new_set_xpaths = summary.get("set_xpaths", 0)
        new_state_only = summary.get("state_only", 0)
        new_set_get_sub = summary.get("set_get_sub", 0)
        new_deviations_count = summary.get("deviations", 0)
        new_input_xpaths = summary.get("input_xpaths", 0)
        new_input_state_xpaths = summary.get("input_state_xpaths", 0)
        new_test_set_get_sub = summary.get("test_set_get_sub", 0)
        new_test_state = summary.get("test_state", 0)
        new_test_xpaths = summary.get("test_xpaths", 0)
        new_test_coverage = summary.get("test_coverage", 0)
        # Add only if the new value is different
        if new_total_deviations != previous_total_deviations:
            total_deviations += new_total_deviations

        if new_total_paths != previous_total_paths:
            total_paths += new_total_paths

        if new_set_xpaths != previous_set_xpaths:
            set_xpaths += new_set_xpaths

        if new_state_only != previous_state_only:
            state_only += new_state_only

        if new_set_get_sub != previous_set_get_sub:
            set_get_sub += new_set_get_sub

        if new_deviations_count != previous_deviations_count:
            deviations_count += new_deviations_count

        if new_input_xpaths != previous_input_xpaths:
            input_xpaths += new_input_xpaths

        if new_input_state_xpaths != previous_input_state_xpaths:
            input_state_xpaths += new_input_state_xpaths

        if new_test_set_get_sub != previous_test_set_get_sub:
            test_set_get_sub += new_test_set_get_sub

        if new_test_state != previous_test_state:
            test_state += new_test_state

        if new_test_xpaths != previous_test_xpaths:
            test_xpaths += new_test_xpaths
        

        if new_test_coverage != previous_test_coverage:
            test_coverage += new_test_coverage
        actual_test_release_str = summary.get("actual_test_release", [])
        existing_releases = set(actual_test_release.split(", ")) if actual_test_release else set()

        if isinstance(actual_test_release_str, list):
            for release in actual_test_release_str:
                if str(release) not in existing_releases:  # Add only if not present
                    if actual_test_release:  # Add a comma if content exists
                        actual_test_release += ", "
                    actual_test_release += str(release)
                    existing_releases.add(str(release))
        else:
            if str(actual_test_release_str) not in existing_releases:  # Add only if not present
                if actual_test_release:  # Add a comma if content exists
                    actual_test_release += ", "
                actual_test_release += str(actual_test_release_str)
  


        test_release_str = summary.get("test_release", [])
        test_release += ", ".join(test_release_str) + ", " if isinstance(test_release_str, list) else str(test_release_str) + ", "
        test_platform_str = summary.get("test_platform", [])
        if isinstance(test_platform_str, list):
            if test_platform:  # Add a comma only if test_platform already has content
                test_platform += " ab"
            test_platform += ", ".join(test_platform_str)
        else:
            if test_platform:  # Add a comma only if test_platform already has content
                test_platform += "cd "
            test_platform += str(test_platform_str)
        # Store previous value for comparison
        previous_platform_support_summary = platform_support_summary
        # Get new value from summary
        platform_support_summary_str = summary.get("platform_support", [])
        # Convert the existing platform support into a set for comparison
        existing_platform_supports = set(platform_support_summary.split(", ")) if platform_support_summary else set()
        # Add values only if they are not already present
        if isinstance(platform_support_summary_str, list):
            for platform in platform_support_summary_str:
                if str(platform) not in existing_platform_supports:  # Add only if not present
                    if platform_support_summary:  # Add a comma if content exists
                        platform_support_summary += ", "
                    platform_support_summary += str(platform)
                    existing_platform_supports.add(str(platform))
        else:
            if str(platform_support_summary_str) not in existing_platform_supports:  # Add only if not present
                if platform_support_summary:  # Add a comma if content exists
                    platform_support_summary += ", "
                platform_support_summary += str(platform_support_summary_str)

        test_coverage_str = f"{test_coverage}% [{input_xpaths}/{total_paths}]"
        #breakpoint()
        detail_rows = ""
        s_no = 1
        for result in sorted(results, key=lambda r: int(re.findall(r'\d+', r.get("test_id", "0"))[0])):
            testcase = result.get("test_name", "")
            if "<-" in testcase and "->" in testcase:
                before = testcase.split("<-")[0].strip()
                bold_part = testcase.split("<-")[1].split("->")[0].strip()
                after = testcase.split("->")[1].strip()
                testcase = f'{before} <- <b>{bold_part}</b> -> {after}'
            inner_results = result.get("results", [])
            if inner_results:
                validations = inner_results[0].get("validations", {})
                op_dict = validations.get("Set_and_Get", {}).get("type", {})
                if op_dict:
                    op_type = list(op_dict.keys())[0]
                    testcase_operation = "SET - " + op_type + " & GET" if op_type == "UPDATE" else "SET - " + op_type
                else:
                    testcase_operation = testcase.split("<-")[0].strip() if "<-" in testcase else testcase
            else:
                testcase_operation = testcase.split("<-")[0].strip() if "<-" in testcase else testcase

            test_id = result.get("test_id", "")
            xpath = extract_xpath(testcase)
            success = "PASS" if result.get("success", False) else "FAIL"
            testcase_result = next((r.get("result", "N/A") for r in result.get("results", []) if "result" in r), "N/A")
            deviation_field = "No" if xpath not in deviations else "Yes"
            platform_val = platform_support.get(xpath, "NA")
            platform_val1 = platform_val if platform_val != "NA" else "Not Applicable"
            
            result_field = ""
            if success == "FAIL":
                if deviation_field == 'Yes':
                    deviation_field +=1
                if deviation_field == "Yes" or platform_val in ['NS', 'NA']:  
                    result_field = "PASS" + "(D)" + f"(P-{platform_val1})"
                elif deviation_field == "No" and platform_val in ['S']:
                    result_field = "FAIL"
            else:
                if deviation_field == 'Yes':
                    deviation_field +=1
                if deviation_field == "Yes" or platform_val in ['NS', 'NA']:  
                    result_field = "PASS" + "(D)" + f"(P-{platform_val1})"
                else:
                    result_field = "PASS" + f"(P-{platform_val1})"

            total_validations = result.get("total_validations", 0)
            passed_validations = result.get("passed_validations", 0)
            failed_validations = result.get("failed_validations", 0)
            ignored_validations = result.get("ignored_validations", 0)
            coverage = result.get("coverage", 0)
            test_log = result.get("test_log", "N/A")
            gnmi_log = result.get("gnmi_log", "N/A")

            subscribe_field = "PASS" if result.get("success", False) else "FAIL"
            inner_logs = ""
            if success == "FAIL":
                for inner_result in result.get("results", []):
                    log_text = inner_result.get("log", "N/A")
                    inner_logs += log_text + "<br/>"
            else:
                inner_logs = ""
            detail_rows += f"""
            <tr>
            <td style="text-align: right;">{s_no}</td>
            <td>{test_id}</td>
            <td>{testcase}</td>
            <td>{testcase_operation}</td>
            <td>{success}</td>
            <td>{deviation_field}</td>
            <td>{platform_val1}</td>
            <td>{result_field}</td>
            <td> <a href="javascript:void(0)" onclick='parent.postMessage({{"action": "navigateToLogReport", "testId": "{test_id}"}}, "*");'>{inner_logs}</a></td>
            </tr>
            """
            s_no += 1
    test_platform_str=test_platform
    base_dir = os.path.dirname(os.path.abspath(__file__))
    alternative_template_path = os.path.join("Report_Generators/Testcase_Report_HTML/template.html")
    main_template_path = os.path.join("template.html")

    template_path = alternative_template_path if os.path.exists(alternative_template_path) else main_template_path

    with open(template_path, "r", encoding="utf-8") as f:
        template_html = f.read()

    template_html = template_html.replace("xpath_model_info", str(model_info))
    template_html = template_html.replace("xpath_total_paths", str(total_paths))
    template_html = template_html.replace("xpath_config_paths", str(set_xpaths))
    template_html = template_html.replace("xpath_set_get_sub", str(set_get_sub))
    template_html = template_html.replace("xpath_state_only", str(state_only))
    template_html = template_html.replace("xpath_deviations", str(total_deviations))
    template_html = template_html.replace("xpath_p_result", str(test_platform_str))
    template_html = template_html.replace(
        "xpath_platform",
        f"Tagged : {test_platform}: {test_platform} - {input_xpaths}/{total_paths}"
    )

    template_html = template_html.replace("xpath_test_release", str(actual_test_release))
    template_html = template_html.replace("xpath_platform_support", str(platform_support_summary))
    template_html = template_html.replace("xpath_tested_paths", str(test_xpaths))
    template_html = template_html.replace("xpath_input_config", str(input_xpaths))
    template_html = template_html.replace("xpath_tested_set_get_sub", str(test_set_get_sub))
    template_html = template_html.replace("xpath_tested_state_only", str(state_only))
    template_html = template_html.replace("xpath_test_coverage", str(test_coverage_str))
    template_html = template_html.replace("xpath_total_testcases", str(tests_total))
    template_html = template_html.replace("xpath_passed", str(tests_pass))
    # template_html = template_html.replace("xpath_failed", str(tests_failed_validations))
    template_html = template_html.replace("xpath_failed",f"{tests_fail} [F - {abs(tests_fail - deviation_failures)} D/P/S - {deviation_failures}]"

)

    # template_html = template_html.replace("xpath_overall_result", str(overall_result))
 
    #template_html = template_html.replace("xpath_overall_result", "PASS" if deviation_failures > 0 and tests_failed_validations >= 0 else "FAIL")
    template_html = template_html.replace(
            "xpath_overall_result",
            "PASS" if (deviation_failures == 0 and tests_failed_validations == 0) or (deviation_failures > 0 and tests_failed_validations >= 0) else "FAIL"
        )
    template_html = template_html.replace("<!-- xpath_detail_rows -->", detail_rows)

    output_folder= "logs"

     # '/var/www/html/aish/api-publish/tools/yang_gnmi_validator'
    # Old:
    # base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

    # New:
    base_dir = os.path.dirname(os.path.abspath(__file__))

    #'/var/www/html/aish/api-publish/tools/yang_gnmi_validator/logs'
    logs_dir = os.path.join(base_dir, output_folder)

    os.makedirs(logs_dir, exist_ok=True)


    output_path = os.path.join( logs_dir , filename_result + "_testcase_report" + ".html")
    with open(output_path, "w", encoding="utf-8") as out_file:
        out_file.write(template_html)

    print(f"Generated HTML report at: {os.path.abspath(output_path)}")

    
import os
import sys
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_test_result.py <json_file1> <json_file2> ... OR <json_directory>")
        sys.exit(1)

    input_paths = sys.argv[1:]

    # If a single argument is passed and it's a directory
    if len(input_paths) == 1 and os.path.isdir(input_paths[0]):
        input_path = input_paths[0]
        print(f"📁 Handling directory: {input_path}")
        filename_result = os.path.basename(os.path.normpath(input_path))
        data = parse_log_files_from_directory(input_path)
        dict_data_handling(data, filename_result)
        return

    # Handle multiple JSON files
    combined_data = []
    valid_files = []

    for path in input_paths:
        if os.path.isfile(path) and path.endswith("_result.json"):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        combined_data.extend(data)
                    elif isinstance(data, dict):
                        combined_data.append(data)
                    else:
                        print(f"⚠️ Skipping invalid format in: {path}")
                valid_files.append(path)
            except Exception as e:
                print(f"❌ Error reading {path}: {e}")
                sys.exit(1)
        else:
            print(f"❌ Invalid input: {path} (must be a .json file ending with _result.json)")
            sys.exit(1)

    if not valid_files:
        print("❌ No valid JSON files found.")
        sys.exit(1)

    # Write combined output
    with open("combined_data.json", 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=4)
    print("✅ Combined data saved to combined_data.json")

    # Create prefix from all file names
    filename_result = ""
    filename_result = "_".join([
    os.path.splitext(os.path.basename(p))[0].replace("_result", "") 
    for p in valid_files
    ])

    print(f"✅ Prefix used: {filename_result}")

    dict_data_handling(combined_data, filename_result)

if __name__ == "__main__":
    main()
