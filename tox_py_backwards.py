from tox import hookimpl


@hookimpl
def tox_addoption(parser):
    parser.add_testenv_attribute(
        name='py_backwards',
        type="bool",
        default=False,
        help='compile code with py-backwards before running tests')
    parser.add_testenv_attribute(
        name='py_backwards_inputs',
        type="line-list",
        default=(),
        help='list of files/dirs to be converted by py-backwards before running tests',
    )


script = '''
VERSION=$(python -c 'import sys; print("{{}}.{{}}".format(*sys.version_info[:2]))')
rm -rf .tox/py_backwards/
mkdir .tox/py_backwards/
cp -a * .tox/py_backwards/
cd .tox/py_backwards/
{0}
{1}
rm -rf .tox/py_backwards/
'''
convert_command = 'py-backwards -i {0} -o {0} -t $VERSION'


@hookimpl
def tox_runtest_pre(venv):
    if venv.envconfig.py_backwards:
        convert = '\n'.join(convert_command.format(file)
                            for file in venv.envconfig.py_backwards_inputs)
        original_command = '\n'.join(' '.join(command)
                                     for command in venv.envconfig.commands)
        venv.envconfig.commands = [['sh', '-c',
                                    script.format(convert, original_command)]]
        venv.envconfig.whitelist_externals.append('sh')
