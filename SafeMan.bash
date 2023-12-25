if [ -n "$1" ]
then
    >&2 echo "SafeMan does not accept additional arguments."
else
    python3 /usr/local/lib/safeman/src/app_window.py
fi