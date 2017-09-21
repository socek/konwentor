from {{settings["package:name"]}}.application.init import main


def setup(env):
    request = env['request']
    env['driver'] = request.driver
    env['db'] = env['request'].db
    env['main'] = main
