import importlib.util
import sys


def dynamic_import_function(module_path, function_name):
    """
    动态导入指定路径的模块，并获取其中的函数。
    :param module_path: 目标模块的文件路径
    :param function_name: 要获取的函数名
    :return: 函数对象
    """

    # 生成模块规范
    spec = importlib.util.spec_from_file_location('dynamic_module', module_path)
    module = importlib.util.module_from_spec(spec)

    # 执行模块，加载代码
    sys.modules['dynamic_module'] = module
    spec.loader.exec_module(module)

    # 获取指定函数
    func = getattr(module, function_name)
    return func