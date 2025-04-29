file="$1"
date1="$2"
date2="$3"
if [[ $date1 == '0' || $date2 == '0' ]]; then
   awk 'BEGIN{FS=",";OFS=",";}
    {cmd = "date -d \""$1"\" +%s"
    cmd | getline ts
    close(cmd)
    print ts, $0}' "$file" | sort -t"," -k1,1n | cut -d"," -f2- > Orgsorted.csv
    exit 0
else
    ts1=$(date -d "$date1" +%s)
    ts2=$(date -d "$date2" +%s)
    > filtered.csv
    while read -r line; do
        tm=$(echo "$line" | cut -d"," -f1)
        ts=$(date -d "$tm" +%s)
        if (( ts > ts2 )); then
            break
        fi
        if (( ts >= ts1 )); then
            echo "$line" >> filtered.csv
        fi
    done < "Orgsorted.csv"
    awk 'BEGIN{FS=",";OFS=",";}
        {cmd = "date -d \""$1"\" +%s"
        cmd | getline ts
        close(cmd)
        print ts, $0}' filtered.csv | sort -t"," -k1,1n | cut -d"," -f2- > sorted.csv
rm filtered.csv
echo "Done filtering"
fi