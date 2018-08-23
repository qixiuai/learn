MATLAB="/home/guo/AwareTech/software/matlab"
Arch=glnxa64
ENTRYPOINT=mexFunction
MAPFILE=$ENTRYPOINT'.map'
PREFDIR="/home/guo/.matlab/R2018a"
OPTSFILE_NAME="./setEnv.sh"
. $OPTSFILE_NAME
COMPILER=$CC
. $OPTSFILE_NAME
echo "# Make settings for kalman02" > kalman02_mex.mki
echo "CC=$CC" >> kalman02_mex.mki
echo "CFLAGS=$CFLAGS" >> kalman02_mex.mki
echo "CLIBS=$CLIBS" >> kalman02_mex.mki
echo "COPTIMFLAGS=$COPTIMFLAGS" >> kalman02_mex.mki
echo "CDEBUGFLAGS=$CDEBUGFLAGS" >> kalman02_mex.mki
echo "CXX=$CXX" >> kalman02_mex.mki
echo "CXXFLAGS=$CXXFLAGS" >> kalman02_mex.mki
echo "CXXLIBS=$CXXLIBS" >> kalman02_mex.mki
echo "CXXOPTIMFLAGS=$CXXOPTIMFLAGS" >> kalman02_mex.mki
echo "CXXDEBUGFLAGS=$CXXDEBUGFLAGS" >> kalman02_mex.mki
echo "LDFLAGS=$LDFLAGS" >> kalman02_mex.mki
echo "LDOPTIMFLAGS=$LDOPTIMFLAGS" >> kalman02_mex.mki
echo "LDDEBUGFLAGS=$LDDEBUGFLAGS" >> kalman02_mex.mki
echo "Arch=$Arch" >> kalman02_mex.mki
echo "LD=$LD" >> kalman02_mex.mki
echo OMPFLAGS= >> kalman02_mex.mki
echo OMPLINKFLAGS= >> kalman02_mex.mki
echo "EMC_COMPILER=gcc" >> kalman02_mex.mki
echo "EMC_CONFIG=optim" >> kalman02_mex.mki
"/home/guo/AwareTech/software/matlab/bin/glnxa64/gmake" -j 1 -B -f kalman02_mex.mk
