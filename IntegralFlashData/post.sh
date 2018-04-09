for impa in 6 12 24 36 48
do
 impad="ignMPoleA-"$impa"e5"
 pushd $impad
 cp ../*.py .
 rm *_ordered.dat
 nohup python prepost.py $impa >/dev/null &
 nohup python post.py $impa >/dev/null &
 popd
done
