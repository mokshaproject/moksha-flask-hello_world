from setuptools import setup
setup(
    name='tutorial',
    install_requires=[
            "flask",
            "moksha.wsgi",
            "moksha.hub",
            ],
    entry_points="""
    [moksha.producer]
    hello = tutorial:HelloWorldProducer
    """,
)
