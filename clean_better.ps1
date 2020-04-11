New-Item -Path . -Name "addresses_cleaned.txt" -ItemType "file" -Force;
foreach($line in Get-Content .\addresses_raw.txt){ 
  $line = $line -replace "\s+"," "
  $line = $line.ToUpper()
  $line = $line -replace "LOT\s\d+\s",""
  $line = $line.replace('"','')
  $line = $line -replace '^(\d+)-(\d+)','$1'
  $line = $line -replace '(\d+)-(\d+)','$1'
  $line = $line -replace 'HOUSE\s\d+',''
  $line = $line -replace "^LEVEL\s\d+\s",""
  $line = $line -replace "IN FRONT OF THE ",""
  $line = $line -replace "^UNIT\s\d+\s",""
  $line = $line -replace "^U\s\d+\s",""
  $line = $line -replace "^ROOM\s\d+\s",""
  $line = $line -replace "\sBUILDING\s"," "
  $line = $line -replace "[/,.]",""
  $line = $line.replace("`t","")
  $line = $line -replace "\sARC\s"," ARCADE "
  $line = $line -replace "\sESP\s"," ESPLANADE "
  $line = $line -replace "\sCV\s"," COVE "
  $line = $line -replace "\sCRES\s"," CRESCENT "
  $line = $line -replace "\sCR\s"," CRESCENT "
  $line = $line -replace "\sRD\s"," ROAD "
  $line = $line -replace "\sAVE\s"," AVENUE "
  $line = $line -replace "\sPL\s"," PLACE "
  $line = $line -replace "\sCRT\s"," COURT "
  $line = $line -replace "\sCT\s"," COURT "
  $line = $line -replace "\sDR\s"," DRIVE "
  $line = $line -replace "\sTCE\s"," TERRACE "
  $line = $line -replace "\sPDE\s"," PARADE "
  $line = $line -replace "\sCCT\s"," CIRCUIT "
  $line = $line -replace "\sCRST\s"," CREST "
  $line = $line -replace "\sLA\s"," LANE "
  $line = $line -replace "\sWAY\s"," WAY "
  $line = $line -replace "\sGDN\s"," GARDENS "
  $line = $line -replace "\sGDNS\s"," GARDENS "
  $line = $line -replace "\sCL\s"," CLOSE "
  $line = $line -replace "\w\sCCS\s"," CIRCUS "
  $line = $line -replace "\w\sCCL\s"," CIRCLE "
  $line = $line -replace "\w\sBVD\s"," BOULEVARD "
  $line = $line -replace "\w\sBLVD\s"," BOULEVARD "
  $line = $line -replace "\w\sSTREETS\s"," STREET "
  $line = $line -replace "\w\sST\s"," STREET "
  $line = $line -replace "\sMT\s"," MOUNT "
  $line = $line -replace "\sRD\s"," ROAD "
  $line = $line -replace "\sHWY\s"," HIGHWAY "
  
  $address = [regex]::Match($line,'(\d*\w*)\s(\w*\s*\w*).(ROAD|STREET|BOULEVARD|CIRCLE|CIRCUS|CLOSE|GARDENS|LANE|CIRCUIT|PARADE|HIGHWAY|MALL|BROADWAY|TERRACE|DRIVE|COURT|PLACE|AVENUE|CRESCENT)(.*)(NSW|QLD|SA|TAS|ACT|NT|VIC|WA).(\d{4})$').captures.groups
  if ($address.value.length -gt 0)
  {
    write-host("ok")
    $st_num = 
    if ($st_num-is [int]) {$st_num=''}
    write-host("1- "+$address[1].value)
    write-host("2- "+$address[2].value)
    write-host("3- "+$address[3].value)
    write-host("4- "+$address[4].value)
    write-host("5- "+$address[5].value)
    write-host("6- "+$address[6].value)
    $line=$address[1].value.Trim() + " " + $address[2].value.Trim() + " " + $address[3].value.Trim() + " " + $address[4].value.Trim()+ " " + $address[5].value.Trim()+ " " + $address[6].value.Trim()
  }
  Else
    {
     $line = $line.Trim();
     $address = [regex]::Match($line,'(\w+)\s(ROAD|STREET|BOULEVARD|CIRCLE|CIRCUS|CLOSE|GARDENS|LANE|CIRCUIT|PARADE|HIGHWAY|MALL|BROADWAY|TERRACE|QUAYS|DRIVE|COURT|PLACE|AVENUE|CRESCENT)(.*)(NSW|QLD|SA|TAS|ACT|NT|VIC|WA).(\d{4})$').captures.groups;
    if ($address.value.length -gt 0)
       {
          write-host('no street no');
	  write-host($line)
          write-host("1- " + $address[1].value)
          write-host("2- " + $address[2].value)
          write-host("3- " +$address[3].value)
          write-host("4- " +$address[4].value)
          write-host("5- " +$address[5].value)
          $line=$address[1].value.Trim() + " " + $address[2].value.Trim() + " " + $address[3].value.Trim() + " " + $address[4].value.Trim() + " " + $address[5].value.Trim()
       }
     Else
       { 
          if ($address.value.length -gt 0) 
             {
                $address = [regex]::Match($line,'(\w+)(\s)(NSW|QLD|SA|TAS|ACT|NT|VIC|WA).(\d{4})$').captures.groups;
                write-host('no street name')
                write-host($line)
                write-host("1- " + $address[1].value)
                write-host("2- " + $address[2].value)
                write-host("3- " +$address[3].value)
                $line=$address[1].value.Trim() + " " + $address[2].value.Trim() + " " + $address[3].value.Trim()
             }
       }
}
  echo $line| Out-File -FilePath addresses_cleaned.txt -Append
};
$file="addresses_cleaned.txt";
(Get-Content $file | Select-Object -Skip 1) | Set-Content $file


