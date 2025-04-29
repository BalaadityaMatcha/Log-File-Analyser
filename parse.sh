take=$1
file=""
tr -d "\r" < "$take" > file
if [[ -s file ]]; then
sed -f update.sed file | awk '{print $0;}' > upfile
awk 'BEGIN{
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
}' upfile > events 
    if (($? != 0)); then
        echo "File not eligible for converting into csv"
        exit 1
    else
        paste -d"," file events | sed -e 's/\] /,/g' -e 's/\[//g' -e 's/\(client .*\),D/[\1] D/' > upfile
        sed -f reupdate.sed upfile | awk 'BEGIN{ FS=",";OFS=","} {print $4}' > events
        paste -d"," upfile events > final.csv
    fi
    rm events upfile file
else
    echo "Empty file!"
fi