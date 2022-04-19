import logging
import re
import constants

__c_like_function_scope_regex__ = r"(public|private|static|protected|abstract|native|synchronized)?"
__llvm_like_function_scope_regex__ = r"(def|fn|fun)"
__function_return_regex__ = r"([a-zA-Z0-9\[\]\<\>\.\_\?\, ]*)"
__function_name_regex__ = r"([a-zA-Z0-9_]+)"
__function_arguments_regex__ = r"\([a-zA-Z0-9<>\[\]\.\_\-\?\&\*\, \r\n]*\)[ \t\r\n]*"
__function_body_regex__ = r"([{:])"
__one_or_more_spaces__ = r" +"
__zero_or_more_spaces__ = r" *"

# c_like_function_regex = "(public|private|static|protected|abstract|native|synchronized) +([a-zA-Z0-9\[\]<>._?, ]+) +([a-zA-Z0-9_]+) *\([a-zA-Z0-9<>\[\]._?, \n]*\) *([a-zA-Z0-9_ ,\n]*) +[\t\r\n]*\{"

llvm_like_regex = __llvm_like_function_scope_regex__ + __one_or_more_spaces__ + __function_name_regex__ + __zero_or_more_spaces__ + \
                __function_arguments_regex__ + __zero_or_more_spaces__ + __function_body_regex__
llvm_like_regex_function_parameter = 1

c_like_regex = __c_like_function_scope_regex__ + __one_or_more_spaces__ + __function_return_regex__ + __one_or_more_spaces__ + \
                __function_name_regex__ + __zero_or_more_spaces__ + __function_arguments_regex__ + __zero_or_more_spaces__ + \
                __function_body_regex__

c_like_regex_function_parameter = 2

def get_long_method_names_c_like(file_contents):
    method_names = []
    try:
        matches = re.findall(c_like_regex, file_contents)
        logging.info(f"{len(matches)} functions")
        for match in matches:
            if len(match[c_like_regex_function_parameter]) > constants.LONG_FUNCTION_LENGTH:
                method_names.append(match[c_like_regex_function_parameter])
    except Exception as e:
        logging.error(f"Something went wrong with the c-like regex due to {e}")
    return method_names


def get_long_method_names_llvm_like(file_contents):
    method_names = []
    try:
        matches = re.findall(llvm_like_regex, file_contents)
        logging.info(f"{len(matches)} function")
        for match in matches:
            if len(match[llvm_like_regex_function_parameter]) > constants.LONG_FUNCTION_LENGTH:
                method_names.append(match[llvm_like_regex_function_parameter])
    except Exception as e:
        logging.error(f"Something went wrong with the llvm-like regex due to {e}")
    return method_names






__test_cases__ = (
    "def python_public_function(someArg):",
    "def __python_private_function__(someArg):",
    "pub async fn rust_function(&mut arg) {",
    "fun kotlinFunction(Args some_args) :",
    "public static[] void javaFunction1(String args[]) {",
    "private interface CsharpFunction(<T> type1, <T>type2) {"
)

def run_tests():
    all_llvm_matches = []
    all_c_matches = []
    for test_case in __test_cases__:
        llvm_matches = re.findall(llvm_like_regex, test_case)
        for match in llvm_matches:
            all_llvm_matches.append(match[1])
        c_matches = re.findall(c_like_regex, test_case)
        for match in c_matches:
            all_c_matches.append(match[2])
    print(f"LLVM-like matches: {all_llvm_matches}")
    print(f"C-like matches: {all_c_matches}")

if __name__ == "__main__":
    run_tests()