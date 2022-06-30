import setuptools  # 导入setuptools打包工具

# cwd = Path(__file__).parent
# filepath = "README.md"

setuptools.setup(
    name="yaoys-python-tool",  # 用自己的名替换其中的YOUR_USERNAME_
    version="0.0.28",  # 包版本号，便于维护版本
    author="YaoYuanshuai",  # 作者，可以写自己的姓名
    author_email="yaoys@mail.imu.edu.cn",  # 作者联系方式，可写自己的邮箱地址
    description="python工具类",  # 包的简述
    long_description="open(filepath, encoding='utf-8').read()",  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="https://gitee.com/yys518/PythonTools.git",  # 自己项目地址，比如github的项目地址
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
                      'joblib>=0.11']
    # data_files=list(str(filepath))
    # include_package_data=True,
    # exclude_package_date={'': ['.gitignore']}
)
