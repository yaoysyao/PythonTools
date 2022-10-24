import setuptools  # 导入setuptools打包工具
from pathlib import Path

cwd = Path(__file__).parent
try:
    long_description = (cwd / "README.MD").read_text(encoding='utf8')
except:
    long_description = ''
"""
打包命令: python setup.py sdist
twine upload dist/yaoys-python-tool-0.0.36.tar.gz
"""

setuptools.setup(
    name="yaoys-python-tool",  # pip库名称
    version="0.0.49",  # 包版本号，便于维护版本
    author="YaoYuanshuai",  # 作者
    author_email="yys9508@qq.com",  # 联系方式
    description="python工具类",  # 包的简述
    # long_description="此工具类致力于封装一些常用的python代码，目前支持log日志，progress进度条，mysql数据库操作，雪花算法唯一id，时间工具类等方法",  # 包的详细介绍，一般在README.md文件内
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yaoysyao/PythonTools.git",  # 项目地址
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # 对python的最低版本要求
    python_requires='>=3.6',
    install_requires=['pymysql',
                      'dbutils>=3.0.2',
                      'sklearn',
                      'numpy>=1.20.3',
                      'threadpoolctl>=2.0.0',
                      'joblib>=0.11',
                      'colorlog>=4.0.0'],
    # data_files=list(str(filepath))
    include_package_data=True,
    exclude_package_date={'': ['.gitignore']}
)
