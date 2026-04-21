import re

# 测试换行符处理
test_cases = [
    '1\n2\n3\n4\n5',
    '1,2,3,4,5',
    '1 2 3 4 5',
    '1\n2,3 4\n5'
]

for i, input_str in enumerate(test_cases):
    print(f"测试用例 {i+1}:")
    print(f"输入: {repr(input_str)}")
    processed_str = re.sub(r'[\s,\n\r]+', ',', input_str.strip())
    print(f"处理后: {repr(processed_str)}")
    print(f"分割后: {processed_str.split(',')}")
    print()
