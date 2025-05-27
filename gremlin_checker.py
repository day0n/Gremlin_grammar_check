import sys
import os

# 添加Gremlin目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'Gremlin'))

from antlr4 import *
from GremlinLexer import GremlinLexer
from GremlinParser import GremlinParser
from GremlinListener import GremlinListener
from antlr4.error.ErrorListener import ErrorListener

class GremlinErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []
    
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(f"第 {line} 行, 第 {column} 列: {msg}")

def check_gremlin_syntax(query):
    # 创建输入流
    input_stream = InputStream(query)
    
    # 创建词法分析器
    lexer = GremlinLexer(input_stream)
    lexer.removeErrorListeners()
    lexer_error_listener = GremlinErrorListener()
    lexer.addErrorListener(lexer_error_listener)
    
    # 创建词法符号流
    token_stream = CommonTokenStream(lexer)
    
    # 创建语法分析器
    parser = GremlinParser(token_stream)
    parser.removeErrorListeners()
    parser_error_listener = GremlinErrorListener()
    parser.addErrorListener(parser_error_listener)
    
    # 解析  
    try:
        parser.queryList()
        if lexer_error_listener.errors or parser_error_listener.errors:
            return False, lexer_error_listener.errors + parser_error_listener.errors
        return True, []
    except Exception as e:
        return False, [str(e)]

def main():

    print("请输入Gremlin查询（输入完成后按Ctrl+D结束）：")
    query = sys.stdin.read()
    
    is_valid, errors = check_gremlin_syntax(query)
    
    if is_valid:
        print("语法正确！")
    else:
        print("语法错误：")
        for error in errors:
            print(f"- {error}")

if __name__ == "__main__":
    main() 