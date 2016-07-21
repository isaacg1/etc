echo "overall start"
while true
do
    echo "round start"
    python main.py 2>main.err
    echo "round end"
    sleep 1
done
