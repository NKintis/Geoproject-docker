#!/bin/bash

echo "Starting the startup.sh script..."

echo "Starting image_download_input.py..."

python image_download_input.py &

bg_process_pid=$!

wait $bg_process_pid

echo "image_download_input.py completed successfully. Starting s2_preprocess.py..."

python s2_preprocess.py 

s2_preprocess_exit=$!

wait $s2_preprocess_exit

echo "s2_preprocess.py completed successfully."


if echo "Running" > /shared_files/jupyterlab_status.txt; then
    echo "File written successfully"
else
    echo "Error writing to file"
fi

nohup jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' 

jupyter_lab_pid=$!





