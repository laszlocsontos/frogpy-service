#!/bin/sh

build_dir=build
target_name=frogpy-service
target_dir=$build_dir/$target_name

if [ -d $build_dir ]; then
  rm -r $build_dir
fi

mkdir -p $target_dir

cp -R env $target_dir
cp -R frogpy $target_dir
cp requirements.txt $target_dir
cp init-venv.sh $target_dir
cp runserver.py $target_dir
cp *-server.sh $target_dir

cd $build_dir
zip -r $target_name.zip $target_name
cd ..
