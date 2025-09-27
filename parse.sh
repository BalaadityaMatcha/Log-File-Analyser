take=$1
if [[ -s "$take" ]]; then
tr -d "\r" < "$take" | sed -f update.sed | awk '
BEGIN{
    FS=" ";
}
{
	if($0 ~ /^\[[A-Z][a-z]{2} [A-Z][a-z]{2} [0-1][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9] [0-9]{4,}\] \[(notice|error)\] .*$/){
        if($7 !~ /^E[1-6]$/){
            $7=""
        }
        event[NR]=$7
    }
    else{
        ex=1
        exit 1
    }
}
END{
    if(ex!=1){
        for(i=1;i<NR+1;i++){
            print event[i]
        }
    }
}' > events 
    if (($? != 0)); then
        echo "File not eligible for converting into csv"
        exit 1
    else
        paste -d"," <(tr -d "\r" < "$take") events | sed -e 's/\] /,/g' -e 's/\[//g' -e 's/\(client .*\),D/[\1] D/' > upfile
        sed -f reupdate.sed upfile | awk 'BEGIN{ FS=",";OFS=","} {print $4}' | paste -d"," upfile - > final.csv
    fi
    rm events upfile
else
    echo "Empty file!"
fi