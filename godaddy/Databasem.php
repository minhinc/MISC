<?php
class Databasec{
public $link="";
public function __construct() {
$dbname="trackweb";
//echo "<p>__construct<br></p>";
//$this->link=mysqli_connect('localhost','minhinc','pinku76minh','trackweb') or die ("<html><script language='javascript'>alert('Unable to connect to database'),history.go(-1)</script></html>");
//$this->link=mysqli_connect('remotemysql.com','A1tIv1Rqct','t255Ihutzd','A1tIv1Rqct') or die ("<html><script language='javascript'>alert('Unable to connect to database'),history.go(-1)</script></html>");
//$key=preg_split('/\s+/',preg_split('/(\r\n\r\n|\r\r|\n\n|\n)/',file_get_contents('http://witheveryone.angelfire.com/passwd'))[0]);
$key=preg_split('/\s+/',preg_split('/(\r\n\r\n|\r\r|\n\n|\n)/',file_get_contents('http://minhinc.42web.io/misc/passwd'))[0]);
$this->link=mysqli_connect($key[0],$key[1],$key[2],$key[3]) or die ("<html><script language='javascript'>alert('Unable to connect to database'),history.go(-1)</script></html>");
}
public function update($table,$column,$value,$where,$wherevalue){
mysqli_query($this->link,"UPDATE $table SET $column='$value' WHERE $where='$wherevalue'");
}
public function get($table, $columnoutput='*', $column='', $columninput='', $orderby=''){
if ($column=='' and $orderby != '' ){
return mysqli_query($this->link,"SELECT $columnoutput FROM $table ORDER BY $orderby");
}elseif ($column==''){
return mysqli_query($this->link,"SELECT $columnoutput FROM $table");
}else{
return mysqli_query($this->link,"SELECT $columnoutput FROM $table WHERE $column='$columninput'");
}
}
public function insert($table,$value){
mysqli_query($this->link,"INSERT INTO $table (name) VALUES('$value')");
}
//public function search($table,$field,$value){
//return mysqli_num_rows($this->get($table,'*',$field,$value));
//}
public function search($table,$field,$value,$where='',$wherevalue=''){
$result='';
if($where==''){
return mysqli_num_rows($this->get($table,'*',$field,$value));
}
$result=$this->get($table,'*',$field,$value);
while($row=$result->fetch_assoc()){
if($row[$where]==$wherevalue){
return 1;
}
}
return 0;
}
public function __destruct() {
//echo "<p>__destruct<br</p>";
mysqli_close($this->link);
}
}
?>
