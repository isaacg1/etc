echo "overall start"
while true
do
    echo "round start"
    echo "round started" >> .monitor
    date >> .monitor
    python main.py 2>main.err
    echo "round end"
    echo "round end" >> .monitor
    date >> .monitor
    sleep 2
done
