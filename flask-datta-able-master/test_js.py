import re

with open('apps/templates/product/commission.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取 JavaScript 部分
match = re.search(r'<script>(.*?)</script>', content, re.DOTALL)
if match:
    js_code = match.group(1)
    
    # 检查括号匹配
    open_braces = js_code.count('{')
    close_braces = js_code.count('}')
    open_parens = js_code.count('(')
    close_parens = js_code.count(')')
    
    print(f'Open braces {{: {open_braces}')
    print(f'Close braces }}: {close_braces}')
    print(f'Open parens (: {open_parens}')
    print(f'Close parens ): {close_parens}')
    
    if open_braces != close_braces:
        print(f'ERROR: Braces mismatch! Diff: {open_braces - close_braces}')
    else:
        print('Braces: OK')
        
    if open_parens != close_parens:
        print(f'ERROR: Parentheses mismatch! Diff: {open_parens - close_parens}')
    else:
        print('Parentheses: OK')
    
    # 保存到临时文件用于检查
    with open('test_commission.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
    print('\nJavaScript code saved to test_commission.js')
