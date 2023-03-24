<?
class Utilbc{
public $level='.';
public $headername="";
public $subitem="";
public $script="";
public $chap="";
public $db;
public $json="";
public function __construct(){
 require_once('Databasem.php');
 $this->db=new Databasec;
//foreach(split("\/",split("public_html\/?",ereg_replace("\/*$","",getcwd()))[1]) as $item){
foreach(preg_split("/\//",$_SERVER['SCRIPT_NAME']) as $item){
if(!empty($item) and !preg_match('/[.]php$/',$item)){
 if($this->level=='.')
  $this->headername=$item;
 elseif(empty($this->subitem))
  $this->subitem=$item;
 $this->level=$this->level."/..";
 }elseif(preg_match('/[.]php$/',$item) and $item!='index.php')
  $this->script='http://www.minhinc.42web.io/'.preg_replace('/(.*)[.]php$/','$1',$_SERVER['SCRIPT_NAME']);
  if (isset($_GET['chap'])){
   $this->chap='-chap'.$_GET['chap'];
  }
}
 $this->drawheader();
if(!empty($this->script))
 //echo file_get_contents($this->script);
 $this->drawscript();
else{
 if(empty($this->headername))
  $this->json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name','main'))[0],true);
 elseif(empty($this->subitem))
  $this->json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$this->headername))[0],true);
 else
  $this->json=json_decode(mysqli_fetch_row($this->db->get('headername','content','name',$this->subitem))[0],true);
 $this->draw();
}
 $this->drawfooter();
}
}
?>
