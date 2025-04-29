BEGIN{
    FS=",";
    OFS="</th><th>";
    print "<thead><tr><th>S.No","Time","Level","Error","Event ID","Event Template</th><tr></thead>"
    OFS="</td><td>";
}
{
    i=i+1
    $5=$5 "</td></tr>"
    print "<tr><td>"i, $0
}