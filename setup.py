import os
import os.path as osp
import glob
from setuptools import setup, find_packages

import torch
from torch.utils.cpp_extension import BuildExtension
from torch.utils.cpp_extension import CppExtension, CUDAExtension, CUDA_HOME

WITH_CUDA = torch.cuda.is_available() and CUDA_HOME is not None
if os.getenv('FORCE_CUDA', '0') == '1':
    WITH_CUDA = True
if os.getenv('FORCE_CPU', '0') == '1':
    WITH_CUDA = False

BUILD_DOCS = os.getenv('BUILD_DOCS', '0') == '1'


def get_extensions():
    Extension = CppExtension
    define_macros = []
    extra_compile_args = {'cxx': []}
    extra_link_args = []

    #extra_compile_args['cxx'] = ['-flto', '-fPIC']
    #extra_link_args = ['-fuse-ld=lld', '-Wl,--plugin-opt=emit-llvm',
    #                          '-Wl,--plugin-opt=save-temps']

    if WITH_CUDA:
        Extension = CUDAExtension
        define_macros += [('WITH_CUDA', None)]
        nvcc_flags = os.getenv('NVCC_FLAGS', '')
        nvcc_flags = [] if nvcc_flags == '' else nvcc_flags.split(' ')
        nvcc_flags += ['-arch=sm_35', '--expt-relaxed-constexpr']
        extra_compile_args['nvcc'] = nvcc_flags

    extensions_dir = osp.join(osp.dirname(osp.abspath(__file__)), 'csrc')
    main_files = glob.glob(osp.join(extensions_dir, '*.cpp'))
    extensions = []
    for main in main_files:
        name = main.split(os.sep)[-1][:-4]

        sources = [main]

        path = osp.join(extensions_dir, 'cpu', f'{name}_cpu.cpp')
        if osp.exists(path):
            sources += [path]

        path = osp.join(extensions_dir, 'cuda', f'{name}_cuda.cu')
        if WITH_CUDA and osp.exists(path):
            sources += [path]

        extension = Extension(
            'torch_cluster._' + name,
            sources,
            include_dirs=[extensions_dir],
            define_macros=define_macros,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        )
        extensions += [extension]

    return extensions


install_requires = []
setup_requires = ['pytest-runner']
tests_require = ['pytest', 'pytest-cov', 'scipy']

setup(
    name='torch_cluster',
    version='1.5.7',
    author='Matthias Fey',
    author_email='matthias.fey@tu-dortmund.de',
    url='https://github.com/rusty1s/pytorch_cluster',
    description=('PyTorch Extension Library of Optimized Graph Cluster '
                 'Algorithms'),
    keywords=[
        'pytorch',
        'geometric-deep-learning',
        'graph-neural-networks',
        'cluster-algorithms',
    ],
    license='MIT',
    python_requires='>=3.6',
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    ext_modules=get_extensions() if not BUILD_DOCS else [],
    cmdclass={
        'build_ext':
        BuildExtension.with_options(no_python_abi_suffix=True, use_ninja=False)
    },
    packages=find_packages(),
)
