import math
TITLE1="计算器"
TITLE2="科学计算器"

SUM_WIDGET1=(("7","8","9","+"),
             ("4","5","6","-"),
             ("1","2","3","x"),
             ("0",".","=","÷"))
SUM_WIDGET2=(("sin","π","7","8","9","+"),
             ("cos","x²","4","5","6","-"),
             ("tan","x^y","1","2","3","x"),
             ("lg","√x","0",".","%","÷"),
             ("ln","x!","e","="))
SUM_WIDGET2_OPERATOR_RE=("(\d*?)!", "√([0-9.]*)", "([0-9.]*)\^\(2\)", "([0-9.]*)\^\(([0-9.]*)\)",
                                   "sin\(([0-9.]*)\)", "cos\(([0-9.]*)\)", "tan\(([0-9.]*)\)", "ln\(([0-9.]*)\)",
                                   "lg\(([0-9.]*)\)")
SUM_WIDGET2_OPERATOR_LEFT=("", "√", "", None, "sin(", "cos(", "tan(", "ln(", "lg(")
SUM_WIDGET2_OPERATOR_RIGHT=("!", "", "^(2)", None, ")", ")", ")", ")", ")")
SUM_WIDGET2_FUNC=(math.factorial, math.sqrt, math.pow, None, math.sin, math.cos,
                  math.tan, math.log, math.log10)
SUM_WIDGET1_ENTRY_FONT=("微软雅黑",20)
SUM_WIDGET1_BUTTON_FONT=("微软雅黑",15)
SUM_WIDGET2_ENTRY_FONT=("微软雅黑",20)
SUM_WIDGET2_BUTTON_FONT=("微软雅黑",15)