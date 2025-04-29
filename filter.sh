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
    awk -v ts1="$ts1" -v ts2="$ts2" 'BEGIN{FS=",";OFS=",";}
        {cmd = "date -d \""$1"\" +%s"
        cmd | getline ts
        close(cmd)
        if (( ts > ts2 )); then
            exit
        fi
        if (( ts >= ts1 )); then
            print ts,$0
        fi }' "Orgsorted.csv" | sort -t"," -k1,1n | cut -d"," -f2- > sorted.csv
echo "Done filtering"
fi