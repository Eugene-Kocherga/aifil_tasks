
class OptionInfo:
    def __init__(self, name, parser, required):
        self.name = name
        self.parser = parser
        self.required = required
        self.is_flag = parser is None

    def from_string(self, text):
        if self.is_flag:
            return True
        return self.parser(text)


def get_one_opt(arg, option_info_dict):
    dividers = '= '
    arg_splitted = [arg]
    for d in dividers:
        if d in arg:
            arg_splitted = arg.split(d)
            break
    arg_cleared = [t for t in arg_splitted if t]
    if len(arg_cleared) == 0:
        return
    elif len(arg_cleared) > 2:
        raise Exception('Input error')
    arg_name = arg_cleared[0]
    if arg_name not in option_info_dict:
        raise Exception('Unknown option: ' + arg_name)
    elif option_info_dict[arg_name].is_flag:
        if len(arg_cleared) != 1:
            raise Exception('Value for boolean option: ' + arg_name)
        return (arg_name, True)
    else:
        if len(arg_cleared) != 2:
            raise Exception('Missing value for option: ' + arg_name)
        return (arg_name, option_info_dict[arg_name].from_string(arg_cleared[1]))

def prepare(text):
    whitespaces = ' \t\n\r'
    for ws in whitespaces:
        text = text.replace(ws, ' ')
    return text

def check_fullness(args, option_info_dict):
    missed = list()
    for arg_name, arg_info in option_info_dict.items():
        if arg_info.required and arg_name not in args:
            missed.append(arg_name)
    if missed:
        raise Exception('Missed required options:' + ' '.join(missed))

def show_help(option_info_dict):
    for option_info in option_info_dict.values():
        line = '--' + option_info.name
        if not option_info.is_flag:
            line += '=' + str(option_info.parser)
        if not option_info.required:
            line = '[' + line + ']'
        print(line)

def getopt(argv, option_info_dict):
    argv = prepare(argv)
    result = dict()
    for arg in argv.split('--'):
        r = get_one_opt(arg, option_info_dict)
        if r:
            result[r[0]] = r[1]
    if 'help' in result:
        show_help(option_info_dict)
    check_fullness(result, option_info_dict)
    return result

if __name__ == "__main__":
    option_info_list = [OptionInfo('my_str_option', str, True),
                        OptionInfo('my_int_option', int, True),
                        OptionInfo('my_float_option', float, False),
                        OptionInfo('my_boolean_option', None, False),
                        OptionInfo('help', None, False)]
    option_info_dict = {oi.name: oi for oi in option_info_list}

    test_case = """--my_str_option test --my_int_option=4
    --my_float_option -3.2"""
    print(getopt(test_case, option_info_dict))

    test_case = """--my_str_option test --my_int_option=4
    --my_float_option -3.2 --help"""
    print(getopt(test_case, option_info_dict))