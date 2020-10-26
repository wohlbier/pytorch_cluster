#!/bin/bash

P=./build/lib.linux-x86_64-3.7/torch_cluster
FILES="_fps.so
       _graclus.so
       _grid.so
       _knn.so
       _nearest.so
       _radius.so
       _rw.so
       _sampler.so
       _version.so"

OPT="/DATA/SDH/packages/spack/opt/spack/linux-ubuntu18.04-broadwell/clang-9.0.1/llvm-9.0.1-mupwetisd3upwdfojfn6ztdmxmgfy3kz/bin/opt -load /home/jgwohlbier/DSSoC/DASH/TraceAtlas/build/lib/AtlasPasses.so -EncodedTrace"
COMP="/DATA/SDH/packages/spack/opt/spack/linux-ubuntu18.04-broadwell/clang-9.0.1/llvm-9.0.1-mupwetisd3upwdfojfn6ztdmxmgfy3kz/bin/clang++ -O2 -g -DNDEBUG -pthread -shared -B /DATA/SDH/packages/anaconda3/envs/dash_gs_env/compiler_compat -fuse-ld=lld -fPIC"
LINK="-L/DATA/SDH/packages/anaconda3/envs/dash_gs_env/lib -Wl,-rpath=/DATA/SDH/packages/anaconda3/envs/dash_gs_env/lib -Wl,--no-as-needed -Wl,--sysroot=/ -L/DATA/SDH/packages/anaconda3/envs/dash_gs_env/lib/python3.7/site-packages/torch/lib -lc10 -ltorch -ltorch_cpu -ltorch_python"
LINK="${LINK} -L/home/jgwohlbier/DSSoC/DASH/TraceAtlas/build/lib  -Wl,-rpath,/home/jgwohlbier/DSSoC/DASH/TraceAtlas/build/lib -lAtlasBackend -lz"

for f in ${FILES}; do
    cmd="${OPT} ${P}/${f} -o ${P}/${f}.opt.bc"
    echo "${cmd}"
    eval ${cmd}

    cmd="${COMP} ${P}/${f}.opt.bc -o ${P}/${f} ${LINK}"
    #cmd="${COMP} ${P}/${f}.opt.bc -o ${P}/${f}.opt.bc.so ${LINK}"
    echo "${cmd}"
    eval ${cmd}
done
