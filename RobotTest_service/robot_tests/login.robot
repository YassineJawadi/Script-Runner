*** Settings ***
Library    OperatingSystem

*** Test Cases ***
Passing Example
    Log    Hello Robot Framework!

Failing Example
    Fail    This is an intentional failure
