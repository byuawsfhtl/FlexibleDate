from FlexibleDate.FlexibleDate import createFlexibleDate

def runTestCases() -> None:
    """Runs the test cases for FlexibleDate
    """    
    inputToExpectedOutput = {
        '2024-08-06': '2024-8-6',
        '06/08/2024': '2024-6-8',
        '08-06-2024': '2024-8-6',
        '2024.08.06': '2024-8-6',
        '06-Aug-2024': '2024-8-6',
        'August 6, 2024': '2024-8-6',
        '20240806': '2024',
        '06-08-24': '2024-6-8',
        '08/06/24': '2024-8-6',
        '06.Aug.2024': '2024-8-6',
        '2024/Aug/06': '2024-8-6',
        'Aug 6, 2024': '2024-8-6',
        '2024 08 06': '2024-8-6',
        '06_August_2024': '2024-8-6',
        'August-06-2024': '2024-8-6',
        '24-08-06': '2006-8-24',
        '2024/08/06': '2024-8-6',
        '06-08-2024 15:30:00': '2024-6-8',
        '2024-08-06T15:30:00Z': '2024-8-6',
        '06/08/2024 3:30 PM': '2024-6-8',
        '06-Aug-24': '2024-8-6',
        '2024-Aug-06': '2024-8-6',
        '6th August 2024': '2024-8-6',
        '2024/06/August': '2024-8-6',
        '06 Aug 2024': '2024-8-6',
        'Aug 06, 2024': '2024-8-6',
        '06-08-2024 15:30': '2024-6-8',
        '2024-08-06 15:30': '2024-8-6',
        '06/08/2024 15:30': '2024-6-8',
        '2024-August-06': '2024-8-6',
        'august 6 2024': '2024-8-6',
        'aug': 'None-8',
        'sep 21 pengu theodore banana trashpanda': 'None-9-21',
        'sep 21 pengu theodore banana trashpanda 1234': '1234-9-21',
        'sep 21': 'None-9-21',
        '30': '30',
        '120': '120',
        '1200': '1200',
        '1': '1',
        '32': '32',
        '0032': '32',
        '-1100': '-1100',
        '-1100 Jan 1': '1100-1-1',
        '-9000': '-9000',
        '': 'None',
        '1034-12-3': '1034-12-3',
        '102-12-3': '102-12-3',
        '100-12-3': '100-12-3',
        '99-12-3': '1999-12-3',
        '3 99 12': 'None',
        '2 1000 3': '1000',
        '2 Sep May 1999': '1999',
        None: 'None',
    }

    for input, expectedOutput in inputToExpectedOutput.items():
        actualOutput = createFlexibleDate(input)
        if f'{actualOutput}' == expectedOutput:
            continue
        print('Actual output and expected output do not match:')
        print(f'{input = }')
        print(f'{expectedOutput = }')
        print(f'actualOutput = {actualOutput}')
        print()