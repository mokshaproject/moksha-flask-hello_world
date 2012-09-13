from setuptools import setup
setup(
    name='tutorial',
    entry_points="""
    [moksha.producer]
    hello = tutorial:HelloWorldProducer
    """,
)
